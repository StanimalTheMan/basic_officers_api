import sqlite3
from flask import jsonify

class Year():
    TABLE_NAME = 'years'

    def __init__(self, _id, academic_year):
        self.id = _id
        self.academic_year = academic_year

    def json(self):
        return {
            "id": self.id,
            "academic_year": self.academic_year
        }

    @classmethod
    def find_by_id(cls, _id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM {table} WHERE id=?".format(table=cls.TABLE_NAME)
        result = cursor.execute(query, (_id,))
        row = result.fetchone()

        if row:
            year = cls(*row)
        else:
            year = None 

        connection.close()
        
        return year

class YearActions():
    
    @staticmethod
    def get_all():
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM {table}".format(table=Year.TABLE_NAME)
        results = cursor.execute(query)

        year_lst = []

        for row in results:
            year_lst.append({
                                'id': row[0],
                                'academic_year': row[1]
                            })

        connection.close()

        if year_lst:
            return jsonify(
                academic_years = year_lst
            )
        return jsonify(
            message = "No years found"
        )

    @staticmethod
    def post(new_year):
        try:
            # probably can isolate db connection into separate try except
            connection = sqlite3.connect('data.db')
            cursor = connection.cursor()

            query = "INSERT INTO {table} VALUES (NULL, ?)".format(table=Year.TABLE_NAME)
            cursor.execute(query, (new_year['academic_year'],))

            connection.commit()
            connection.close()
        except sqlite3.Error as e:
            # assume connection error or unique constraint error
            print(e)
            return jsonify(
                error = "Database connection error or unique constraint error."
            ), 500
        return jsonify(
            # identifying year by id is another option albeit vague to user
            message = f"Year {new_year['academic_year']} has been created successfully."
        )

    @staticmethod
    def update_year(year_id, new_year):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "SELECT * FROM {table} WHERE id={yearId}".format(table=Year.TABLE_NAME, yearId=year_id)

        result = cursor.execute(query)
        row = result.fetchone()
        if not row:
            # tentative as PUT request should create new if resource doesn't exist?
            return jsonify(
                error = "No year found with supplied id"
            ), 404

        query = "UPDATE {table} SET academic_year=? WHERE id={yearId}".format(table=Year.TABLE_NAME, yearId=year_id)
        cursor.execute(query, (new_year['academic_year'],))

        connection.commit()
        connection.close()

        return jsonify (
            message = f"Year {new_year['academic_year']} successfully updated"
        ), 201

    @staticmethod
    def delete_year(year_id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        
        query = "SELECT * FROM {table} WHERE id={yearId}".format(table=Year.TABLE_NAME, yearId=year_id)
        result = cursor.execute(query)

        row = result.fetchone()
        print(row)
        if not row:
            return jsonify(
                error = "No year found with supplied id"
            )
        
        query = "DELETE FROM {table} WHERE id=?".format(table=Year.TABLE_NAME)
        cursor.execute(query, (year_id,))

        connection.commit()
        connection.close()
        return jsonify(
          # vague message e.g. Year 1
            message = f"Year {year_id} successfully deleted."
        ), 200