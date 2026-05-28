from pydantic import ValidationInfo, field_validator


def validate_string(field_name: str):
    @field_validator(field_name)
    @classmethod
    def _validator(cls, value: str, info: ValidationInfo) -> str:
        value = value.strip()
        if not value:
            raise ValueError(f"{info.field_name} cannot be empty")
        if len(value) > 200:
            raise ValueError(
                f"`{info.field_name}` cannot be longer than 200 characters"
            )
        return value
    return _validator
