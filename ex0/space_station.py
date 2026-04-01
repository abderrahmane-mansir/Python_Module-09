try:
    from pydantic import BaseModel, Field, ValidationError
except ImportError:
    print("pydantic is not installed. Please install it to run this code.")
from datetime import datetime
from typing import Optional


class SpaceStation(BaseModel):
    station_id: str = Field(
                        ...,
                        min_length=3,
                        max_length=10,
                        description="Unique identifier for the space station")
    name: str = Field(
                        ...,
                        min_length=1,
                        max_length=20,
                        description="Name of the space station")
    crew_size: int = Field(
                        ...,
                        ge=1,
                        le=20,
                        description="Number of the space station crew members")
    power_level: float = Field(
                        ...,
                        ge=0.0,
                        le=100.0,
                        description="Power level of the space station")
    oxygen_level: float = Field(
                        ...,
                        ge=0.0,
                        le=100.0,
                        description="Oxygen level of the space station")
    last_maintenance_date: datetime = Field(
                        ...,
                        description="Date of the last maintenance")
    is_operational: bool = Field(
                        ...,
                        description="Operational status of the space station")
    note: Optional[str] = Field(
                        True,
                        max_length=200,
                        description="Additional notes about the space station")


def main():
    print("Space Station Data Validation")
    print("=" * 40)
    try:
        station = SpaceStation(
            station_id="SS-001",
            name="Alpha Station",
            crew_size=10,
            power_level=85.5,
            oxygen_level=90.0,
            last_maintenance_date=datetime(2026, 4, 1),
            is_operational=True,
            note="All systems are functioning properly."
        )
        print("Valid station created:")
        print(f"ID: {station.station_id}")
        print(f"Name: {station.name}")
        print(f"Crew: {station.crew_size} people")
        print(f"Power: {station.power_level}%")
        print(f"Oxygen: {station.oxygen_level}%")
        status = (
            "Operational"
            if station.is_operational
            else "Not Operational"
        )
        print(f"Status: {status}")
    except ValidationError as e:
        print("Expected validation error:")
        print(e.errors()[0]["msg"])
    print("\n"+"=" * 40)
    try:
        invalid_station = SpaceStation(
            station_id="SS-002",
            name="Beta Station",
            crew_size=25,
            power_level=100.0,
            oxygen_level=90.0,
            last_maintenance_date=datetime(2025, 12, 31),
            is_operational=False,
            note="Some systems need attention."
        )
        print("Valid station created:")
        print(f"ID: {invalid_station.station_id}")
        print(f"Name: {invalid_station.name}")
        print(f"Crew: {invalid_station.crew_size} people")
        print(f"Power: {invalid_station.power_level}%")
        print(f"Oxygen: {invalid_station.oxygen_level}%")
        status = (
            "Operational"
            if invalid_station.is_operational
            else "Not Operational"
        )
        print(f"Status: {status}")
    except ValidationError as e:
        print("Expected validation error:")
        print(e.errors()[0]["msg"])


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"An error occurred: {e}")
