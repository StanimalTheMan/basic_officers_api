from flask import Blueprint, request, jsonify
from database.rank import Rank, RankActions
from decorators.auth import ensure_logged_in

rank = Blueprint('rank', __name__)

# auxiliary create rank function
def create_rank(data):
    new_rank = {
        'officer_rank': data['officer_rank']
    }
    
    return new_rank

# GET ALL, POST new rank
@rank.route('/ranks', methods=['GET', 'POST']) # default method is get, just being explicit
# @ensure_logged_in
def get_ranks():
    if request.method == "GET":
        return RankActions.get_all()
    # request.method = "POST"
    if request.is_json:
        data = request.get_json()

        new_rank = create_rank(data)
    
        db_response = RankActions.post(new_rank)
        return db_response
    # client error
    return jsonify(
        error = "The request payload is not in JSON format"
    ), 400


# GET SINGLE RANK
@rank.route('/ranks/<int:rank_id>', methods=['GET']) # default method is get
# @ensure_logged_in
def get_single_rank(rank_id):
    rank = Rank.find_by_id(rank_id)
    if rank:
        return rank.json()
    return jsonify(
        error = "no rank found with given id"
    ), 404

# UPDATE SINGLE RANK
@rank.route('/ranks/<int:rank_id>', methods=['PUT'])
# @ensure_logged_in
def update_rank(rank_id):
    # should be idempotent but just updating if in db for now
    if request.is_json:
        data = request.get_json()
    
        new_rank = create_rank(data)

        db_response = RankActions.update_rank(rank_id, new_rank)
        return db_response
    # client error
    return jsonify(
        error = "The request payload is not in JSON format"
    ), 400

# DELETE SINGLE RANK
@rank.route('/ranks/<int:rank_id>', methods=['DELETE'])
# @ensure_logged_in
def delete_rank(rank_id):
    return RankActions.delete_rank(rank_id)