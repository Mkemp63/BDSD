import vertica_python

conn_info = {'host': '192.168.154.129',
             'port': 5433,
             'user': 'dbadmin',
             'password': 'password',
             'database': 'VMart',
             'SSL': False,
             'connection_timeout': 5}
connection = vertica_python.connect(**conn_info)

cur = connection.cursor()

cur.execute("INSERT INTO big_data_system_desgin VALUES(" + response.json() + ")")

cur.execute("SELECT MAPTOSTRING(__raw__) FROM big_data_system_design")
# get all content from db

# throw in list

# match new file to list
