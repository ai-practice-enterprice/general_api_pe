import logging
from fastapi import APIRouter, Query
from faker import Faker
from faker.config import AVAILABLE_LOCALES
from enum import Enum
from typing import Annotated

from models import Customer, Parcel


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

    fake = Faker(locale)

    log.info(f"Generating {limit} fake customers with locale {locale}")

    return [
        Customer(
            name=fake.name(),
            age=fake.random_int(min=18, max=100),
            email=fake.email(),
            address=fake.address(),
            phone=fake.phone_number(),
        )
        for _ in range(limit)
    ]


@router.get("/parcels", response_model=list[Parcel])
async def get_fake_parcel_data(
    limit: Annotated[int, Query(ge=1, le=100)] = 1,
    locale: Annotated[AvailableLocales, Query()] = AvailableLocales.nl_BE,  # type: ignore
):
    """
    Get fake data for testing purposes based on the provided limit and locale.
    """

    fake = Faker(locale)

    log.info(f"Generating {limit} fake parcels with locale {locale}")

    return [
        Parcel(
            customer=Customer(
                name=fake.name(),
                age=fake.random_int(min=18, max=100),
                email=fake.email(),
                address=fake.address(),
                phone=fake.phone_number(),
            ),
            tracking_number=fake.random_int(min=10, max=10_000),
            weight=fake.random_int(min=1, max=1000) + fake.random_int(min=0, max=100) / 100,
            destination=fake.address(),
            recipient=fake.name(),
        )
        for _ in range(limit)
    ]
