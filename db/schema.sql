CREATE TYPE mood AS ENUM ('toilet', 'water_fountain', 'soup_kitchen');

CREATE TABLE locations (
    id INT NOT NULL,
    name VARCHAR(255) NOT NULL,
    longitude REAL NOT NULL,
    latitude REAL NOT NULL,
    detail_id INT NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE details (
    id INT NOT NULL,
    opening_time TIME,
    closing_time TIME,
    PRIMARY KEY (id)
);