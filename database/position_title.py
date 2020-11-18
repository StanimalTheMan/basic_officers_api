import sqlite3
from flask import jsonify

class PositionTitle():
    TABLE_NAME = 'position_titles'

    def __init__(self, _id, officer_position_title):
        self.id = _id
        self.officer_position_title = officer_position_title

    def json(self):
        return {
            "id": self.id,
            "officer_position_title": self.officer_position_title
        }

    @classmethod
    def find_by_id(cls, _id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM {table} WHERE id=?".format(table=cls.TABLE_NAME)
        result = cursor.execute(query, (_id,))
        row = result.fetchone()

        if row:
            position_title = cls(*row)
        else:
            position_title = None 

        connection.close()
        
        return position_title

class PositionTitleActions():
    
    @staticmethod
    def get_all():
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM {table}".format(table=PositionTitle.TABLE_NAME)
        results = cursor.execute(query)

        pos_titles_lst = []

        for row in results:
            pos_titles_lst.append({
                                'id': row[0],
                                'officer_position_title': row[1]
                            })

        connection.close()

        if pos_titles_lst:
            return jsonify(
                officer_position_titles = pos_titles_lst
            )
        return jsonify(
            message = "No position titles found"
        )

    @staticmethod
    def post(new_position_title):
        try:
            # probably can isolate db connection into separate try except
            connection = sqlite3.connect('data.db')
            cursor = connection.cursor()

            query = "INSERT INTO {table} VALUES (NULL, ?)".format(table=PositionTitle.TABLE_NAME)
            print(query)
            cursor.execute(query, (new_position_title['officer_position_title'],))
            print("POST CURSOR EXECUTE")

            connection.commit()
            connection.close()
        except sqlite3.Error as e:
            # assume connection error
            # print(e)
            return jsonify(
                error = "Database connection error."
            ), 500
        return jsonify(
            # identifying position title by id is another option albeit vague to user
            message = f"Position Title {new_position_title['officer_position_title']} has been created successfully."
        )

    @staticmethod
    def update_position_title(position_title_id, new_position_title):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "SELECT * FROM {table} WHERE id={positionTitleId}".format(table=PositionTitle.TABLE_NAME, positionTitleId=position_title_id)

        result = cursor.execute(query)
        row = result.fetchone()
        if not row:
            # tentative as PUT request should create new if resource doesn't exist?
            return jsonify(
                error = "No position title found with supplied id"
            ), 404

        query = "UPDATE {table} SET  officer_position_title=? WHERE id={positionTitleId}".format(table=PositionTitle.TABLE_NAME, positionTitleId=position_title_id)
        cursor.execute(query, (new_position_title['officer_position_title'],))

        connection.commit()
        connection.close()

        return jsonify (
            message = f"Position Title {position_title_id} successfully updated"
        ), 201

    @staticmethod
    def delete_position_title(position_title_id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        
        query = "SELECT * FROM {table} WHERE id={positionTitleId}".format(table=PositionTitle.TABLE_NAME, positionTitleId=position_title_id)
        result = cursor.execute(query)

        row = result.fetchone()
        print(row)
        if not row:
            return jsonify(
                error = "No position title found with supplied id"
            )
        
        query = "DELETE FROM {table} WHERE id=?".format(table=PositionTitle.TABLE_NAME)
        cursor.execute(query, (position_title_id,))

        connection.commit()
        connection.close()
        return jsonify(
            message = f"Position Title {position_title_id} successfully deleted."
        ), 200