import vertica_python

conn_info = {'host': '192.168.154.129',
             'port': 5433,
             'user': 'dbadmin',
             'password': 'password',
             'database': 'VMart',
             'ssl': False,
             'connection_timeout': 5}

connection = vertica_python.connect(**conn_info)

cur = connection.cursor()
with open("complete-dump.json", "rb") as fs:
    my_file = fs.read().decode('utf-8')
    cur.copy("COPY json FROM STDIN parser fjsonparser(flatten_maps=false)", my_file)
    connection.commit()

cur.execute("SELECT MAPTOSTRING(__raw__) FROM big_data_system_design")

for row in cur.iterate():
    dict = dict(row)
    print(type(dict))
connection.close()