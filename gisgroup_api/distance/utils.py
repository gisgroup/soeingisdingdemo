"""
    gisgroup_api.distance.utils
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Provide distance calculation capabilities
"""
import os
from flask import current_app
from ..database import connection as conn

from collections import namedtuple
Result = namedtuple('Result', 'name cost x y')
Point = namedtuple('Point', 'x y')

SEARCH_RADIUS = 50000
KNN = 5
CACHE_SEARC_RADIUS = 5

def nearest_neighbour( point ):
    """
    Given a point object, returns the nearest node in road network graph
    """
    cur = conn.cursor()

    # this try block ensures that the transaction is closed on errors
    try:
        # select closest node to given point
        # sql = """SELECT source, osm_name
        #          FROM danmark
        #          ORDER BY ST_Distance(
        #             geom_way,
        #             -- ST_Transform(
        #                 ST_SetSRID(ST_MakePoint( %(x)s, %(y)s ),4326)
        #             --,25832)
        #          )
        #          ASC LIMIT 1"""

        sql = """
	        SELECT source, osm_name
	        FROM danmark
	        ORDER BY
	                 geom_way <-> ST_SetSRID(ST_MakePoint( %(x)s, %(y)s ),4326)
	        ASC LIMIT 1
        """

        data = {
            'x': point.x,
            'y': point.y
        }

        cur.execute( sql, data )
        node = cur.fetchone()

    finally:
        cur.close()

    return node

def calculate( origin_x, origin_y, target_x, target_y, testing=False):
    """
    Calculates the closest POI to an origin coordinate pair
    """

        # this try block ensures that the db transaction is closed on error

    try:
        cur = conn.cursor()

        # determine node closest to origin location
        origin = Point( origin_x, origin_y )
        target = Point( target_x, target_y )
        (origin_node, origin_name) = nearest_neighbour( origin )
        (target_node, target_name) = nearest_neighbour( target )

        if not testing:
            current_app.logger.debug( "Found %s" % origin_name )



        # put target node ids into separate list for easy lookup
        target_nodes = [target_node]

        djks_max_dist = 2000;

        # then we can perform the distance calculation
        # here we also constrain the search to a given radius threshold
        sql = """SELECT seq, id1 AS source, id2 AS target, cost
        FROM
            pgr_kdijkstraCost(
                    'SELECT *
                        FROM danmark',
                    %(source)s,
                    %(target)s,
                    false,
                    false
            )
        WHERE cost > 0
        ORDER BY cost
        LIMIT 1
        """

        data = {
            'source': origin_node,
            'target': target_nodes,
            'x': origin_x,
            'y': origin_y,
            'radius': djks_max_dist
        }

        cur.execute(sql, data)

        # the pg routing result is a list of tuples in the format:
        #   ( sequence-number, source node id, target node id, cost in km )
        rows = cur.fetchall()
        (seq, id1, id2, cost)  = rows[0]


        if not testing:
            current_app.logger.debug( rows )



    finally:
        conn.commit()

    return cost
