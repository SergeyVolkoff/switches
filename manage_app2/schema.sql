CREATE TABLE mainmenu (
id integer  PRIMARY KEY AUTOINCREMENT,
title text NOT NULL,
url text NOT NULL
);
CREATE TABLE sqlite_sequence(name,seq);
CREATE TABLE thirdmenu (
id integer  PRIMARY KEY AUTOINCREMENT,
title text NOT NULL,
url text NOT NULL
);
CREATE TABLE constants_trident (
id integer  PRIMARY KEY AUTOINCREMENT,
title text NOT NULL,
val integer NOT NULL,
url text
);
CREATE TABLE users (
id integer  PRIMARY KEY AUTOINCREMENT,
name text NOT NULL,
email integer NOT NULL,
psw text NOT NULL,
url text
);
CREATE TABLE read_cfg (
id integer  PRIMARY KEY AUTOINCREMENT,
title text NOT NULL,
url text
);
CREATE TABLE device (
id integer  PRIMARY KEY AUTOINCREMENT,
tag_type text,
tag_name text,
device_tag text,
device_name text NOT NULL,
url text
);
CREATE TABLE device_type (
id integer  PRIMARY KEY AUTOINCREMENT,
tag text NOT NULL,
type_dev text NOT NULL
);
CREATE TABLE tests_category (
id integer  PRIMARY KEY AUTOINCREMENT,
tag text,
name text NOT NULL,
url text
);
CREATE TABLE l2_test (
id integer  PRIMARY KEY AUTOINCREMENT,
tag text,
name text NOT NULL,
path_schema text,
path_descr text
);
CREATE TABLE tests_all (
id integer  PRIMARY KEY AUTOINCREMENT,
tag text,
name text NOT NULL,
path_schema text,
path_descr text
);
