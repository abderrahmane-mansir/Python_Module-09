from datetime import datetime
from enum import Enum
from typing import Optional

try:
    from pydantic import BaseModel, Field, ValidationError, model_validator
except ImportError:
    print("pydantic is not installed. Please install it to run this code.")


class ContactType(Enum):
    RADIO = "radio"
    VISUAL = "visual"
    PHYSICAL = "physical"
    TELEPATHIC = "telepathic"


class AlienContact(BaseModel):
    contact_id: str = Field(
                ...,
                min_length=5,
                max_length=15,
                description="Unique identifier for the contact")
    timestamp: datetime = Field(
                ...,
                description="Date and time of the contact")
    location: str = Field(
                ...,
                min_length=3,
                max_length=100,
                description="Location of the contact")
    contact_type: ContactType = Field(
                ...,
                description="Type of contact")
    signal_strength: float = Field(
                ...,
                ge=0.0,
                le=10.0,
                description="Strength of the signal (0-10)")
    duration_minutes: int = Field(
                ...,
                ge=1,
                le=1440,
                description="Duration of the contact in minutes")
    witness_count: int = Field(
                ...,
                ge=1,
                le=100,
                description="Number of witnesses to the contact")
    message_received: Optional[str] = Field(
                ...,
                max_length=500,
                description="Additional information about the contact")
    is_verified: bool = Field(
                False,
                description="Whether the contact is verified")

    @model_validator(mode="after")
    def check(self) -> "AlienContact":
        if not self.contact_id.startswith("AC"):
            raise ValueError("Contact ID must start with 'AC'")
        if (
            self.contact_type == ContactType.PHYSICAL
            and not self.is_verified
           ):
            raise ValueError("Physical contact needs to be verified")
        if (
            self.contact_type == ContactType.TELEPATHIC
            and self.witness_count < 3
           ):
            raise ValueError(
                "Telepathic contact must have at least 3 witnesses")
        if (
            self.signal_strength > 7.0
            and not self.message_received
           ):
            raise ValueError("Strong signals must have a message received")
        return self


def main() -> None:
    print("Alien Contact Log Validation")
    print("=" * 40)
    try:
        contact = AlienContact(
            contact_id="AC_2024_001",
            timestamp=datetime(2026, 5, 1, 14, 30),
            location="Area 51, Nevada",
            contact_type=ContactType.RADIO,
            signal_strength=8.5,
            duration_minutes=45,
            witness_count=5,
            message_received="Greetings from Zeta Reticuli",
            is_verified=True
        )
        print("Valid contact report:")
        print(f"ID: {contact.contact_id}")
        print(f"Type: {contact.contact_type.value}")
        print(f"Location: {contact.location}")
        print(f"Signal: {contact.signal_strength}/10")
        print(f"Duration: {contact.duration_minutes} minutes")
        print(f"Witnesses: {contact.witness_count}")
        print(f"Message: '{contact.message_received}'")
    except ValidationError as e:
        print("Expected validation errors:")
        for e in e.errors():
            message = e.get("msg", "Unknown validation error")
            if "value error" in message.lower() and "," in message:
                _, clean_message = message.split(",", 1)
                print(clean_message.strip())
            else:
                print(message)
    print("\n"+"=" * 40)
    try:
        invalid_contact = AlienContact(
            contact_id="AC-23456",
            timestamp=datetime(2026, 5, 1, 14, 30),
            location="Sector 7G",
            contact_type=ContactType.TELEPATHIC,
            signal_strength=8.5,
            duration_minutes=30,
            witness_count=2,
            message_received="We come in peace.",
            is_verified=False
        )
        print("Invalid contact created:")
        print(f"ID: {invalid_contact.contact_id}")
        print(f"Time: {invalid_contact.timestamp}")
        print(f"Location: {invalid_contact.location}")
        print(f"Type: {invalid_contact.contact_type.value}")
        print(f"Signal: {invalid_contact.signal_strength}/10")
        print(f"Duration: {invalid_contact.duration_minutes} minutes")
        print(f"Witnesses: {invalid_contact.witness_count}")
        print(f"Message: '{invalid_contact.message_received}'")
    except ValidationError as e:
        print("Expected validation errors:")
        for e in e.errors():
            message = e.get("msg", "Unknown validation error")
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
