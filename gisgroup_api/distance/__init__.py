"""
    gisgroup_api.distance
    ~~~~~~~~~~~~~~~~~~~~~
    Provide endpoint for calculating distances between addresses and POIs
"""

import os
from flask import Blueprint, jsonify

from . import utils as distance_utils
from ..geocode import utils as geocode_utils

# initialize blueprint
blueprint = Blueprint('distance', __name__)

@blueprint.route( "/<target>/<origin>" )
def distance_address( target, origin ):
    location_origin = geocode_utils.findone( origin )
    location_target = geocode_utils.findone( target )
    coordinates_origin = location_origin.get('adgangsadresse').get('adgangspunkt').get('koordinater')
    coordinates_target = location_target.get('adgangsadresse').get('adgangspunkt').get('koordinater')

    r = distance_utils.calculate( coordinates_origin[0], coordinates_origin[1], coordinates_target[0], coordinates_target[1] )

    return jsonify(
        distance=r
    )
