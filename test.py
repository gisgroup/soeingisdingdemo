#!/usr/bin/env python

from gisgroup_api.distance.utils import *

if __name__ == '__main__':
    print  calculate(12.5579222330736, 55.6895903526632, 12.5679222330736, 55.6795903526632, testing=True), "\n"
#
# SELECT
# sum(num_hits) +
# count(1)
# from result_cache
# where
# created > NOW() - interval '24 hour'
# ;
#
#
# select * from result_cache
# where num_hits > 5
# limit 2;
