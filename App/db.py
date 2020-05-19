from django.db import connection

def test_db():
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM node_report_202005")
        row = cursor.fetchall()

    return row