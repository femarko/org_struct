from enum import StrEnum


class DeletionMode(StrEnum):
    CASCADE = "cascade"
    REASSIGN = "reassign"