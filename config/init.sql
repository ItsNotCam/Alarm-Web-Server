CREATE DATABASE IF NOT EXISTS weatherdb;
USE weatherdb;

CREATE TABLE IF NOT EXISTS devices (
    uuid        VARCHAR(32) PRIMARY KEY,
    api_key     VARCHAR(32) UNIQUE DEFAULT ""
);

CREATE TABLE IF NOT EXISTS metausage (
    api_key     VARCHAR(32) PRIMARY KEY,
    daily       INT DEFAULT 0,
    weekly      INT DEFAULT 0,
    monthly     INT DEFAULT 0,
    total       INT DEFAULT 0
);

CREATE TABLE IF NOT EXISTS cities (
    country     VARCHAR(2) PRIMARY KEY,
    city        VARCHAR(32) UNIQUE,
    numcalls    INT DEFAULT 0
);

CREATE USER 'axiiom'@'localhost' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON weatherdb . * TO 'axiiom'@'localhost';