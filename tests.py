from random import randint

from conn import connections
from conn.connections import insert_row


def testing():
    query = f'''INSERT INTO team (id_team, name_team) VALUES (111, 'warriors')'''
    insert_row(query=query)
