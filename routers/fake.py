import logging
import random
from fastapi import APIRouter, Query
from faker import Faker
from faker.config import AVAILABLE_LOCALES
from enum import Enum
from typing import Annotated

from models import Customer, Package


router = APIRouter(prefix="/fake", tags=["Fake Data"])
AvailableLocales = Enum("AvailableLocales", {loc: loc for loc in AVAILABLE_LOCALES})
log = logging.getLogger(__name__)


@router.get("/", response_model=list[Customer])
def get_fake_data(
    limit: Annotated[int, Query(ge=1, le=100)] = 1,
    locale: Annotated[AvailableLocales, Query()] = AvailableLocales.nl_BE,  # type: ignore
):
    """
    Get fake data for testing purposes based on the provided limit and locale.
    """

    fake = Faker(locale.value)

    log.info(f"Generating {limit} fake customers with locale {locale}")

    return [
        Customer(
            name=fake.name(),
            age=fake.random_int(min=18, max=100),
            email=fake.email(),
            address=fake.address(),
            city=fake.city()
        )
        for _ in range(limit)
    ]


@router.get("/packages", response_model=list[Package])
def get_fake_parcel_data(
    limit: Annotated[int, Query(ge=1, le=100)] = 1,
    locale: Annotated[AvailableLocales, Query()] = AvailableLocales.nl_BE,  # type: ignore
):
    """
    Get fake data for testing purposes based on the provided limit and locale.
    """

    fake = Faker(locale.value)

    log.info(f"Generating {limit} fake packages with locale {locale}")

    return [
        Package(
            customer=Customer(
                name=fake.name(),
                age=fake.random_int(min=18, max=100),
                email=fake.email(),
                address=fake.address(),
                city=fake.city()
            ),
            dimension=f"{fake.random_int(min=1, max=100)}x{fake.random_int(min=1, max=100)}x{fake.random_int(min=1, max=100)}",
            status=random.choice(["pending", "in_transit", "delivered"]),
            weight=fake.random_int(min=1, max=1000) + fake.random_int(min=0, max=100) / 100,
            destination_address=fake.address()
        )
        for _ in range(limit)
    ]
