CREATE TABLE IF NOT EXISTS mainmenu (
id integer  PRIMARY KEY AUTOINCREMENT,
title text NOT NULL,
url text NOT NULL
);

CREATE TABLE IF NOT EXISTS thirdmenu (
id integer  PRIMARY KEY AUTOINCREMENT,
title text NOT NULL,
url text NOT NULL
);

CREATE TABLE IF NOT EXISTS constants_trident (
id integer  PRIMARY KEY AUTOINCREMENT,
title text NOT NULL,
val integer NOT NULL,
url text
);

CREATE TABLE IF NOT EXISTS users (
id integer  PRIMARY KEY AUTOINCREMENT,
name text NOT NULL,
email integer NOT NULL,
psw text NOT NULL,
url text
);

CREATE TABLE IF NOT EXISTS read_cfg (
id integer  PRIMARY KEY AUTOINCREMENT,
title text NOT NULL,
url text
);

CREATE TABLE IF NOT EXISTS device (
id integer  PRIMARY KEY AUTOINCREMENT,
tag_type text,
tag_name text,
device_tag text,
device_name text NOT NULL,
url text
);

CREATE TABLE IF NOT EXISTS device_type (
id integer  PRIMARY KEY AUTOINCREMENT,
tag text NOT NULL,
type_dev text NOT NULL
);

CREATE TABLE IF NOT EXISTS tests_category (
id integer  PRIMARY KEY AUTOINCREMENT,
tag text,
name text NOT NULL,
url text
);

CREATE TABLE IF NOT EXISTS l2_test (
id integer  PRIMARY KEY AUTOINCREMENT,
tag text,
name text NOT NULL,
path_schema text,
path_descr text
);

CREATE TABLE IF NOT EXISTS tests_all (
id integer  PRIMARY KEY AUTOINCREMENT,
tag text,
name text NOT NULL,
path_schema text,
path_descr text
);

INSERT INTO device (tag_type, tag_name, device_tag, device_name, url) VALUES ('cpe', 'CPE', 'bm10-hp', 'BM10-HP-2xLTE', '/bm10hp2xlte');
INSERT INTO device (tag_type, tag_name, device_tag, device_name,  url) VALUES ('cpe', 'CPE', 'bm10-lte', 'BM10-LTE', '/bm10lte');
INSERT INTO device (tag_type, tag_name, device_tag, device_name,  url) VALUES ('router', 'Router','bm1300', 'BM1300', '/bm1300');
INSERT INTO device (tag_type, tag_name, device_tag, device_name,  url) VALUES ('switchboard', 'Switchboard','trident', 'Trident','/BS751048x6q');

INSERT INTO device_type (tag, type_dev) VALUES ('cpe', 'CPE');
INSERT INTO device_type (tag, type_dev) VALUES ('router', 'Router');
INSERT INTO device_type (tag, type_dev) VALUES ('switchboard', 'Switchboard');

INSERT INTO tests_category (tag, name, url) VALUES ('l2', 'L2 тесты', '/l2');
INSERT INTO tests_category (tag, name, url) VALUES ('l3', 'L3 тесты', '/l3');
INSERT INTO tests_category (tag, name, url) VALUES ('manage', 'Management тесты', '/manag_categor');
INSERT INTO tests_category (tag, name, url) VALUES ('secur', 'Security тесты', '/secur_categor');
INSERT INTO tests_category (tag, name, url) VALUES ('amount1', 'Тесты с использованием 1 устройства', '/amount1_categor ');
INSERT INTO tests_category (tag, name, url) VALUES ('amount2', 'Тесты с использованием 2 устройства', '/amount2_categor ');
INSERT INTO tests_category (tag, name, url) VALUES ('amount3', 'Тесты с использованием 3 и более устройств', '/amount3_categor ');
INSERT INTO tests_category (tag, name, url) VALUES ('ixia', 'Тесты с использованием IXIA', '/ixia_categor');
INSERT INTO tests_category (tag, name, url) VALUES ('gns', 'Тесты с использованием GNS3', '/gns_categor');

