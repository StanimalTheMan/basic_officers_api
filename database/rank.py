import sqlite3
from flask import jsonify

class Rank():
    TABLE_NAME = 'ranks'

    def __init__(self, _id, officer_rank):
        self.id = _id
        self.officer_rank = officer_rank

    def json(self):
        return {
            "id": self.id,
            "officer_rank": self.officer_rank
        }

    @classmethod
    def find_by_id(cls, _id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM {table} WHERE id=?".format(table=cls.TABLE_NAME)
        result = cursor.execute(query, (_id,))
        row = result.fetchone()

        if row:
            rank = cls(*row)
        else:
            rank = None 

        connection.close()
        
        return rank

class RankActions():
    
    @staticmethod
    def get_all():
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM {table}".format(table=Rank.TABLE_NAME)
        results = cursor.execute(query)

        rank_lst = []

        for row in results:
            rank_lst.append({
                                'id': row[0],
                                'officer_rank': row[1]
                            })

        connection.close()

        if rank_lst:
            return jsonify(
                officer_ranks = rank_lst
            )
        return jsonify(
            message = "No ranks found"
        )

    @staticmethod
    def post(new_rank):
        try:
            # probably can isolate db connection into separate try except
            connection = sqlite3.connect('data.db')
            cursor = connection.cursor()

            query = "INSERT INTO {table} VALUES (NULL, ?)".format(table=Rank.TABLE_NAME)
            cursor.execute(query, (new_rank['officer_rank'],))

            connection.commit()
            connection.close()
        except sqlite3.Error as e:
            # assume connection error
            # print(e)
            return jsonify(
                error = "Database connection error."
            ), 500
        return jsonify(
            # identifying rank by id is another option albeit vague to user
            message = f"Rank {new_rank['officer_rank']} has been created successfully."
        )

    @staticmethod
    def update_rank(rank_id, new_rank):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "SELECT * FROM {table} WHERE id={rankId}".format(table=Rank.TABLE_NAME, rankId=rank_id)

        result = cursor.execute(query)
        row = result.fetchone()
        if not row:
            # tentative as PUT request should create new if resource doesn't exist?
            return jsonify(
                error = "No rank found with supplied id"
            ), 404

        query = "UPDATE {table} SET  officer_rank=? WHERE id={rankId}".format(table=Rank.TABLE_NAME, rankId=rank_id)
        cursor.execute(query, (new_rank['officer_rank'],))

        connection.commit()
        connection.close()

        return jsonify (
            message = f"Rank {rank_id} successfully updated"
        ), 201

    @staticmethod
    def delete_rank(rank_id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        
        query = "SELECT * FROM {table} WHERE id={rankId}".format(table=Rank.TABLE_NAME, rankId=rank_id)
        result = cursor.execute(query)

        row = result.fetchone()
        print(row)
        if not row:
            return jsonify(
                error = "No rank found with supplied id"
            )
        
        query = "DELETE FROM {table} WHERE id=?".format(table=Rank.TABLE_NAME)
        cursor.execute(query, (rank_id,))

        connection.commit()
        connection.close()
        return jsonify(
            message = f"Rank {rank_id} successfully deleted."
        ), 200