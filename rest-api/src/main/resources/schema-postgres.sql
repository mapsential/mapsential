DROP TABLE IF EXISTS locations;
CREATE TABLE locations(id serial PRIMARY KEY, type VARCHAR(127), name VARCHAR(255), address VARCHAR, longitude REAL, latitude REAL, details_id INTEGER);