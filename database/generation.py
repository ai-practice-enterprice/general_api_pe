import mysql.connector
import random
from models import Package, Customer


def insert_package_data(data: list[Package]):
    """
    Insert package data into the database

    Args:
        data (Package): The parcel data to insert into the database
    """

    conn = mysql.connector.connect(
        host="localhost",
        user="admin",
        password="admin",
        database="bluesky warehouse",
    )
    cursor = conn.cursor()

    for package in data:
        cursor.execute(
            "INSERT INTO customers (name, age, email, address, city) VALUES (%s, %s, %s, %s, %s)",
            (package.customer.name, package.customer.age, package.customer.email, package.customer.address, package.customer.city),
        )
        customer_id = cursor.lastrowid

        cursor.execute(
            "INSERT INTO packages (customer_id, weight, destination_address, status, dimension) VALUES (%s, %s, %s, %s, %s)",
            (customer_id, package.weight, package.destination_address, package.status, package.dimension),
        )

    conn.commit()
    cursor.close()
    conn.close()


def get_data_for_order(package_id: int) -> dict | None:
    """
    Get package data for a specific order

    Args:
        package_id (int): The package ID to retrieve data for

    Returns:
        (dict | None): The package data for the specified order
    """
    conn = mysql.connector.connect(
        host="localhost",
        user="admin",
        password="admin",
        database="bluesky warehouse",
    )

    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT * FROM packages JOIN customers ON packages.customer_id = customers.customer_id WHERE packages.package_id = %s",
        (package_id,),
    )
    data = cursor.fetchone()

    cursor.close()
    conn.close()

    return data # type: ignore


def insert_order_data(data: dict):
    """
    Insert order data into the database

    Args:
        data (dict): The order data to insert into the database

    Returns:
        None
    """

    conn = mysql.connector.connect(
        host="localhost",
        user="admin",
        password="admin",
        database="bluesky warehouse",
    )

    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO orders (customer_id, destination, load_out_zone_id, storage_location_id) VALUES (%s, %s, %s, %s)",
        (data["customer_id"], data["destination_address"], 1, 1),
    )

    conn.commit()
    cursor.close()
    conn.close()