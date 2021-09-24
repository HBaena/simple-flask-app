from flask import request  # receiving data from requests
from flask import jsonify  # Make a response (like dict)
from flask import make_response  # Make a response (like dict)

from flask_restful import Resource  # modules for fast creation of apis
from flask_apispec import marshal_with, doc, use_kwargs
from flask_apispec.views import MethodResource

from marshmallow import Schema, fields, validate

from model.enum import StatusMsg, ErrorMsg

from functions import coords_from_address, is_in_mkad, get_distance

from pathlib import Path

from typeguard import check_type

from icecream import ic


class ResponseSchema(Schema):
    """
        Define a format for API response
    """
    class DistanceSchema(Schema):
        """
            Define a format for distance response
        """
        text = fields.Str(default='Nothing')
        value = fields.Integer(default=0)


    status = fields.Str(validate=validate.OneOf(
        [StatusMsg.FAIL, StatusMsg.OK]), required=True)  # String that always is returned
    message = fields.Str(validate=validate.OneOf([
        'address is needed', 'address not found', 'address is iside of MKAD',
        'originis address is not measurable', 'distance meassured correclty',
        'an error occurred'
    ]), required=True)  # String that always is returned
    error = fields.Str(optional=True, validate=validate.OneOf([
        ErrorMsg.MISSING_VALUES, ErrorMsg.INVALID_VALUE, ErrorMsg.INVALID_VALUE,
        ErrorMsg.TYPE_ERROR, ErrorMsg.UNKNOWN_ERROR
    ]))
    # distance = fields.Dict()
    distance = fields.Nested(DistanceSchema)


class RequestSchema(Schema):
    """
        Define a format for apis request
    """
    address = fields.Str()


class MeassureDistance(MethodResource, Resource):
    @doc(
        description='Get distance from <i>addres</i> to <b>MDAK</b> taken as parammeter some address making use of google maps api',
        tags=['Distance']
    )  # Adding a brief description for endpoint 
    @marshal_with(ResponseSchema)  # Adding response schema
    @use_kwargs(RequestSchema)  # Adding request schema
    def get(self):
        """
        Function: get
        Summary: HTTP GET methdo to meassure distance between a address and MKAD
        Examples: distance from Madrid, Spain to MKAD
        Parameters:
            address (str): Address of origin
        Returns: Status,
        """
        address = request.args.get('address')  # Get address (it does not fail if address is not sent)
        try:
            if not address:  # Check if addres is sent
                return make_response(jsonify(
                    status=StatusMsg.FAIL, error=ErrorMsg.MISSING_VALUES, message='address is needed'), 400)
            check_type('address', address, str)  # Check for address type
            response = coords_from_address(address)  # Get coords and place_id from address
            if not response:  # If not response something was wrong with the address
                return make_response(jsonify(
                    status=StatusMsg.FAIL, error=ErrorMsg.INVALID_VALUE, message='address not found'), 400)
            coords, place_id = response
            if is_in_mkad(coords):  # Check if the coords are inside of MKAD
                return jsonify(status=StatusMsg.OK, message='address is iside of MKAD', distance=dict(
                    text='', value=0))
            # Get distance from input address to MKAD
            distance = get_distance(place_id)
            if not distance:  # If no distance are returned, the distance are not measurable
                return make_response(jsonify(
                    status=StatusMsg.FAIL, error=ErrorMsg.INVALID_VALUE, message='originis address is not measurable'), 400)
            with open(Path.cwd()/'distances.log', 'a') as f:
                f.write(f'{distance}\n')  # Write distance into .log file
                return jsonify(
                status=StatusMsg.OK, message='distance meassured correclty', distance=distance)
        # It is raised for unexpected types (Will never raised given that get's
        # parameter are always formated as strings)
        except TypeError as e:
            return make_response(jsonify(
                status=StatusMsg.FAIL, error=ErrorMsg.TYPE_ERROR, message='an error occurred', log=str(e)), 400)
        except Exception as e:  # Any other error
            return make_response(jsonify(
                status=StatusMsg.FAIL, error=ErrorMsg.UNKNOWN_ERROR, message='an error occurred', log=str(e)), 500)
