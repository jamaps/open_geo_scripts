#######################################################
# shell scripts that make my life a little bit easier #
#######################################################
# last updated by Jeff Allen on August 24, 2015


# looping through directories:
for d in */ ; do
    echo "$d"
done


# looping through all folders in a directory
for d in */ ; do
  for x in "$d"/*/ ; do
      echo "$x"
  done
done


# create new directories
mkdir folder_name
mkdir folder1 folder2 folder3


# create same set of new folders for loop of directories
for d in */ ; do
    mkdir "$d"folder1 "$d"folder2
done
# example - folder for every province/territory
for d in */ ; do
    mkdir "$d"AB "$d"BC "$d"MB "$d" "$d"NB "$d"NL "$d"NS "$d"NT "$d"NU "$d"ON "$d"PE "$d"QC "$d"SK "$d"YT
done


# rename files
mv old_file_name new_file_name


# zipping individual folders - without DS_Store
zip -r folder.zip folder -x "*.DS_Store"


# zipping all folders in a directory
for d in *; do
    zip -r -X "$d".zip "$d" -x "*.DS_Store"
done


# deleting directories
rm -rf folder_name


# 
for d in */ ; do
  for x in "$d"* ; do
      zip -r -X "$x".zip "$x" -x "*.DS_Store"
      rm -rf "$x"
  done
done
