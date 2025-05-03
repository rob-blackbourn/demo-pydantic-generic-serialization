import json
import importlib

from pydantic import BaseModel, ValidationInfo


def serialize_model_to_dict(model: BaseModel) -> dict:
    dct = model.model_dump(mode='json')
    dct['__module__'] = model.__class__.__module__
    dct['__qualname__'] = model.__class__.__qualname__
    return dct


def serialize_model(model: BaseModel) -> dict:
    return serialize_model_to_dict(model)


def serialize_model_to_json_str(model: BaseModel) -> str:
    dct = serialize_model_to_dict(model)
    return json.dumps(dct)


def serialize_model_to_json_bytes(model: BaseModel) -> bytes:
    text = serialize_model_to_json_str(model)
    return text.encode('utf-8')


def deserialize_model_from_dict(dct: dict) -> BaseModel:
    module = dct.pop('__module__')
    qualname = dct.pop('__qualname__')
    cls = getattr(importlib.import_module(module), qualname)
    model = cls.model_validate(dct)
    return model


def deserialize_model_from_json(data: str | bytes | bytearray) -> BaseModel:
    dct = json.loads(data)
    model = deserialize_model_from_dict(dct)
    return model


def validate_model(value: BaseModel | dict | str | bytes | bytearray, info: ValidationInfo) -> BaseModel:

    match info.mode:

        case 'python':

            if isinstance(value, BaseModel):
                return value
            elif isinstance(value, dict):
                return deserialize_model_from_dict(value)
            else:
                raise ValueError(
                    f"unhandled type for mode {info.mode}: {type(value)}"
                )

        case 'json':

            if isinstance(value, (str, bytes, bytearray)):
                return deserialize_model_from_json(value)
            elif isinstance(value, dict):
                return deserialize_model_from_dict(value)
            else:
                raise ValueError(
                    f"unhandled type for mode {info.mode}: {type(value)}"
                )

        case _:

            raise ValueError(f"Invalid mode: {info.mode}")
