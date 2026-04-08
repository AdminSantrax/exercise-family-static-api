"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def handle_members():
    members = jackson_family.get_all_members()
    return jsonify(members), 200

# this endpoint returns one specific member
@app.route('/members/<int:id>', methods=['GET'])
def handle_one_member(id):
    member = jackson_family.get_member(id)
    if member:
        return jsonify(member), 200
    return jsonify({'message': 'Member not found'}), 404


# this endpoint adds a new member
@app.route('/members', methods=['POST'])
def add_member_route():
    body = request.get_json()
    if not body:
        return jsonify({'message': 'Body not found'}), 400
    member = jackson_family.add_member(body)
    return jsonify(member), 200


# this endpoint deletes a member
@app.route('/members/<int:id>', methods=['DELETE'])
def delete_member_route(id):
    deleted = jackson_family.delete_member(id)
    if deleted:
        return jsonify({'done': True}), 200
    return jsonify({'message': 'Member not found'}), 404


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
