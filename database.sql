DROP TABLE IF EXISTS url_checks;
DROP TABLE IF EXISTS urls;


CREATE TABLE urls(
    id SERIAL PRIMARY KEY,
    name varchar(255) UNIQUE NOT NULL,
    created_at date NOT NULL
);

CREATE TABLE url_checks(
    id SERIAL PRIMARY KEY,
    url_id bigint REFERENCES urls(id),
    status_code int,
    h1 varchar(255),
    title varchar(255),
    description text,
    created_at date
);