INSERT INTO tests_all (tag, name, path_schema, path_descr) VALUES ('l2', 'Проверка механизмов Learning, Forwarding, Filtering, Flooding', '/static/tests_schema/', '/static/tests_descr/');
INSERT INTO tests_all (tag, name, path_schema, path_descr) VALUES ('l2', 'Проверка поддержки Jumbo frame', '/static/tests_schema/', '/static/tests_descr/');
INSERT INTO tests_all (tag, name, path_schema, path_descr) VALUES ('l2', 'Проверка статических записей в MAC-таблице', '/static/tests_schema/', '/static/tests_descr/');
INSERT INTO tests_all (tag, name, path_schema, path_descr) VALUES ('l2', 'Проверка ограничения на размер MAC-таблицы per-port/per-bridge', '/static/tests_schema/', '/static/tests_descr/');
INSERT INTO tests_all (tag, name, path_schema, path_descr) VALUES ('l2', 'Проверка MAC Ageing Timer', '/static/tests_schema/', '/static/tests_descr/');
INSERT INTO tests_all (tag, name, path_schema, path_descr) VALUES ('l2', 'Проверка механизма Err-Disable', '/static/tests_schema/', '/static/tests_descr/');
INSERT INTO tests_all (tag, name, path_schema, path_descr) VALUES ('l2', 'Проверка механизма Port Security', '/static/tests_schema/', '/static/tests_descr/');
INSERT INTO tests_all (tag, name, path_schema, path_descr) VALUES ('l2', 'Проверка механизма Layer 2 Protocol Tunneling', '/static/tests_schema/', '/static/tests_descr/');
INSERT INTO tests_all (tag, name, path_schema, path_descr) VALUES ('l2', 'Проверка механизма Flow Control', '/static/tests_schema/', '/static/tests_descr/');
INSERT INTO tests_all (tag, name, path_schema, path_descr) VALUES ('l2', 'Проверка конфигурирования MAC на интерфейсе', '/static/tests_schema/', '/static/tests_descr/');

INSERT INTO tests_all (tag, name, path_schema, path_descr) VALUES ('l3', 'Проверка функционирования Static Routing', '/static/tests_schema/', '/static/tests_descr/');
INSERT INTO tests_all (tag, name, path_schema, path_descr) VALUES ('l3', 'Проверка возможности изменения параметра priority', '/static/tests_schema/', '/static/tests_descr/');
INSERT INTO tests_all (tag, name, path_schema, path_descr) VALUES ('l3', 'Проверка возможности включения OSPF на интерфейсе', '/static/tests_schema/', '/static/tests_descr/');

INSERT INTO tests_all (tag, name, path_schema, path_descr) VALUES ('manage', 'Проверка доступа (Console, Telnet, SSH)', '/static/tests_schema/', '/static/tests_descr/');
INSERT INTO tests_all (tag, name, path_schema, path_descr) VALUES ('manage', 'Обновление ПО', '/static/tests_schema/', '/static/tests_descr/');
INSERT INTO tests_all (tag, name, path_schema, path_descr) VALUES ('manage', 'Сохранение и восстановление конфигурации', '/static/tests_schema/', '/static/tests_descr/');

INSERT INTO tests_all (tag, name, path_schema, path_descr) VALUES ('secur', 'Проверка функционала AAA', '/static/tests_schema/', '/static/tests_descr/');
INSERT INTO tests_all (tag, name, path_schema, path_descr) VALUES ('secur', 'Проверка механизма Control Plane Protection ACL', '/static/tests_schema/', '/static/tests_descr/');
INSERT INTO tests_all (tag, name, path_schema, path_descr) VALUES ('secur', 'Проверка функционирования ACL (Access Lits) L2', '/static/tests_schema/', '/static/tests_descr/');

INSERT INTO tests_all (tag, name, path_schema, path_descr) VALUES ('gns','Проверка поддержки GRE', '/static/tests_schema/', '/static/tests_descr/');
INSERT INTO tests_all (tag, name, path_schema, path_descr) VALUES ('gns','Проверка поддержки Chego_to_Tam', '/static/tests_schema/', '/static/tests_descr/');


INSERT INTO read_cfg (title, url) VALUES ('Просмотр конфигурации под тест GRE', '/read_cfg/1');
INSERT INTO read_cfg (title, url) VALUES ('Просмотр конфигурации под тест 2', '/read_cfg/2');
INSERT INTO read_cfg (title, url) VALUES ('Просмотр конфигурации под тест 3', '/read_cfg/3');

INSERT INTO mainmenu (title, url) VALUES ('Конфигурация устройства', '/cfg');
INSERT INTO mainmenu (title, url) VALUES ('Сброс настроек устройства', '/reset');
INSERT INTO mainmenu (title, url) VALUES ('Настройки', '/constants');
INSERT INTO mainmenu (title, url) VALUES ('Авторизация пользователя', '/login');
INSERT INTO mainmenu (title, url) VALUES ('ГЛАВНАЯ', '/');

INSERT INTO thirdmenu (title, url) VALUES ('Конфигурация устройства под тест GRE', '/cfg/1');
INSERT INTO thirdmenu (title, url) VALUES ('Конфигурация устройства под test2', '/cfg/2');
INSERT INTO thirdmenu (title, url) VALUES ('Конфигурация устройства под  test3', '/cfg/3');


INSERT INTO constants_trident (title, val, url) VALUES ('device_type', 'cisco_ios_telnet','constants');
INSERT INTO constants_trident (title, val, url) VALUES ('host', '10.27.193.2','constants');
INSERT INTO constants_trident (title, val, url) VALUES ('username', 'admin','constants');
INSERT INTO constants_trident (title, val, url) VALUES ('password', 'bulat','constants');
INSERT INTO constants_trident (title, val, url) VALUES ('secret', 'enable','constants');
INSERT INTO constants_trident (title, val, url) VALUES ('port', '0000','constants');
