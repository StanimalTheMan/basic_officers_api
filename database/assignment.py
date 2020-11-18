import sqlite3
from flask import jsonify
from database.officer import Officer
from database.year import Year

class Assignment():
    TABLE_NAME = 'assignments'

    def __init__(self, _id, overhire, remarks, officer_id, year_id):
        self.id = _id
        self.overhire = overhire
        self.remarks = remarks
        self.officer_id = officer_id
        self.year_id = year_id

    def json(self):
        return {
            "id": self.id,
            "overhire": self.overhire,
            "remarks": self.remarks,
            "officer_id": self.officer_id,
            "year_id": self.year_id
        }

    @classmethod
    def find_by_id(cls, _id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM {table} WHERE id=?".format(table=cls.TABLE_NAME)
        result = cursor.execute(query, (_id,))
        row = result.fetchone()

        if row:
            assignment = cls(*row)
        else:
            assignment = None 

        connection.close()
        
        return assignment

class AssignmentActions():
    
    @staticmethod
    def get_all():
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM {table}".format(table=Assignment.TABLE_NAME)
        results = cursor.execute(query)

        assignment_lst = []
        
        for row in results:
            officer = Officer.find_by_id(row[3]) # hardcoding is bad
            year = Year.find_by_id(row[4])
            assignment_lst.append({
                                'id': row[0],
                                'overhire': row[1],
                                'remarks': row[2],
                                'officer_id': row[3],
                                'officer': officer.json(),
                                'year_id': row[4],
                                'year': year.json()
                            })

        connection.close()

        if assignment_lst:
            return jsonify(
                assignments = assignment_lst
            )
        return jsonify(
            message = "No assignments found"
        )

    @staticmethod
    def post(new_assignment):
        try:
            # probably can isolate db connection into separate try except
            connection = sqlite3.connect('data.db')
            cursor = connection.cursor()
            cursor.execute("PRAGMA foreign_keys = ON")

            query = "INSERT INTO {table} VALUES (NULL, ?, ?, ?, ?)".format(table=Assignment.TABLE_NAME)
            cursor.execute(query, (new_assignment['overhire'], new_assignment['remarks'], new_assignment['officer_id'],
                                    new_assignment['year_id']))
            cursor.close()

            connection.commit()
            connection.close()
        except sqlite3.Error as e:
            # assume connection error or foreign key constraint error
            # need to look into some more
            print(e)
            return jsonify(
                error = "Database connection error or Foreign Key Constraint Error."
            ), 500
        return jsonify(
            # identifying assignment by id is vague to user
            message = f"Assignment has been created successfully."
        )

    @staticmethod
    def update_assignment(assignment_id, new_assignment):
        try:
            connection = sqlite3.connect('data.db')
            cursor = connection.cursor()
            cursor.execute("PRAGMA foreign_keys = ON")

            query = "SELECT * FROM {table} WHERE id={assignmentId}".format(table=Assignment.TABLE_NAME, assignmentId=assignment_id)
            
            result = cursor.execute(query)
            row = result.fetchone()
            if not row:
                # tentative as PUT request should create new if resource doesn't exist?
                return jsonify(
                    error = "No assignment found with supplied id"
                ), 404

            query = "UPDATE {table} SET overhire=?, remarks=?, officer_id=?, year_id=? WHERE id={assignmentId}".format(table=Assignment.TABLE_NAME, assignmentId=assignment_id)
            cursor.execute(query, (new_assignment['overhire'], new_assignment['remarks'], new_assignment['officer_id'], new_assignment['year_id']))

            cursor.close()
            connection.commit()
            connection.close()
        except sqlite3.Error as e:
            return jsonify(
                error = "Foreign key constraint failed"
            )

        return jsonify (
            message = f"Assignment {new_assignment[assignment_id]} successfully updated"
        ), 201

    @staticmethod
    def delete_assignment(assignment_id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        
        query = "SELECT * FROM {table} WHERE id={assignmentId}".format(table=Assignment.TABLE_NAME, assignmentId=assignment_id)
        result = cursor.execute(query)

        row = result.fetchone()
        if not row:
            return jsonify(
                error = "No assignment found with supplied id"
            ), 404
        
        query = "DELETE FROM {table} WHERE id=?".format(table=Assignment.TABLE_NAME)
        cursor.execute(query, (assignment_id,))

        connection.commit()
        connection.close()
        return jsonify(
            message = f"Assignment {assignment_id} successfully deleted."
        ), 200