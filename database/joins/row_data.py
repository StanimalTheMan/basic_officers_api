# need to refactor but don't know where to put join (controller?) code
import sqlite3
from flask import jsonify

from database.assignment import Assignment
from database.officer import Officer
from database.year import Year

class RowDataActions():
    @classmethod
    def get_data(cls):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT pt.id, pt.officer_position_title, GROUP_CONCAT(y.id) FROM position_titles pt LEFT JOIN position_years py ON pt.id=py.position_title_id LEFT JOIN years y ON y.id=py.year_id GROUP BY(pt.officer_position_title)"

        results = cursor.execute(query)

        # messy code but initialize data to return and proceed to get assignments for each year id
        data_lst = []
        for row in results:
            position_title_id = row[0]
            if row[2]:
                years = row[2].split(',')
            data_obj = {
                'position_title_id': position_title_id,
                'officer_position_title': row[1]
            }
            for year_id in years: # hardcoded index value on sql query result w/o sqlalchemy
                # get year name based on year id
                year_json = Year.find_by_id(year_id).json()
                # get assignment based on year id and position title id
                assignment = Assignment.find_by_position_id_and_year_id(year_id, position_title_id)
                if assignment:
                    assignment_json = assignment.json()
                    # print(year_json)
                    # print(assignment_json)
                    # get officer data based on officer_id
                    officer_json = Officer.find_by_id(assignment_json["officer_id"]).json()
                    # print(officer_json)
                    data_obj[year_json['academic_year']] = {
                        'id': assignment_json['id'],
                        'academic_year_id': assignment_json['year_id'],
                        'officer_full_name': officer_json['first_name'] + ' ' + officer_json['last_name']
                    }
                else:
                    data_obj[year_json['academic_year']] = {
                        'academic_year_id': year_id,
                        'officer_full_name': ''
                    }
            data_lst.append(data_obj)                    

        return jsonify({
            "data": data_lst
        })
    # BAD, will try to use many to many
    # using Position Titles as the leftmost table
    # @staticmethod
    # def get_data():
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()

        # probably bad to have query as plain string literal?
        # query = "SELECT pt.id, pt.officer_position_title, GROUP_CONCAT(y.academic_year) FROM position_titles pt LEFT JOIN assignments a ON pt.id=a.position_title_id LEFT JOIN years y ON a.year_id = y.id GROUP BY(pt.officer_position_title)"

        # results = cursor.execute(query)
        # years = set()
        # bad approach
        # one pass to get the unique annual assignments/years
        # for row in results:
        #     if row[2]:
        #         position_title_years = row[2].split(',') # contains dups possibly, bad to hardcode e.g. row[2] but w/o sqlalchemy and idk what db to use
        #         for yr in position_title_years:
        #             years.add(yr)

        # another pass to add the years to each of the items in data
        # results = cursor.execute(query)
        # data_lst = []
        # for row in results:
        #     data_obj = {}
        #     data_obj['officer_position_title'] = row[1]
        #     for yr in years:
        #         data_obj[yr] = yr # dummy value 
        #     data_lst.append(data_obj)
        
        # connection.close()
        # print(data_lst)
        # if data_lst:
        #     return jsonify(
        #         data = data_lst
        #     )
        # return jsonify(
        #     message = "No data available"
        # )

    # BAD
    # using Assignments as the leftmost table 
    # @staticmethod
    # def get_data():
    #     connection = sqlite3.connect('data.db')
    #     cursor = connection.cursor()

    #     # probably bad to have query as plain string literal?
    #     query = "SELECT * FROM assignments a LEFT JOIN years y on a.year_id=y.id LEFT JOIN officers o on a.officer_id=o.id LEFT JOIN position_titles pt on a.position_title_id=pt.id"

    #     results = cursor.execute(query)
    #     data_lst = []
    #     for row in results:
    #         print(row)
    #         data_lst.append({
    #             'assignment_id': row[0],
    #             'officer_id': row[3],
    #             'year_id': row[4],
    #             'position_title_id': row[5],
    #             row[7]: row[9] + ' ' + row[10],
    #             'position_title': row[15],
    #         })
        
    #     connection.close()
    #     print(data_lst)
    #     if data_lst:
    #         return jsonify(
    #             data = data_lst
    #         )
    #     return jsonify(
    #         message = "No data available"
    #     )