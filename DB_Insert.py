import os

import vertica_python


def connect_to_db():
    conn_info = {'host': '192.168.154.129',
                 'port': 5433,
                 'user': 'dbadmin',
                 'password': 'password',
                 'database': 'VMart',
                 'ssl': False,
                 'connection_timeout': 5}

    connection = vertica_python.connect(**conn_info)
    return connection


def insert(connection, filename):
    cur = connection.cursor()
    with open(filename, "rb") as fs:
        my_file = fs.read().decode('utf-8')
        cur.copy("COPY big_data_system_design FROM STDIN parser fjsonparser(flatten_maps=false, flatten_arrays=true)",
                 my_file)
        connection.commit()
    remove_file(filename)

def remove_file(filename):
    if os.path.exists(filename):
        os.remove(filename)
    else:
        print("Can not delete the file, as it doesn't exist")

def select(connection):
    cur = connection.cursor()
    cur.execute("select content, title, maptostring(keywords) from big_data_system_design")
    results = []
    for row in cur.fetchall():
        results.append(row)
    return results


def selectsearch(connection, searchKey):
    cur = connection.cursor()
    cur.execute("select content, title, regexp_count(maptostring(keywords), '"+searchKey+"') as 'keywordscount', regexp_count(content, '"+searchKey+"') as 'contentcount', regexp_count(title, '"+searchKey+"') as 'titlecount' from big_data_system_design where regexp_count(maptostring(keywords), '"+searchKey+"') > 0 or regexp_count(content, '"+searchKey+"') > 0 or regexp_count(title, '"+searchKey+"') > 0 order by regexp_count(maptostring(keywords), '"+searchKey+"') desc, regexp_count(title, '"+searchKey+"') desc, regexp_count(content, '"+searchKey+"') desc limit 10")
    results = []
    for row in cur.fetchall():
        results.append(row)
    return results


def main():
    conn = connect_to_db()
    # for json file:
    path = os.getcwd()
    for i in os.listdir(path):
        if os.path.isfile(os.path.join(path, i)) and 'partij-' in i:
            insert(conn, i)
    conn.close()


if __name__ == '__main__':
    main()
