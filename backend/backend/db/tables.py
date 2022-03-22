from enums import HandDryingMethod
from enums import LocationType
from enums import YesNoLimited
from piccolo.columns import Boolean
from piccolo.columns import ForeignKey
from piccolo.columns import Numeric
from piccolo.columns import Real
from piccolo.columns import Text
from piccolo.columns import Timestamp
from piccolo.columns import Varchar
from piccolo.table import Table

class Details(Table):

    # General columns
    name = Varchar(length=255, null=False, default=None)
    operator = Varchar(null=True, default=None)
    opening_times = Varchar(null=True, default=None)

    address = Varchar(null=True, default=None)
    street = Varchar(null=True, default=None)
    district = Varchar(null=True, default=None)
    town = Varchar(null=True, default=None)
    city = Varchar(null=True, default=None)
    state = Varchar(null=True, default=None)
    # Stored as varchar because postal codes starting with 0 could cause
    # unexpected bugs if they were handled as integers.
    postcode = Varchar(length=5, null=True, default=None)
    country = Varchar(null=True, default=None)
    country_code = Varchar(length=2, null=True, default=None)

    has_fee = Boolean(null=True, default=None)
    fee = Numeric(
        # Stores dd.dd
        # This will cause a problem if there are toilets that charge more that 99 Euro.
        # I don't think that will be a problem.
        digits=(4, 2),
        null=True,
        default=None
    ),
    is_customer_only = Boolean(null=True, default=None)

    female = Boolean(null=True, default=None)
    male = Boolean(null=True, default=None)
    unisex = Boolean(null=True, default=None)
    child = Boolean(null=True, default=None)

    has_seated = Boolean(null=True, default=None)
    has_urinal = Boolean(null=True, default=None)
    has_squat = Boolean(null=True, default=None)

    change_table = Varchar(length=31, choices=YesNoLimited, null=True, default=None)

    wheelchair_accessible = Varchar(length=31, choices=YesNoLimited, null=True, default=None)
    wheelchair_access_info = Text(null=True, default=None)

    has_hand_washing = Boolean(null=True, default=None)
    has_soap = Boolean(null=True, default=None)
    has_hand_disinfectant = Boolean(null=True, default=None)
    has_hand_creme = Boolean(null=True, default=None)
    has_hand_drying = Boolean(null=True, default=None)
    hand_drying_method = Varchar(length=31, choices=HandDryingMethod, null=True, default=None)
    has_paper = Boolean(null=True, default=None)
    has_hot_water = Boolean(null=True, default=None)
    has_shower = Boolean(null=True, default=None)
    has_drinking_water = Boolean(null=True, default=None)

    # Location type specific columns
    soup_kitchen_info = Text(null=True, default=None)


class Locations(Table):
    details_id = ForeignKey(references=Details)

    type = Varchar(length=127, choices=LocationType)
    latitude = Real(null=True, default=None)
    longitude = Real(null=True, default=None)


class Comments(Table):
    location_id = ForeignKey(references=Locations)

    author_name = Varchar(length=255)
    content = Text()
    timestamp = Timestamp()


class Captcha(Table):
    token = Varchar(length=255)
    answer = Varchar(length=255)
