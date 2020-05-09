import psycopg2

con = psycopg2.connect(
    host = "localhost",
    database="postgres",
    user = "postgres",
    password = "karolina13")

cur = con.cursor()

cur.execute("select * from buty")

rows = cur.fetchall()

for r in rows:
    print (f" id {r[0]} name {r[1]}")

cur.close()