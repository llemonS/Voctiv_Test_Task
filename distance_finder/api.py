from flask import Blueprint, request, jsonify, render_template, request, redirect, url_for
from distance_finder.mkad import haversine_distance, poly
from shapely.geometry import Point
from os import environ
import json, requests, logging


#credential stored in enviroment variables
access_key = str(environ['API_KEY'])

LOG = logging.getLogger(__name__)

distance_finder = Blueprint('distance_finder', __name__)


@distance_finder.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return jsonify({"message":"Post a address on this route."})
        
    if request.method == 'POST':
        body = dict(request.json)

        if "address" not in body:
            return jsonify({"message": 'You must insert "address" as key.'})

        if type(body['address']) != str:
            return jsonify({"message": "Value must be a valid string"})

        if len(body['address']) < 1:
            return jsonify({"message": "Please insert a valid string corresponding to the desired address."})
        
        else:
            #request on the positionstack API the lat long of the given address, if valid with high confidence then apply harvesine distance method.
            headers= {'content-type': 'application/json'}
            params = {'access_key': access_key  ,'query': str(body['address']),'limit':1}
            #getting coordinates of given address
            try:
                data = json.loads(requests.get('http://api.positionstack.com/v1/forward', params=params, headers=headers).text)
                if len(data['data']) >= 1:
                    lat_,lon_,confidence = data['data'][0]['latitude'], data['data'][0]['longitude'], data['data'][0]['confidence']
                else:
                    confidence = 0     
                      
            except IndexError:
                return jsonify({"message: You must provide better details of the given address."})

            if float(confidence) < 0.6:
                return jsonify({"message":"You must provide details of the address, the confidence by the given information stills low: {}".format(confidence)})
            
            place = Point(lat_,lon_)
        
            if place.within(poly):
                LOG.info("ADDRESS: {0} is located inside MKAD.".format(str(body['address'])))
                return jsonify({"message": "This address is located inside MKAD."})
            
            else:
                #first two coordinates represents the centroid of the mkad_km array, given by poly.centroid
                answer = haversine_distance(55.74477620680145,37.6132832348739, lat_,lon_)
                #sending result to log as required from challenge.
                LOG.info("ADDRESS: {0} DISTANCE: {1}  km far from the centroid of MKAD with confidence {2}".format(str(body['address']), str(answer), str(confidence)))
                return jsonify({"message": "This address is {0} km far from the centroid of MKAD polygon points with confidence {1}".format(answer,confidence)})

