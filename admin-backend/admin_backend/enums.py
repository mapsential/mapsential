from enum import Enum


class LocationType(str, Enum):
    SOUP_KITCHEN = "soup_kitchen"
    TOILET = "toilet"
    water_fountain = "water_fountain"


class YesNoLimited(str, Enum):
    YES = "yes"
    NO = "no"
    LIMITED = "limited"


class HandDryingMethod(str, Enum):
    ELECTRIC_HAND_DRYER = "electric_hand_dryer"
    PAPER_TOWEL = "paper_towel"
    TOWEL = "towel"
