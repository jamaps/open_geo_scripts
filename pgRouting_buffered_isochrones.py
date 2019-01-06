# creates a network graph, then computes isochrones based on a travel distance and buffer length from edges

import psycopg2
import csv

def create_nearby_graph(dms_id):
    
    # sql query to create the graph for the dms_id
    query = '''
        -- select all edge gids that are 10km radius from the DMS location
        DROP TABLE IF EXISTS temp_osm_e;
        CREATE TABLE temp_osm_e AS (
            WITH temp_osm AS (
                SELECT 
                osm_edges_A.gid
                FROM
                osm_edges_A
                JOIN dms_locations on ST_DWithin(osm_edges_A.geom::geography, dms_locations.geom::geography, 10000)
                WHERE dms_locations.dms_id = %s
        ), temp_osm_ne AS (
        -- selects the full geometry from these nearby edges    
                SELECT 
                *
                FROM osm_edges_A
                WHERE osm_edges_A.gid IN (SELECT gid FROM temp_osm GROUP BY gid)
        ), 
        -- splits these into small (~100m segments when longer)
        segments AS (
                SELECT gid, oneway, (ST_MakeLine(lag((pt).geom, 1, NULL) OVER (PARTITION BY gid ORDER BY gid, (pt).path), (pt).geom)) AS geom
                  FROM (SELECT gid, oneway, ST_DumpPoints(ST_Segmentize(geom, 0.001)) AS pt FROM temp_osm_ne) as dumps
        )
        SELECT * FROM segments WHERE geom IS NOT NULL
        );            

        ALTER TABLE temp_osm_e ADD COLUMN source integer;
        ALTER TABLE temp_osm_e ADD COLUMN target integer;
        ALTER TABLE temp_osm_e ADD COLUMN cost integer;
        ALTER TABLE temp_osm_e ADD COLUMN id SERIAL PRIMARY KEY;
        UPDATE temp_osm_e SET cost = ST_LENGTH(geom::geography);

        SELECT pgr_createTopology('temp_osm_e',0.00001,the_geom:='geom',id:='id',source:='source',target:='target');
        '''
    
    cursor.execute(query %dms_id) # (query %dms_id)
    connection.commit()

    
def generate_buffers(dms_id, distance, buffer):
    
    query = '''
    WITH nne AS (
    -- find the network edge that is closest to the DMS location
    SELECT 
        *
        FROM temp_osm_e
        ORDER BY geom::geography <-> (
            SELECT geom::geography FROM dms_locations WHERE dms_id = ''' + dms_id + '''
        )
        LIMIT 1
    ), 
    -- return the source node and its geom from this edge
    nnn AS (
        SELECT
        nne.source AS id,
        temp_osm_e_vertices_pgr.the_geom AS geom
        FROM nne
        JOIN temp_osm_e_vertices_pgr
        ON nne.source = temp_osm_e_vertices_pgr.id
    ), 
    -- return all edge that are X distance from this starting node 
    ni AS (
        SELECT * FROM
        pgr_drivingDistance('SELECT id, source, target, cost FROM temp_osm_e', (SELECT id FROM nnn), ''' + str(distance) + ''')
    )
    -- create buffered area around this edge
    INSERT INTO dms_d_buffers
    SELECT
    ''' + dms_id + ''' AS dms_id,
    ''' + str(distance) + ''' AS distance_m,
    ''' + str(buffer) + ''' AS buffer_size,
    ST_Union(ST_Buffer(temp_osm_e.geom::geography, ''' + str(buffer) + ''')::geometry) AS geom
    FROM 
    ni
    JOIN temp_osm_e ON temp_osm_e.id = ni.edge
    ;
    '''
    
    cursor.execute(query) # (query %dms_id)
    connection.commit()

try:
    
    # connect to the database
    connection = psycopg2.connect(user = "ja",
                                  password = "",
                                  host = "localhost",
                                  port = "5433",
                                  database = "dms")
    cursor = connection.cursor()
    # Print PostgreSQL Connection properties
    print ( connection.get_dsn_parameters(),"\n")
    # Print PostgreSQL version
    cursor.execute("SELECT version();")
    record = cursor.fetchone()
    print("You are connected to - ", record,"\n")


except:
    
    print("did not connect")


# create an empty table
query = '''
    DROP TABLE IF EXISTS dms_d_buffers;
    CREATE TABLE dms_d_buffers(
        dms_id TEXT,
        distance_m INT,
        buffer_size INT,
        geom GEOGRAPHY
    );
'''
cursor.execute(query) # (query %dms_id)
connection.commit()


failed_dms_dist = []

dms_id_list = []
with open("dms_data/DMS_valid2.csv", "r") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        dms_id_list.append(row["dms_id"])

c = 1
for dmsid in dms_id_list:
    
    dmsid = "'" + dmsid + "'"
    
    print(c, dmsid)

    try:
        create_nearby_graph(dmsid)
    except:
        cursor.execute("rollback;") # (query %dms_id)
        connection.commit()
        create_nearby_graph(dmsid)

    dms_distance_list = [1000,3000,5000,10000]
    
    
    for dms_distance in dms_distance_list:

        # re-run for different buffer size if it fails - this happened for ~100 or so of the 869 * 4 buffers
        try:
            generate_buffers(dmsid,dms_distance,25)
        except:
            try:
                generate_buffers(dmsid,dms_distance,23)
            except:
                try:
                    generate_buffers(dmsid,dms_distance,27)
                except:
                    try:
                        generate_buffers(dmsid,dms_distance,21)
                    except:
                        failed_dms_dist.append([dmsid,dms_distance])
    
    
    c += 1
    
if(connection):
    cursor.close()
    connection.close()
    print("PostgreSQL connection is closed")
