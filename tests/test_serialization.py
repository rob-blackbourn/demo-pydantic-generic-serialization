from datetime import datetime
from decimal import Decimal

from demo.models import User, Location, Update
from demo.serialization import (
    serialize_model_to_json_str,
    deserialize_model_from_json
)


def test_serialization() -> None:

    user = User(
        name='John Doe',
        date_of_birth=datetime(1990, 1, 1),
        height=1.75
    )
    location = Location(
        name='Central Park',
        latitude=Decimal('40.785091'),
        longitude=Decimal('-73.968285')
    )

    user_json_str = serialize_model_to_json_str(user)
    deserialized_user = deserialize_model_from_json(user_json_str)
    assert user == deserialized_user

    location_json_str = serialize_model_to_json_str(location)
    deserialized_location = deserialize_model_from_json(location_json_str)
    assert location == deserialized_location

    update = Update(model=user)
    update_json_str = serialize_model_to_json_str(update)
    deserialized_update = deserialize_model_from_json(update_json_str)
    assert update == deserialized_update


def test_model() -> None:
    user = User(
        name='John Doe',
        date_of_birth=datetime(1990, 1, 1),
        height=1.75
    )
    location = Location(
        name='Central Park',
        latitude=Decimal('40.785091'),
        longitude=Decimal('-73.968285')
    )

    user_json_str = user.model_dump_json()
    deserialized_user = User.model_validate_json(user_json_str)
    assert user == deserialized_user

    location_json_str = location.model_dump_json()
    deserialized_location = Location.model_validate_json(location_json_str)
    assert location == deserialized_location

    update = Update(model=user)
    update_json_str = update.model_dump_json()
    deserialized_update = Update.model_validate_json(update_json_str)
    assert update == deserialized_update
