from flask import Blueprint, request, jsonify
from database.officer import Officer, OfficerActions
from decorators.auth import ensure_logged_in

officer = Blueprint('officer', __name__)

# auxiliary create rank function
def create_officer(data):

    # "id": self.id,
    # "first_name": self.first_name,
    # "last_name": self.last_name,
    # "rank_id": self.rank_id,
    # "position_id": self.position_id,
    # "mos_id": self.mos_id

    new_officer = {
        'first_name': data['first_name'],
        'last_name': data['last_name'],
        'rank_id': data['rank_id'],
        'position_id': data['position_id'],
        'mos_id': data['mos_id']
    }
    
    return new_officer

# GET ALL, POST new rank
@officer.route('/officers', methods=['GET', 'POST']) # default method is get, just being explicit
# @ensure_logged_in
def get_officers():
    if request.method == "GET":
        return OfficerActions.get_all()
    # request.method = "POST"
    if request.is_json:
        data = request.get_json()

        new_officer = create_officer(data)
    
        db_response = OfficerActions.post(new_officer)
        return db_response
    # client error
    return jsonify(
        error = "The request payload is not in JSON format"
    ), 400

# NOT RESTFUL as getting officers with specific position id
@officer.route('/officers/positionTitle/<int:position_title_id>', methods=['GET'])
def get_officers_with_position_title(position_title_id):
    return OfficerActions.get_officers_with_position_title(position_title_id)

# GET SINGLE OFFICER
@officer.route('/officers/<int:officer_id>', methods=['GET']) # default method is get
# @ensure_logged_in
def get_single_officer(officer_id):
    officer = Officer.find_by_id(officer_id)
    if officer:
        return officer.json()
    return jsonify(
        error = "no officer found with given id"
    ), 404

# UPDATE SINGLE OFFICER
@officer.route('/officers/<int:officer_id>', methods=['PUT'])
# @ensure_logged_in
def update_officer(officer_id):
    # should be idempotent but just updating if in db for now
    if request.is_json:
        data = request.get_json()
    
        new_officer = create_officer(data)

        db_response = OfficerActions.update_officer(officer_id, new_officer)
        return db_response
    # client error
    return jsonify(
        error = "The request payload is not in JSON format"
    ), 400

# DELETE SINGLE OFFICER
@officer.route('/officers/<int:officer_id>', methods=['DELETE'])
# @ensure_logged_in
def delete_officer(officer_id):
    return OfficerActions.delete_officer(officer_id)