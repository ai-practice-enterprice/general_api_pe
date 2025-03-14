import logging
import random
from enum import Enum
from datetime import datetime , timedelta
from fastapi import APIRouter, Query
from typing import Annotated

from faker import Faker
from faker.config import AVAILABLE_LOCALES
from faker_airtravel import AirTravelProvider 
from faker.providers import BaseProvider

# available fake models ==========================================================================
# based upon the AD team's ERD 
from models import (
    Customer,
    Package,
    Address,
    Airline,
    Airplane,
    Airport,
    City,
    Contract,
    Country,
    Employee,
    Flight,
    Job,
    Location,
    PackageMovement,
    Payroll,
    User,
    Vacation,
    Work,
    Worker
)

# Faker configuration (providers) ==========================================================================
# ...


# API endpoints setup ==========================================================================

router = APIRouter(prefix="/fake", tags=["Fake Data"])
AvailableLocales = Enum("AvailableLocales", {loc: loc for loc in AVAILABLE_LOCALES})
log = logging.getLogger(__name__)

# API endpoints for fake data ==========================================================================

@router.get("/customers", response_model=list[Customer])
def get_fake_customer_data(
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
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            email=fake.email(),
            phone_number=fake.phone_number(),
        )
        for _ in range(limit)
    ]

# ===========================================================================
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
            reference=fake.random_letters(32),
            dimension=f"{fake.random_int(min=1, max=100)}x{fake.random_int(min=1, max=100)}x{fake.random_int(min=1, max=100)}",
            status=random.choice(["pending", "in_transit", "delivered"]),
            name=fake.first_name(),
            lastname=fake.last_name(),
            receiverEmail=fake.email(),
            receiver_phone_number=fake.phone_number(),
        )
        for _ in range(limit)
    ]

# ===========================================================================
@router.get("/locations", response_model=list[Location])
def get_fake_location_data(
    limit: Annotated[int, Query(ge=1, le=100)] = 1,
    locale: Annotated[AvailableLocales, Query()] = AvailableLocales.nl_BE,  # type: ignore
):
    """
    Get fake data for testing purposes based on the provided limit and locale.
    """

    fake = Faker(locale.value)

    log.info(f"Generating {limit} fake locations with locale {locale}")

    locationNames = Enum("pickup point","distribution center","airport")

    return [
        Location(
            name=fake.random_company_acronym(),
            location_type=fake.enum(locationNames),
            contact_number=fake.phone_number(),
            opening_hours=str(fake.random_int(min=6,max=12) + "AM - " + fake.random_int(min=1,max=9) + "PM") 
        )
        for _ in range(limit)
    ]

# ===========================================================================
@router.get("/flights", response_model=list[Flight])
def get_fake_flight_data(
    limit: Annotated[int, Query(ge=1, le=100)] = 1,
    locale: Annotated[AvailableLocales, Query()] = AvailableLocales.nl_BE,  # type: ignore
):
    """
    Get fake data for testing purposes based on the provided limit and locale.
    """

    fake = Faker(locale.value)

    log.info(f"Generating {limit} fake flights with locale {locale}")

    statusFlight = Enum("departed","arrived","underway")

    listFakeFlightData: list[Flight] = list()

    for _ in range(limit):
        today = datetime.today()
        departureDate = fake.date_this_year()
        statusCurrentFlight = fake.enum(statusFlight)

        if statusCurrentFlight == "departed":
            arrivalDate = fake.date_between_dates(
                date_start=today,
                date_end=departureDate + timedelta(days=fake.random_int(0,3))
            )
        elif statusCurrentFlight == "arrived":
            arrivalDate = fake.date_between_dates(
                date_start=departureDate,
                date_end=today
            )
        elif statusCurrentFlight == "underway":
            arrivalDate = departureDate + timedelta(
                days=fake.random_int(0,3),
                hours=(abs(random.random) % 24)
            )
            pass
        
        
        listFakeFlightData.append(
            Flight(
                departure_time=departureDate,
                arrival_time=arrivalDate,
                status=statusCurrentFlight,
            )
        )

    return 

# ===========================================================================
@router.get("/cities", response_model=list[City])
def get_fake_location_data(
    limit: Annotated[int, Query(ge=1, le=100)] = 1,
    locale: Annotated[AvailableLocales, Query()] = AvailableLocales.nl_BE,  # type: ignore
):
    """
    Get fake data for testing purposes based on the provided limit and locale.
    """

    fake = Faker(locale.value)

    log.info(f"Generating {limit} fake cities with locale {locale}")

    return [
        City(
            name=fake.city_name(),
            postcode=fake.postal_code()
        )
        for _ in range(limit)
    ]

# ===========================================================================
@router.get("/airplanes", response_model=list[Airplane])
def get_fake_location_data(
    limit: Annotated[int, Query(ge=1, le=100)] = 1,
    locale: Annotated[AvailableLocales, Query()] = AvailableLocales.nl_BE,  # type: ignore
):
    """
    Get fake data for testing purposes based on the provided limit and locale.
    """

    fake = Faker(locale=locale.value,providers=["AirTravelProvider"])
    

    log.info(f"Generating {limit} fake airplanes with locale {locale}")

    return [
        Airplane(
            model=fake.flight()["iata"],
            capacity=fake.random_int(15,600),
            status="",
        )
        for _ in range(limit)
    ]
# ===========================================================================
@router.get("/airports", response_model=list[Airport])
def get_fake_location_data(
    limit: Annotated[int, Query(ge=1, le=100)] = 1,
    locale: Annotated[AvailableLocales, Query()] = AvailableLocales.nl_BE,  # type: ignore
):
    """
    Get fake data for testing purposes based on the provided limit and locale.
    """

    # NOTE : I can't seem to add providers for some reason
    # fake = Faker(locale=locale.value,providers=["AirTravelProvider"])
    

    log.info(f"Generating {limit} fake airports with locale {locale}")

    return [
        Airport(
            name="fake.airport_name()"
        )
        for _ in range(limit)
    ]

# ===========================================================================
@router.get("/airlines", response_model=list[Airline])
def get_fake_location_data(
    limit: Annotated[int, Query(ge=1, le=100)] = 1,
    locale: Annotated[AvailableLocales, Query()] = AvailableLocales.nl_BE,  # type: ignore
):
    """
    Get fake data for testing purposes based on the provided limit and locale.
    """

    fake = Faker(locale=locale.value)
    

    log.info(f"Generating {limit} fake airlines with locale {locale}")

    return [
        Airline(
            name="",
            IATA_code="",
            contact_number="",
            headquarters_location="",
        )
        for _ in range(limit)
    ]
# ===========================================================================
# ===========================================================================
# ===========================================================================
# ===========================================================================
# ===========================================================================
