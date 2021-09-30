import os
import random
import time

import psycopg2

dsn = (
    "dbname={dbname} "
    "user={user} "
    "password={password} "
    "port={port} "
    "host={host} ".format(
        dbname="orders",
        user="postgres",
        password=os.environ["password"],
        port=5432,
        host="rds-production-orders-db.cdbhrilkwhra.us-east-1.rds.amazonaws.com",
    )
)

conn = psycopg2.connect(dsn)
print("connected")
conn.set_session(autocommit=True)
cur = conn.cursor()


def get_update_query():
    cur.execute("select order_id from orders order by random() limit 1")
    order_id = cur.fetchone()[0]
    rand_value = random.randrange(1, 100000)
    return f"update orders set value = {rand_value} where order_id='{order_id}'"


while True:
    query = get_update_query()
    cur.execute(query)
    print(query)
    time.sleep(5)
