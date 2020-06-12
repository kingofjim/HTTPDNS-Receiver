from django.db import connection

def test_db():
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM node_report_202005")
        row = cursor.fetchall()
    return row

def save_data(table_name, value, ):
    if not check_table_exist(tablename=table_name):
        create_table_report(table_name)
    with connection.cursor() as cursor:
        if table_name.find('_hqt_') > -1:
            query = 'insert into %s (ip, domain, query, response_time, datetime) value %s;' % (table_name, value)
        elif table_name.find('_ie_') > -1:
            query = 'insert into %s (ip, domain, query, response_time, device, user_agent, datetime) value %s;' % (table_name, value)
        print(query)
        cursor.execute(query)


def check_table_exist(tablename):
    with connection.cursor() as cursor:
        query = 'SELECT * FROM information_schema.tables WHERE table_name = "%s" and not table_schema like "%%backup"' % tablename
        cursor.execute(query)
        return True if len(cursor.fetchall()) == 1 else False

def create_table_report(table_name):
    with connection.cursor() as cursor:
        if table_name.find('_hqt_') > -1:
            query = "CREATE TABLE `%s` (`id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,`ip` varchar(20) NOT NULL DEFAULT '',`domain` varchar(40) NOT NULL DEFAULT '',`query` varchar(255) DEFAULT NULL,`response_time` smallint(5) unsigned NOT NULL,`datetime` datetime DEFAULT  NULL,`created_at` datetime DEFAULT CURRENT_TIMESTAMP, PRIMARY KEY (`id`)) ENGINE=InnoDB DEFAULT CHARSET=utf8;" % table_name
        elif table_name.find('_ie_') > -1:
            query = "CREATE TABLE `%s`( `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT, `ip` varchar(20) NOT NULL DEFAULT '', `domain` varchar(40) NOT NULL DEFAULT '', `query` varchar(255) DEFAULT NULL, `response_time` smallint(5) unsigned NOT NULL, `device` varchar(10) DEFAULT NULL, `user_agent` varchar(255) DEFAULT NULL, `datetime` datetime DEFAULT NULL, `created_at` datetime DEFAULT CURRENT_TIMESTAMP, PRIMARY KEY (`id`)) ENGINE=InnoDB DEFAULT CHARSET=utf8;" % table_name
        # print(query)
        cursor.execute(query)