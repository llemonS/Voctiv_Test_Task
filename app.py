from flask import Flask, jsonify
from distance_finder.api import distance_finder
import logging

app = Flask(__name__)
app.register_blueprint(distance_finder)

logging.basicConfig(filename='distance_logs.log', level=logging.INFO)


@app.errorhandler(404)
def page_not_found(error):
    return jsonify({"message":"This endpoint does not exists."}), 404

@app.errorhandler(405)
def page_not_found(error):
    return jsonify({"message":"Sorry, this method is not allowed in our API."}), 405 
    

if __name__ == '__main__':

    app.run(debug=True)