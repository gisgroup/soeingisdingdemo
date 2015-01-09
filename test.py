#!/usr/bin/env python

from gisgroup_api.distance.utils import *
from gisgroup_api.apis.rejseplanen import get as getrp

if __name__ == '__main__':
    print  calculate(12.5579222330736, 55.6895903526632, "strain", testing=True), "\n"
    print  calculate(12.5579222330736, 55.6895903526632, "stop", testing=True), "\n"
    print  calculate(12.5579222330736, 55.6895903526632, "metro", testing=True), "\n"
    print  calculate(12.5579222330736, 55.6895903526632, "junction", testing=True), "\n"
    print  calculate(12.5579222330736, 55.6895903526632, "stationer", testing=True), "\n"

    print  calculate(12.5763016, 55.6776306, "metro", testing=True), "\n"
    print  calculate(12.5763016, 55.6776306, "strain", testing=True), "\n"
    print  calculate(12.557914, 55.6895831, "metro", testing=True), "\n"
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