from .core import get_db

from models import Package


def insert_package_data(data: list[Package]):
    """
    Insert package data into the database

    Args:
        data (Package): The parcel data to insert into the database
    """

    with get_db(commit=True) as cursor:
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


def get_data_for_order(package_id: int) -> dict | None:
    """
    Get package data for a specific order

    Args:
        package_id (int): The package ID to retrieve data for

    Returns:
        (dict | None): The package data for the specified order
    """

    with get_db() as cursor:
        cursor.execute(
            "SELECT * FROM packages JOIN customers ON packages.customer_id = customers.customer_id WHERE packages.package_id = %s",
            (package_id,),
        )
        data = cursor.fetchone()

    return data # type: ignore


def insert_order_data(data: dict):
    """
    Insert order data into the database

    Args:
        data (dict): The order data to insert into the database

    Returns:
        None
    """

    with get_db(commit=True) as cursor:
        cursor.execute(
            "INSERT INTO orders (customer_id, destination, load_out_zone_id, storage_location_id) VALUES (%s, %s, %s, %s)",
            (data["customer_id"], data["destination_address"], 1, 1),
        )
