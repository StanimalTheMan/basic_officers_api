from flask import Blueprint, request, jsonify
from database.year import Year, YearActions
from decorators.auth import ensure_logged_in

year = Blueprint('year', __name__)

# auxiliary create year function
def create_year(data):
    new_year = {
        'academic_year': data['academic_year']
    }
    
    return new_year

# GET ALL, POST new year
@year.route('/years', methods=['GET', 'POST']) # default method is get, just being explicit
# @ensure_logged_in
def get_years():
    if request.method == "GET":
        return YearActions.get_all()
    # request.method = "POST"
    if request.is_json:
        data = request.get_json()

        new_year = create_year(data)
    
        db_response = YearActions.post(new_year)
        return db_response
    # client error
    return jsonify(
        error = "The request payload is not in JSON format"
    ), 400


# GET SINGLE YEAR
@year.route('/years/<int:year_id>', methods=['GET']) # default method is get
# @ensure_logged_in
def get_single_year(year_id):
    year = Year.find_by_id(year_id)
    if year:
        return year.json()
    return jsonify(
        error = "no year found with given id"
    ), 404

# UPDATE SINGLE YEAR
@year.route('/years/<int:year_id>', methods=['PUT'])
# @ensure_logged_in
def update_year(year_id):
    # should be idempotent but just updating if in db for now
    if request.is_json:
        data = request.get_json()
    
        new_year= create_year(data)

        db_response = YearActions.update_year(year_id, new_year)
        return db_response
    # client error
    return jsonify(
        error = "The request payload is not in JSON format"
    ), 400

# DELETE SINGLE YEAR
@year.route('/years/<int:year_id>', methods=['DELETE'])
# @ensure_logged_in
def delete_year(year_id):
    return YearActions.delete_year(year_id)