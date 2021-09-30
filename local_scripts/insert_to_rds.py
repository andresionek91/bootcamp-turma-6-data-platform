import psycopg2
from datetime import datetime
from random import choice
import time
import uuid

from faker import Faker

faker_instance = Faker(["en_US"])
lat, lng, region, country, timezone = faker_instance.location_on_land()
print(lat, lng, region, country, timezone)


dsn = (
    "dbname={dbname} "
    "user={user} "
    "password={password} "
    "port={port} "
    "host={host} ".format(
        dbname="orders",
        user="postgres",
        password="r3v0phD9S-PT,-kjn0vmb=fPv76Z2-",
        port=5432,
        host="rds-production-orders-db.cdbhrilkwhra.us-east-1.rds.amazonaws.com",
    )
)

conn = psycopg2.connect(dsn)
print("connected")
conn.set_session(autocommit=True)
cur = conn.cursor()
cur.execute(
    """
    create table if not exists customers(
        created_at timestamp,
        updated_at timestamp,
        customer_id uuid PRIMARY KEY,
        name varchar(200),
        city varchar(200),
        state varchar(200),
        country varchar(200),
        lat float,
        lon float,
        email varchar(80),
        phone varchar(30)
    );
    """
)

cur.execute(
    "create table if not exists orders("
    "created_at timestamp,"
    "order_id varchar(100),"
    "product_name varchar(100),"
    "value float);"
)

products = {
    "casa": 500000.00,
    "carro": 69900.00,
    "moto": 7900.00,
    "caminhao": 230000.00,
    "laranja": 0.5,
    "borracha": 0.3,
    "iphone": 1000000.00,
}


while True:
    order_id = uuid.uuid4()
    created_at = datetime.now().isoformat()
    product_name, value = choice(list(products.items()))
    cur.execute(
        f"insert into orders values ('{created_at}', '{order_id}', '{product_name}', {value})"
    )
    print(
        f"insert into orders values ('{created_at}', '{order_id}', '{product_name}', {value})"
    )
    time.sleep(0.2)
