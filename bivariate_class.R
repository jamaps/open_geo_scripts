# creating bivariate classifications of data in R

library(plotrix)
library(ggplot2)

setwd("~/to/folder")

df <- read.csv('data.csv')

# decide how to break the data for biv - in this case 3 bins each
quantile(df$tmode, probs = c(0,0.3333,0.6667,1), na.rm = TRUE)
quantile(df$medinc, probs = c(0,0.3333,0.6667,1), na.rm = TRUE)

# bin the data into a new column
mb <- c(65000,85000)
tm <- c(0.3,0.4)
df$bi_inc_mode <- NA
df$bi_inc_mode[df$medinc<mb[1] & df$tmode<tm[1]] <- 'A1'
df$bi_inc_mode[(df$medinc>=mb[1] & df$medinc<mb[2]) & df$tmode<tm[1]] <- 'A2'
df$bi_inc_mode[df$medinc>=mb[2] & df$tmode<tm[1]] <- 'A3'
df$bi_inc_mode[df$medinc<mb[1] & (df$tmode>=tm[1]&df$tmode<tm[2])] <- 'B1'
df$bi_inc_mode[(df$medinc>=mb[1] & df$medinc<mb[2]) & (df$tmode>=tm[1]&df$tmode<tm[2])] <- 'B2'
df$bi_inc_mode[df$medinc>=mb[2] & (df$tmode>=tm[1]&df$tmode<tm[2])] <- 'B3'
df$bi_inc_mode[df$medinc<mb[1] & df$tmode>=tm[2]] <- 'C1'
df$bi_inc_mode[(df$medinc>=mb[1] & df$medinc<mb[2]) & df$tmode>=tm[2]] <- 'C2'
df$bi_inc_mode[df$medinc>=mb[2] & df$tmode>=tm[2]] <- 'C3'

# then output wherever needed
