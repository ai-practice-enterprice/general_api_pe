import random
import httpx

from models import Package
from database.generation import insert_package_data, get_data_for_order, insert_order_data
from utils.qrcodes import generate_qr_code_b64, decode_qr_code_b64


def push_fake_data_to_db(number_of_records: int):
    response = httpx.get(f"http://localhost:8000/fake/packages?limit={number_of_records}")
    response.raise_for_status()

    data = response.json()
    parsed_data = [Package(**record) for record in data]
    insert_package_data(parsed_data)


if __name__ == "__main__":
    # push_fake_data_to_db(20)
    rand = random.randint(1, 100)
    qrcode = generate_qr_code_b64(str(rand))
    parsed_data = decode_qr_code_b64(qrcode)

    order = get_data_for_order(int(parsed_data))
    if order:
        insert_order_data(order)
    else:
        print("Order not found")