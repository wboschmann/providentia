-- From the psql bash, run the following to create the database and schema:

-- To create and connect to the database, run from here
DROP DATABASE IF EXISTS phosim;
CREATE DATABASE phosim;
\c phosim;

-- Use PostGis

CREATE EXTENSION postgis;

-- If already connected to the database, run from here to create the schema

DROP TABLE IF EXISTS transfer;
DROP TABLE IF EXISTS resource;
DROP TABLE IF EXISTS priority;
DROP TABLE IF EXISTS response;

DROP INDEX IF EXISTS response_ttas_ind;
DROP INDEX IF EXISTS response_ttp_ind;
DROP INDEX IF EXISTS response_tth_ind;
DROP INDEX IF EXISTS response_tts_ind;
DROP INDEX IF EXISTS response_origin_ind;
DROP INDEX IF EXISTS response_dest_ind;

CREATE TABLE transfer
(
    response_id         INTEGER NOT NULL,
    travel_time_station NUMERIC NOT NULL,
    FOREIGN KEY (response_id) REFERENCES response (id)
);

CREATE TABLE resource
(
    id          INTEGER UNIQUE,
    response_id INTEGER NOT NULL,
    FOREIGN KEY (response_id) REFERENCES response (id)
);

CREATE TABLE priority
(
    id          INTEGER UNIQUE,
    response_id INTEGER      NOT NULL,
    description CHARACTER(8) NOT NULL, -- High, moderate, low
    FOREIGN KEY (response_id) REFERENCES response (id)
);

CREATE TABLE response
(
    id                       INTEGER UNIQUE,
    origin                   geometry(Point, 4326) NOT NULL,
    destination              geometry(Point, 4326) NOT NULL,
    t                        INTEGER               NOT NULL,
    time_to_ambulance_starts NUMERIC               NOT NULL,
    on_scene_duration        NUMERIC               NOT NULL,
    time_at_hospital         NUMERIC               NOT NULL,
    travel_time_patient      NUMERIC               NOT NULL,
    travel_time_hospital     NUMERIC               NOT NULL,
    resource_ready_time      NUMERIC               NOT NULL,
    PRIMARY KEY (id)
);

-- Index spatio-temporal data
CREATE INDEX response_ttas_ind ON response (time_to_ambulance_starts);
CREATE INDEX response_ttp_ind ON response (travel_time_patient);
CREATE INDEX response_tth_ind ON response (travel_time_hospital);
CREATE INDEX response_tts_ind ON transfer (travel_time_station);
CREATE INDEX response_origin_ind ON response USING GIST (origin);
CREATE INDEX response_dest_ind ON response USING GIST (destination);

-- Cluster response by start time
CLUSTER transfer USING response_tts_ind;
