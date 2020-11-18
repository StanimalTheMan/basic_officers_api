from flask import Blueprint, request, jsonify
from database.assignment import Assignment, AssignmentActions
from decorators.auth import ensure_logged_in

assignment = Blueprint('Assignment', __name__)

# auxiliary create rank function
def create_assignment(data):

    # self.id = _id
    # self.cmu = cmu
    # self.academic_year = academic_year
    # self.overhire = overhire
    # self.remarks = remarks
    # self.officer_id = officer_id

    new_assignment = {
        'overhire': data['overhire'],
        'remarks': data['remarks'],
        'officer_id': data['officer_id'],
        'year_id': data['year_id']
    }
    
    return new_assignment

# GET ALL, POST new rank
@assignment.route('/assignments', methods=['GET', 'POST']) # default method is get, just being explicit
# @ensure_logged_in
def get_assignments():
    if request.method == "GET":
        return AssignmentActions.get_all()
    # request.method = "POST"
    if request.is_json:
        data = request.get_json()

        new_assignment = create_assignment(data)
    
        db_response = AssignmentActions.post(new_assignment)
        return db_response
    # client error
    return jsonify(
        error = "The request payload is not in JSON format"
    ), 400


# GET SINGLE OFFICER
@assignment.route('/assignments/<int:assignment_id>', methods=['GET']) # default method is get
# @ensure_logged_in
def get_single_officer(assignment_id):
    assignment = Assignment.find_by_id(assignment_id)
    if assignment:
        return assignment.json()
    return jsonify(
        error = "no assignment found with given id"
    ), 404

# UPDATE SINGLE OFFICER
@assignment.route('/assignments/<int:assignment_id>', methods=['PUT'])
# @ensure_logged_in
def update_assignment(assignment_id):
    # should be idempotent but just updating if in db for now
    if request.is_json:
        data = request.get_json()
    
        new_assignment = create_assignment(data)

        db_response = AssignmentActions.update_assignment(assignment_id, new_assignment)
        return db_response
    # client error
    return jsonify(
        error = "The request payload is not in JSON format"
    ), 400

# DELETE SINGLE OFFICER
@assignment.route('/assignments/<int:assignment_id>', methods=['DELETE'])
# @ensure_logged_in
def delete_assignment(assignment_id):
    return AssignmentActions.delete_assignment(assignment_id)