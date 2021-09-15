CREATE TABLE locations (
    id INT NOT NULL,
    type VARCHAR (127) NOT NULL,
    name VARCHAR (255) NOT NULL,
    longitude REAL NOT NULL,
    latitude REAL NOT NULL,
    details_id INT NOT NULL,
    CONSTRAINT check_type CHECK (type IN ('toilet', 'water_fountain', 'soup_kitchen'))
    PRIMARY KEY (id)
);

CREATE TABLE details (
    id INT NOT NULL,
    opening_time TIME,
    closing_time TIME,
    PRIMARY KEY (id)
);