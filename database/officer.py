import sqlite3
from flask import jsonify

class Officer():
    TABLE_NAME = 'officers'

    def __init__(self, _id, first_name, last_name, rank_id, position_id, mos_id):
        self.id = _id
        self.first_name = first_name
        self.last_name = last_name
        self.rank_id = rank_id
        self.position_id = position_id
        self.mos_id = mos_id

    def json(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "rank_id": self.rank_id,
            "position_id": self.position_id,
            "mos_id": self.mos_id
        }

    @classmethod
    def find_by_id(cls, _id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM {table} WHERE id=?".format(table=cls.TABLE_NAME)
        result = cursor.execute(query, (_id,))
        row = result.fetchone()

        if row:
            officer = cls(*row)
        else:
            officer = None 

        connection.close()
        
        return officer

class OfficerActions():
    
    @staticmethod
    def get_all():
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM {table}".format(table=Officer.TABLE_NAME)
        results = cursor.execute(query)

        officer_lst = []
        
        for row in results:
            officer_lst.append({
                                'id': row[0],
                                'first_name': row[1],
                                'last_name': row[2],
                                'rank_id': row[3],
                                'position_id': row[4],
                                'mos_id': row[5]
                            })

        connection.close()

        if officer_lst:
            return jsonify(
                officers = officer_lst
            )
        return jsonify(
            message = "No officers found"
        )

    @staticmethod
    def get_officers_with_position_title(position_title_id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM {table} WHERE position_id=?".format(table=Officer.TABLE_NAME)
        results = cursor.execute(query, (position_title_id,))

        personnel = []

        for row in results:
            personnel.append({
                'id': row[0],
                'full_name': row[1] + ' ' + row[2]
            })

        connection.close()

        if personnel:
            return jsonify(
                personnel = personnel
            )
        return jsonify(
            message = "No officers with position found"
        )

    @staticmethod
    def post(new_officer):
        try:
            # probably can isolate db connection into separate try except
            connection = sqlite3.connect('data.db')
            cursor = connection.cursor()
            cursor.execute("PRAGMA foreign_keys = ON")

            query = "INSERT INTO {table} VALUES (NULL, ?, ?, ?, ?, ?)".format(table=Officer.TABLE_NAME)
            cursor.execute(query, (new_officer['first_name'], new_officer['last_name'], new_officer['rank_id'],
                                   new_officer['position_id'], new_officer['mos_id']))
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
            # identifying officer by id is another option albeit vague to user
            message = f"Officer {new_officer['last_name']} has been created successfully."
        )

    @staticmethod
    def update_officer(officer_id, new_officer):
        try:
            connection = sqlite3.connect('data.db')
            cursor = connection.cursor()
            cursor.execute("PRAGMA foreign_keys = ON")

            query = "SELECT * FROM {table} WHERE id={officerId}".format(table=Officer.TABLE_NAME, officerId=officer_id)
            
            result = cursor.execute(query)
            row = result.fetchone()
            if not row:
                # tentative as PUT request should create new if resource doesn't exist?
                return jsonify(
                    error = "No officer found with supplied id"
                ), 404

            query = "UPDATE {table} SET  first_name=?, last_name=?, rank_id=?, position_id=?, mos_id=? WHERE id={officerId}".format(table=Officer.TABLE_NAME, officerId=officer_id)
            cursor.execute(query, (new_officer['first_name'], new_officer['last_name'], new_officer['rank_id'], new_officer['position_id'], new_officer['mos_id']))

            cursor.close()
            connection.commit()
            connection.close()
        except sqlite3.Error as e:
            return jsonify(
                error = "Foreign key constraint failed"
            )

        return jsonify (
            message = f"Officer {new_officer['last_name']} successfully updated"
        ), 201

    @staticmethod
    def delete_officer(officer_id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        
        query = "SELECT * FROM {table} WHERE id={officerId}".format(table=Officer.TABLE_NAME, officerId=officer_id)
        result = cursor.execute(query)

        row = result.fetchone()
        if not row:
            return jsonify(
                error = "No officer found with supplied id"
            ), 404
        
        query = "DELETE FROM {table} WHERE id=?".format(table=Officer.TABLE_NAME)
        cursor.execute(query, (officer_id,))

        connection.commit()
        connection.close()
        return jsonify(
            message = f"Officer {officer_id} successfully deleted."
        ), 200