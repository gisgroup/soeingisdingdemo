"""
    gisgroup_api
    ~~~~~~~~~~~~
    The APIs provided by Gis Group
"""

from flask import Flask, jsonify, render_template
from werkzeug.exceptions import NotFound, BadRequest, HTTPException

# Define the WSGI application object
app = Flask(__name__)

# Configurations
app.config.from_object('gisgroup_api.config')


from gisgroup_api.distance import blueprint as distance_blueprint
app.register_blueprint( distance_blueprint )


#------------------ ERRORS ------------------#
# NOTE: I would have prefered to use exception classes instead of error codes
#       for these error handlers, but that wont be supported before flask
#       releases version 1.0

@app.errorhandler(400)
def handle_bad_request(error):
    response = jsonify({
        'message': error.description
    })
    response.status_code = 400
    return response

@app.errorhandler(404)
def handle_not_found(error):
    return "Gis Group API"

# Sample HTTP error handling
@app.errorhandler(Exception)
def handle_server_error(error):
    app.logger.debug(error);
    return "server_error %s" % error
