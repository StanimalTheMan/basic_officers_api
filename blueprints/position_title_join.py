from flask import Blueprint, request, jsonify
from database.joins.row_data import RowDataActions
from decorators.auth import ensure_logged_in

position_title_join = Blueprint('position_title_join', __name__)

@position_title_join.route('/data', methods=['GET']) # better to be explicit
# @ensure_logged_in
def get_data():
    return RowDataActions.get_data()
