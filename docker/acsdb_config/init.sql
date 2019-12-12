CREATE DATABASE IF NOT EXISTS weatherdb;
USE weatherdb;

CREATE TABLE IF NOT EXISTS devices (
    uuid        VARCHAR(36) PRIMARY KEY,
    api_key     VARCHAR(36) UNIQUE DEFAULT ""
);

CREATE TABLE IF NOT EXISTS metausage (
    api_key     VARCHAR(36) PRIMARY KEY,
    daily       INT DEFAULT 0,
    weekly      INT DEFAULT 0,
    monthly     INT DEFAULT 0,
    total       INT DEFAULT 0
);

CREATE TABLE IF NOT EXISTS cities (
    country     VARCHAR(2) PRIMARY KEY,
    city        VARCHAR(36) UNIQUE,
    numcalls    INT DEFAULT 0
);

CREATE USER 'axiiom'@'192.19.0.2' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON weatherdb . * TO 'axiiom'@'192.19.0.2';
