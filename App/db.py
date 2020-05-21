from django.db import connection

def test_db():
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM node_report_202005")
        row = cursor.fetchall()
    return row

def save_data(year_month, value):
    if check_table_exist(tablename=('report_%s' % (year_month))):
        with connection.cursor() as cursor:
            query = 'insert into report_%s (ip, domain, query, response_time, datetime) value %s;' % (year_month, value)
            # print(query)
            cursor.execute(query)


def check_table_exist(tablename):
    with connection.cursor() as cursor:
        query = 'SELECT * FROM information_schema.tables WHERE table_name = "%s" and not table_schema like "%%backup"' % tablename
        cursor.execute(query)
        return True if len(cursor.fetchall()) == 1 else False