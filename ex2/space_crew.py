from datetime import datetime
from enum import Enum

try:
    from pydantic import BaseModel, Field, ValidationError, model_validator
except ImportError:
    print("pydantic is not installed. Please install it to run this code.")


class Rank(Enum):
    CADET = "cadet"
    OFFICER = "officer"
    LIEUTENANT = "lieutenant"
    CAPTAIN = "captain"
    COMMANDER = "commander"


class CrewMember(BaseModel):
    member_id: str = Field(
                ...,
                min_length=3,
                max_length=10,
                description="Unique identifier for the crew member")
    name: str = Field(
                ...,
                min_length=2,
                max_length=50,
                description="Name of the crew member")
    rank: Rank = Field(
                ...,
                description="Rank of the crew member")
    age: int = Field(
                ...,
                ge=18,
                le=80,
                description="Age of the crew member")
    specialization: str = Field(
                ...,
                min_length=3,
                max_length=30,
                description="Specialization of the crew member")
    years_experience: int = Field(
                ...,
                ge=0,
                le=50,
                description="Years of experience of the crew member")
    is_active: bool = Field(
                True,
                description="Whether the crew member is currently active")


class SpaceMission(BaseModel):
    mission_id: str = Field(
                ...,
                min_length=5,
                max_length=15,
                description="Unique identifier for the mission")
    mission_name: str = Field(
                ...,
                min_length=3,
                max_length=100,
                description="Name of the mission")
    destination: str = Field(
                ...,
                min_length=3,
                max_length=50,
                description="Destination of the mission")
    launch_date: datetime = Field(
                ...,
                description="Launch date of the mission")
    duration_days: int = Field(
                ...,
                ge=1,
                le=3650,
                description="Duration of the mission in days")
    crew_members: list[CrewMember] = Field(
                ...,
                min_length=1,
                max_length=12,
                description="List of crew members assigned to the mission")
    mission_status: str = Field(
                "planned",
                min_length=3,
                max_length=20,
                description="Status of the mission")
    budget_million: float = Field(
                ...,
                ge=1.0,
                le=10000.0,
                description="Budget of the mission in million dollars")

    @model_validator(mode="after")
    def check(self) -> "SpaceMission":
        exp_years = sum(_.years_experience for _ in self.crew_members)
        duration_years = self.duration_days / 365
        active_list = [member.is_active for member in self.crew_members]
        if not self.mission_id.startswith("M"):
            raise ValueError("Mission ID must start with 'M'")
        if (not any(member.rank in (Rank.COMMANDER, Rank.CAPTAIN) for member in
                    self.crew_members)):
            raise ValueError("Mission must have at least one Commander "
                             "or Captain")
        if (duration_years >= 1 and exp_years < duration_years / 2):
            raise ValueError("Long missions require more experienced"
                             " crew members")
        if not all(active_list):
            raise ValueError("Active crew members must have a "
                             "pilot specialization")
        return self


def main() -> None:
    print("Space Mission Crew Validation")
    print("=" * 41)

    try:
        valid_mission = SpaceMission(
            mission_id="M2024_MARS",
            mission_name="Mars Colony Establishment",
            destination="Mars",
            launch_date=datetime(2026, 7, 15, 9, 0),
            duration_days=900,
            budget_million=2500.0,
            crew_members=[
                CrewMember(
                    member_id="CM001",
                    name="Sarah Connor",
                    rank=Rank.COMMANDER,
                    age=42,
                    specialization="Mission Command",
                    years_experience=20,
                    is_active=True,
                ),
                CrewMember(
                    member_id="CM002",
                    name="John Smith",
                    rank=Rank.LIEUTENANT,
                    age=35,
                    specialization="Navigation",
                    years_experience=15,
                    is_active=True,
                ),
                CrewMember(
                    member_id="CM003",
                    name="Alice Johnson",
                    rank=Rank.OFFICER,
                    age=31,
                    specialization="Engineering",
                    years_experience=15,
                    is_active=True,
                ),
            ],
            mission_status="planned",
        )
        print("Valid mission created:")
        print(f"Mission: {valid_mission.mission_name}")
        print(f"ID: {valid_mission.mission_id}")
        print(f"Destination: {valid_mission.destination}")
        print(f"Duration: {valid_mission.duration_days} days")
        print(f"Budget: ${valid_mission.budget_million}M")
        print(f"Crew size: {len(valid_mission.crew_members)}")
        print("Crew members:")
        for member in valid_mission.crew_members:
            print(f" - {member.name} ({member.rank.value}, "
                  f"{member.specialization}, ")
    except ValidationError as e:
        print("Expected validation error:")
        for err in e.errors():
            message = err.get("msg", "Unknown validation error")
            if "value error" in message.lower() and "," in message:
                _, clean_message = message.split(",", 1)
                print(clean_message.strip())
            else:
                print(message)

    print("\n" + "=" * 41)

    try:
        SpaceMission(
            mission_id="M2024_MARS",
            mission_name="Mars Colony Establishment",
            destination="Mars",
            launch_date=datetime(2026, 7, 15, 9, 0),
            duration_days=900,
            budget_million=2500.0,
            crew_members=[
                CrewMember(
                    member_id="CM010",
                    name="John Smith",
                    rank=Rank.LIEUTENANT,
                    age=35,
                    specialization="Navigation",
                    years_experience=12,
                    is_active=True,
                ),
                CrewMember(
                    member_id="CM011",
                    name="Alice Johnson",
                    rank=Rank.OFFICER,
                    age=31,
                    specialization="Engineering",
                    years_experience=10,
                    is_active=True,
                ),
            ],
            mission_status="planned",
        )

    except ValidationError as e:
        print("Expected validation error:")
        for err in e.errors():
            message = err.get("msg", "Unknown validation error")
            if "value error" in message.lower() and "," in message:
                _, clean_message = message.split(",", 1)
                print(clean_message.strip())
            else:
                print(message)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("An unexpected error occurred:", e)
