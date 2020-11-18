import sqlite3 
from flask import jsonify

class Mos():
    TABLE_NAME = 'mos'

    def __init__(self, _id, mos_job_field):
        self.id = _id 
        self.mos_job_field = mos_job_field

    def json(self):
        return {
            "id": self.id,
            "mos_job_field": self.mos_job_field
        }
    
    @classmethod
    def find_by_id(cls, _id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM {table} WHERE id=?".format(table=cls.TABLE_NAME)
        result = cursor.execute(query, (_id,))
        row = result.fetchone()

        if row:
            mos = cls(*row)
        else:
            mos = None

        connection.close()

        return mos 

class MosActions():

    @staticmethod
    def get_all():
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM {table}".format(table=Mos.TABLE_NAME)
        results = cursor.execute(query)

        mos_lst = []

        for row in results:
            mos_lst.append({
                'id': row[0],
                'mos_job_field': row[1]
            })

        connection.close()

        if mos_lst:
            return jsonify(
                mos_job_fields = mos_lst
            )
        return jsonify(
            message = "No military occupational specialties found"
        )

    @staticmethod
    def post(new_mos):
        try:
            # probably can isolate connection into separate try except
            connection = sqlite3.connect('data.db')
            cursor = connection.cursor()

            query = "INSERT INTO {table} VALUES (NULL, ?)".format(table=Mos.TABLE_NAME)
            cursor.execute(query, (new_mos['mos_job_field'],))
        
            connection.commit()
            connection.close()
        except sqlite3.Error as e:
            # assume connection error
            # print(e)
            return jsonify(
                error = "Database connection error."
            ), 500
        return jsonify (
            # identifying mos by id is another option
            message = f"Mos {new_mos['mos_job_field']} has been created successfully."
        )

    @staticmethod
    def update_mos(mos_id, new_mos):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "SELECT * FROM {table} WHERE id={mosId}".format(table=Mos.TABLE_NAME, mosId=mos_id)

        result = cursor.execute(query)
        row = result.fetchone()
        if not row:
            # tentative as PUT request should create new if resource doesn't exist?
            return jsonify(
                error = "No mos found with supplied id"
            ), 404

        query = "UPDATE {table} SET  mos_job_field=? WHERE id={mosId}".format(table=Mos.TABLE_NAME, mosId = mos_id)
        cursor.execute(query, (new_mos['mos_job_field'],))

        connection.commit()
        connection.close()

        return jsonify (
            message = f"Military occupational specialty {mos_id} successfully updated"
        ), 201

    @staticmethod
    def delete_mos(mos_id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        
        query = "SELECT * FROM {table} WHERE id={mosId}".format(table=Mos.TABLE_NAME, mosId=mos_id)
        result = cursor.execute(query)

        row = result.fetchone()
        print(row)
        if not row:
            return jsonify(
                error = "No military occupational specialty found with supplied id"
            )
        
        query = "DELETE FROM {table} WHERE id=?".format(table=Mos.TABLE_NAME)
        cursor.execute(query, (mos_id,))

        connection.commit()
        connection.close()
        return jsonify(
            message = f"Military occupational specialty {mos_id} successfully deleted."
        ), 200