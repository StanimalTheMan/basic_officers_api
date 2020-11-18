from flask import Blueprint, request, jsonify
from database.position_title import PositionTitle, PositionTitleActions
from decorators.auth import ensure_logged_in

position_title = Blueprint('position_title', __name__)

# auxiliary create position_title function
def create_position_title(data):
    new_position_title = {
        'officer_position_title': data['officer_position_title']
    }
    
    return new_position_title

# GET ALL, POST new position_title
@position_title.route('/position_titles', methods=['GET', 'POST']) # default method is get, just being explicit
# @ensure_logged_in
def get_position_titles():
    if request.method == "GET":
        return PositionTitleActions.get_all()
    # request.method = "POST"
    print(request.get_json())
    if request.is_json:
        data = request.get_json()

        new_position_title = create_position_title(data)
        db_response = PositionTitleActions.post(new_position_title)
        return db_response
    # client error
    return jsonify(
        error = "The request payload is not in JSON format"
    ), 400


# GET SINGLE position_title
@position_title.route('/position_titles/<int:position_title_id>', methods=['GET']) # default method is get
# @ensure_logged_in
def get_single_position_title(position_title_id):
    position_title = PositionTitle.find_by_id(position_title_id)
    if position_title:
        return position_title.json()
    return jsonify(
        error = "no position_title found with given id"
    ), 404

# UPDATE SINGLE position_title
@position_title.route('/position_titles/<int:position_title_id>', methods=['PUT'])
# @ensure_logged_in
def update_position_title(position_title_id):
    # should be idempotent but just updating if in db for now
    if request.is_json:
        data = request.get_json()
    
        new_position_title = create_position_title(data)

        db_response = PositionTitleActions.update_position_title(position_title_id, new_position_title)
        return db_response
    # client error
    return jsonify(
        error = "The request payload is not in JSON format"
    ), 400

# DELETE SINGLE position_title
@position_title.route('/position_titles/<int:position_title_id>', methods=['DELETE'])
# @ensure_logged_in
def delete_position_title(position_title_id):
    return PositionTitleActions.delete_position_title(position_title_id)