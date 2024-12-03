from dataclasses import dataclass
from enum import Enum


@dataclass
class Sex(str, Enum):
    MALE = "M"
    FEMALE = "F"
    X = "X"

@dataclass
class DocumentType(str, Enum):
    PASSPORT = "passport"
    DRIVER_LICENSE = "DL"