from flask import Blueprint, request, jsonify
from database.mos import Mos, MosActions
from decorators.auth import ensure_logged_in

mos = Blueprint('mos', __name__)

# auxiliary create mos function
def create_mos(data):
    new_mos = {
        'mos_job_field': data['mos_job_field']
    }
    
    return new_mos

# GET ALL, POST new mos
@mos.route('/mos', methods=['GET', 'POST']) # default method is get, just being explicit
# @ensure_logged_in
def get_moss():
    if request.method == "GET":
        return MosActions.get_all()
    # request.method = "POST"
    if request.is_json:
        data = request.get_json()

        new_mos = create_mos(data)
    
        db_response = MosActions.post(new_mos)
        return db_response
    # client error
    return jsonify(
        error = "The request payload is not in JSON format"
    ), 400


# GET SINGLE mos
@mos.route('/mos/<int:mos_id>', methods=['GET']) # default method is get
# @ensure_logged_in
def get_single_mos(mos_id):
    mos = Mos.find_by_id(mos_id)
    if mos:
        return mos.json()
    return jsonify(
        error = "no military occupational specialty found with given id"
    ), 404

# UPDATE SINGLE mos
@mos.route('/mos/<int:mos_id>', methods=['PUT'])
# @ensure_logged_in
def update_mos(mos_id):
    # should be idempotent but just updating if in db for now
    if request.is_json:
        data = request.get_json()
    
        new_mos = create_mos(data)

        db_response = MosActions.update_mos(mos_id, new_mos)
        return db_response
    # client error
    return jsonify(
        error = "The request payload is not in JSON format"
    ), 400

# DELETE SINGLE mos
@mos.route('/mos/<int:mos_id>', methods=['DELETE'])
# @ensure_logged_in
def delete_mos(mos_id):
    return MosActions.delete_mos(mos_id)