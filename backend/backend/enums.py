from enum import Enum


class LocationType(str, Enum):
    DEFIBRILLATOR = "defibrillator"
    DRINKING_FOUNTAIN = "drinking_fountain"
    SOUP_KITCHEN = "soup_kitchen"
    TOILET = "toilet"


class YesNoLimited(str, Enum):
    YES = "yes"
    NO = "no"
    LIMITED = "limited"


class HandDryingMethod(str, Enum):
    ELECTRIC_HAND_DRYER = "electric_hand_dryer"
    PAPER_TOWEL = "paper_towel"
    TOWEL = "towel"
