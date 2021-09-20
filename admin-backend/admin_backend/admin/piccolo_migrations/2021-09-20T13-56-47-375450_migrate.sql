CREATE TABLE locations (
    id INTEGER PRIMARY KEY NOT NULL,
    type VARCHAR(127) NOT NULL,
    name VARCHAR(255) NOT NULL,
    name_source_id INTEGER,
    address VARCHAR NOT NULL,
    address_source_id INTEGER,
    longitude REAL NOT NULL,
    longitude_source_id INTEGER,
    latitude REAL NOT NULL,
    latitude_source_id INTEGER,
    details_id INTEGER UNIQUE NOT NULL,
    CONSTRAINT check_type_matches_choices
        CHECK (type IN ('soup_kitchen', 'toilet', 'water_fountain')),
    FOREIGN KEY(longitude_source_id) REFERENCES sources(id)
        ON DELETE NO ACTION
        ON UPDATE CASCADE,
    FOREIGN KEY(latitude_source_id) REFERENCES sources(id)
        ON DELETE NO ACTION
        ON UPDATE CASCADE,
    FOREIGN KEY(details_id) REFERENCES details(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE da_locations (
    id INTEGER PRIMARY KEY NOT NULL,
    type VARCHAR(127) NOT NULL,
    name VARCHAR(255) NOT NULL,
    name_source_id INTEGER,
    address VARCHAR NOT NULL,
    address_source_id INTEGER,
    longitude REAL NOT NULL,
    longitude_source_id INTEGER,
    latitude REAL NOT NULL,
    latitude_source_id INTEGER,
    details_id INTEGER NOT NULL,
    CONSTRAINT check_type_matches_choices
        CHECK (type IN ('soup_kitchen', 'toilet', 'water_fountain')),
    FOREIGN KEY(longitude_source_id) REFERENCES sources(id)
        ON DELETE NO ACTION
        ON UPDATE CASCADE,
    FOREIGN KEY(latitude_source_id) REFERENCES sources(id)
        ON DELETE NO ACTION
        ON UPDATE CASCADE
);

CREATE TABLE details (
    id INTEGER PRIMARY KEY NOT NULL,
    operator VARCHAR(255),
    operator_source_id INTEGER,
    opening_times TEXT,
    opening_times_source_id INTEGER,
    toilet_has_fee INTEGER,
    toilet_has_fee_source_id INTEGER,
    toilet_fee DECIMAL(4, 2),
    toilet_fee_source_id INTEGER,
    toilet_is_customer_only INTEGER,
    toilet_is_customer_only_source_id INTEGER,
    toilet_female INTEGER,
    toilet_female_source_id INTEGER,
    toilet_male INTEGER,
    toilet_male_source_id INTEGER,
    toilet_unisex INTEGER,
    toilet_unisex_source_id INTEGER,
    toilet_child INTEGER,
    toilet_child_source_id INTEGER,
    toilet_has_seated INTEGER,
    toilet_has_seated_source_id INTEGER,
    toilet_has_urinal INTEGER,
    toilet_has_urinal_source_id INTEGER,
    toilet_has_squat INTEGER,
    toilet_has_squat_source_id INTEGER,
    toilet_change_table VARCHAR(31),
    toilet_change_table_source_id INTEGER,
    toilet_wheelchair_accessible VARCHAR(31),
    toilet_wheelchair_accessible_source_id INTEGER,
    toilet_wheelchair_access_info TEXT,
    toilet_wheelchair_access_info_source_id INTEGER,
    toilet_has_hand_washing INTEGER,
    toilet_has_hand_washing_source_id INTEGER,
    toilet_has_soap INTEGER,
    toilet_has_soap_source_id INTEGER,
    toilet_has_hand_disinfectant INTEGER,
    toilet_has_hand_disinfectant_source_id INTEGER,
    toilet_has_hand_creme INTEGER,
    toilet_has_hand_creme_source_id INTEGER,
    toilet_has_hand_drying INTEGER,
    toilet_has_hand_drying_source_id INTEGER,
    toilet_hand_drying_method VARCHAR,
    toilet_hand_drying_method_source_id INTEGER,
    toilet_has_paper INTEGER,
    toilet_has_paper_source_id INTEGER,
    toilet_has_hot_water INTEGER,
    toilet_has_hot_water_source_id INTEGER,
    toilet_has_shower INTEGER,
    toilet_has_shower_source_id INTEGER,
    toilet_has_drinking_water INTEGER,
    toilet_has_drinking_water_source_id INTEGER,
    FOREIGN KEY(opening_times_source_id) REFERENCES sources(id)
        ON DELETE NO ACTION
        ON UPDATE CASCADE,
    CONSTRAINT check_toilet_has_fee_is_bool
        CHECK (toilet_has_fee = 0 OR toilet_has_fee = 1),
    FOREIGN KEY(toilet_fee_source_id) REFERENCES sources(id)
        ON DELETE NO ACTION
        ON UPDATE CASCADE,
    CONSTRAINT check_toilet_is_customer_only_is_bool
        CHECK (toilet_is_customer_only = 0 OR toilet_is_customer_only = 1),
    CONSTRAINT check_toilet_female_is_bool
        CHECK (toilet_female = 0 OR toilet_female = 1),
    CONSTRAINT check_toilet_male_is_bool
        CHECK (toilet_male = 0 OR toilet_male = 1),
    CONSTRAINT check_toilet_unisex_is_bool
        CHECK (toilet_unisex = 0 OR toilet_unisex = 1),
    CONSTRAINT check_toilet_child_is_bool
        CHECK (toilet_child = 0 OR toilet_child = 1),
    CONSTRAINT check_toilet_has_seated_is_bool
        CHECK (toilet_has_seated = 0 OR toilet_has_seated = 1),
    CONSTRAINT check_toilet_has_urinal_is_bool
        CHECK (toilet_has_urinal = 0 OR toilet_has_urinal = 1),
    CONSTRAINT check_toilet_has_squat_is_bool
        CHECK (toilet_has_squat = 0 OR toilet_has_squat = 1),
    CONSTRAINT check_toilet_change_table_matches_choices
        CHECK (toilet_change_table IN ('yes', 'no', 'limited')),
    CONSTRAINT check_toilet_wheelchair_accessible_matches_choices
        CHECK (toilet_wheelchair_accessible IN ('yes', 'no', 'limited')),
    FOREIGN KEY(toilet_wheelchair_access_info_source_id) REFERENCES sources(id)
        ON DELETE NO ACTION
        ON UPDATE CASCADE,
    CONSTRAINT check_toilet_has_hand_washing_is_bool
        CHECK (toilet_has_hand_washing = 0 OR toilet_has_hand_washing = 1),
    CONSTRAINT check_toilet_has_soap_is_bool
        CHECK (toilet_has_soap = 0 OR toilet_has_soap = 1),
    CONSTRAINT check_toilet_has_hand_disinfectant_is_bool
        CHECK (toilet_has_hand_disinfectant = 0 OR toilet_has_hand_disinfectant = 1),
    CONSTRAINT check_toilet_has_hand_creme_is_bool
        CHECK (toilet_has_hand_creme = 0 OR toilet_has_hand_creme = 1),
    CONSTRAINT check_toilet_has_hand_drying_is_bool
        CHECK (toilet_has_hand_drying = 0 OR toilet_has_hand_drying = 1),
    CONSTRAINT check_toilet_hand_drying_method_matches_choices
        CHECK (toilet_hand_drying_method IN ('electric_hand_dryer', 'paper_towel', 'towel')),
    CONSTRAINT check_toilet_has_paper_is_bool
        CHECK (toilet_has_paper = 0 OR toilet_has_paper = 1),
    CONSTRAINT check_toilet_has_hot_water_is_bool
        CHECK (toilet_has_hot_water = 0 OR toilet_has_hot_water = 1),
    CONSTRAINT check_toilet_has_shower_is_bool
        CHECK (toilet_has_shower = 0 OR toilet_has_shower = 1),
    CONSTRAINT check_toilet_has_drinking_water_is_bool
        CHECK (toilet_has_drinking_water = 0 OR toilet_has_drinking_water = 1)
);

CREATE TABLE da_details_toilet (
    id INTEGER PRIMARY KEY NOT NULL,
    operator VARCHAR(255),
    operator_source_id INTEGER,
    opening_times TEXT,
    opening_times_source_id INTEGER,
    overpass_node_id INTEGER NOT NULL,
    overpass_node_id_source_id INTEGER,
    overpass_node_data TEXT NOT NULL,
    overpass_node_data_source_id INTEGER,
    has_fee INTEGER,
    has_fee_source_id INTEGER,
    fee DECIMAL(4, 2),
    fee_source_id INTEGER,
    is_customer_only INTEGER,
    is_customer_only_source_id INTEGER,
    female INTEGER,
    female_source_id INTEGER,
    male INTEGER,
    male_source_id INTEGER,
    unisex INTEGER,
    unisex_source_id INTEGER,
    child INTEGER,
    child_source_id INTEGER,
    has_seated INTEGER,
    has_seated_source_id INTEGER,
    has_urinal INTEGER,
    has_urinal_source_id INTEGER,
    has_squat INTEGER,
    has_squat_source_id INTEGER,
    change_table VARCHAR(31),
    change_table_source_id INTEGER,
    wheelchair_accessible VARCHAR(31),
    wheelchair_accessible_source_id INTEGER,
    wheelchair_access_info TEXT,
    wheelchair_access_info_source_id INTEGER,
    has_hand_washing INTEGER,
    has_hand_washing_source_id INTEGER,
    has_soap INTEGER,
    has_soap_source_id INTEGER,
    has_hand_disinfectant INTEGER,
    has_hand_disinfectant_source_id INTEGER,
    has_hand_creme INTEGER,
    has_hand_creme_source_id INTEGER,
    has_hand_drying INTEGER,
    has_hand_drying_source_id INTEGER,
    hand_drying_method VARCHAR,
    hand_drying_method_source_id INTEGER,
    has_paper INTEGER,
    has_paper_source_id INTEGER,
    has_hot_water INTEGER,
    has_hot_water_source_id INTEGER,
    has_shower INTEGER,
    has_shower_source_id INTEGER,
    has_drinking_water INTEGER,
    has_drinking_water_source_id INTEGER,
    FOREIGN KEY(opening_times_source_id) REFERENCES sources(id)
        ON DELETE NO ACTION
        ON UPDATE CASCADE,
    FOREIGN KEY(overpass_node_id_source_id) REFERENCES sources(id)
        ON DELETE NO ACTION
        ON UPDATE CASCADE,
    FOREIGN KEY(overpass_node_data_source_id) REFERENCES sources(id)
        ON DELETE NO ACTION
        ON UPDATE CASCADE,
    CONSTRAINT check_has_fee_is_bool
        CHECK (has_fee = 0 OR has_fee = 1),
    FOREIGN KEY(fee_source_id) REFERENCES sources(id)
        ON DELETE NO ACTION
        ON UPDATE CASCADE,
    CONSTRAINT check_is_customer_only_is_bool
        CHECK (is_customer_only = 0 OR is_customer_only = 1),
    CONSTRAINT check_female_is_bool
        CHECK (female = 0 OR female = 1),
    CONSTRAINT check_male_is_bool
        CHECK (male = 0 OR male = 1),
    CONSTRAINT check_unisex_is_bool
        CHECK (unisex = 0 OR unisex = 1),
    CONSTRAINT check_child_is_bool
        CHECK (child = 0 OR child = 1),
    CONSTRAINT check_has_seated_is_bool
        CHECK (has_seated = 0 OR has_seated = 1),
    CONSTRAINT check_has_urinal_is_bool
        CHECK (has_urinal = 0 OR has_urinal = 1),
    CONSTRAINT check_has_squat_is_bool
        CHECK (has_squat = 0 OR has_squat = 1),
    CONSTRAINT check_change_table_matches_choices
        CHECK (change_table IN ('yes', 'no', 'limited')),
    CONSTRAINT check_wheelchair_accessible_matches_choices
        CHECK (wheelchair_accessible IN ('yes', 'no', 'limited')),
    FOREIGN KEY(wheelchair_access_info_source_id) REFERENCES sources(id)
        ON DELETE NO ACTION
        ON UPDATE CASCADE,
    CONSTRAINT check_has_hand_washing_is_bool
        CHECK (has_hand_washing = 0 OR has_hand_washing = 1),
    CONSTRAINT check_has_soap_is_bool
        CHECK (has_soap = 0 OR has_soap = 1),
    CONSTRAINT check_has_hand_disinfectant_is_bool
        CHECK (has_hand_disinfectant = 0 OR has_hand_disinfectant = 1),
    CONSTRAINT check_has_hand_creme_is_bool
        CHECK (has_hand_creme = 0 OR has_hand_creme = 1),
    CONSTRAINT check_has_hand_drying_is_bool
        CHECK (has_hand_drying = 0 OR has_hand_drying = 1),
    CONSTRAINT check_hand_drying_method_matches_choices
        CHECK (hand_drying_method IN ('electric_hand_dryer', 'paper_towel', 'towel')),
    CONSTRAINT check_has_paper_is_bool
        CHECK (has_paper = 0 OR has_paper = 1),
    CONSTRAINT check_has_hot_water_is_bool
        CHECK (has_hot_water = 0 OR has_hot_water = 1),
    CONSTRAINT check_has_shower_is_bool
        CHECK (has_shower = 0 OR has_shower = 1),
    CONSTRAINT check_has_drinking_water_is_bool
        CHECK (has_drinking_water = 0 OR has_drinking_water = 1)
);

CREATE TABLE sources (
    id INTEGER PRIMARY KEY NOT NULL,
    name VARCHAR(255) NOT NULL,
    url VARCHAR UNIQUE,
    initial_access TEXT,
    last_access TEXT
);
