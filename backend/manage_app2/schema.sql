CREATE TABLE mainmenu (
id SERIAL PRIMARY KEY,
title text NOT NULL,
url text NOT NULL
);
CREATE TABLE sqlite_sequence(name,seq);
CREATE TABLE thirdmenu (
id SERIAL PRIMARY KEY,
title text NOT NULL,
url text NOT NULL
);
CREATE TABLE constants_trident (
id SERIAL PRIMARY KEY,
title text NOT NULL,
val  NOT NULL,
url text
);
CREATE TABLE users (
id SERIAL PRIMARY KEY,
name text NOT NULL,
email  NOT NULL,
psw text NOT NULL,
url text
);
CREATE TABLE read_cfg (
id SERIAL PRIMARY KEY,
title text NOT NULL,
url text
);
CREATE TABLE device (
id SERIAL PRIMARY KEY,
tag_type text,
tag_name text,
device_tag text,
device_name text NOT NULL,
url text
);
CREATE TABLE device_type (
id SERIAL PRIMARY KEY,
tag text NOT NULL,
type_dev text NOT NULL
);
CREATE TABLE tests_category (
id SERIAL PRIMARY KEY,
tag text,
name text NOT NULL,
url text
);
CREATE TABLE l2_test (
id SERIAL PRIMARY KEY,
tag text,
name text NOT NULL,
path_schema text,
path_descr text
);
CREATE TABLE tests_all (
id SERIAL PRIMARY KEY,
tag text,
name text NOT NULL,
path_schema text,
path_descr text
);
