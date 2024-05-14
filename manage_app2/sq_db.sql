CREATE TABLE IF NOT EXISTS mainmenu (
id integer  PRIMARY KEY AUTOINCREMENT,
title text NOT NULL,
url text NOT NULL
);

CREATE TABLE IF NOT EXISTS secondmenu (
id integer  PRIMARY KEY AUTOINCREMENT,
title text NOT NULL,
url text NOT NULL
);

CREATE TABLE IF NOT EXISTS thirdmenu (
id integer  PRIMARY KEY AUTOINCREMENT,
title text NOT NULL,
url text NOT NULL
);

CREATE TABLE IF NOT EXISTS posts (
id integer  PRIMARY KEY AUTOINCREMENT,
title text DEFAULT NULL,
schema blob DEFAULT NULL,
test_specification text DEFAULT NULL,
test_progress text DEFAULT NULL,
test_result text DEFAULT NULL
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

CREATE TABLE IF NOT EXISTS device_type (
id integer  PRIMARY KEY AUTOINCREMENT,
type text NOT NULL,
device text NOT NULL,
url text
);

CREATE TABLE IF NOT EXISTS test_category (
id integer  PRIMARY KEY AUTOINCREMENT,
type text NOT NULL,
device text NOT NULL,
url text
);


INSERT INTO read_cfg (title, url) VALUES ('Просмотр конфигурации под тест GRE', '/read_cfg/1');
INSERT INTO read_cfg (title, url) VALUES ('Просмотр конфигурации под тест 2', '/read_cfg/2');
INSERT INTO read_cfg (title, url) VALUES ('Просмотр конфигурации под тест 3', '/read_cfg/3');

INSERT INTO mainmenu (title, url) VALUES ('Тесты устройства', '/');
INSERT INTO mainmenu (title, url) VALUES ('Конфигурация устройства', '/cfg');
INSERT INTO mainmenu (title, url) VALUES ('Сброс настроек устройства', '/reset');
INSERT INTO mainmenu (title, url) VALUES ('Настройки', '/constants');
INSERT INTO mainmenu (title, url) VALUES ('Авторизация пользователя', '/login');

INSERT INTO secondmenu (title, url) VALUES ('Проверка поддержки GRE', '1');
INSERT INTO secondmenu (title, url) VALUES ('Проверка поддержки test2', '2');
INSERT INTO secondmenu (title, url) VALUES ('Проверка поддержки test3', '3');

INSERT INTO thirdmenu (title, url) VALUES ('Конфигурация устройства под тест GRE', '/cfg/1');
INSERT INTO thirdmenu (title, url) VALUES ('Конфигурация устройства под test2', '/cfg/2');
INSERT INTO thirdmenu (title, url) VALUES ('Конфигурация устройства под  test3', '/cfg/3');

INSERT INTO posts (title, schema, test_specification, test_progress, test_result) 
VALUES (
'Проверка поддержки GRE', ?,
'Здесь пока пусто',
'Здесь будет прогресс теста',
'Здесь будет результат теста'
);
INSERT INTO posts (title, schema, test_specification, test_progress,test_result) 
VALUES (
'Test Проверка поддержки test2', ?,
'Здесь будет описание test2',
'Здесь будет прогресс test2',
'Здесь будет результат test2'
);
INSERT INTO posts (title, schema, test_specification, test_progress,test_result) 
VALUES (
'Тест: Проверка поддержки test3', ?,
'Здесь будет описание test3',
'Здесь будет прогресс test3',
'Здесь будет результат test3'
);
INSERT INTO constants_trident (title, val, url) VALUES ('device_type', 'cisco_ios_telnet','constants');
INSERT INTO constants_trident (title, val, url) VALUES ('host', '10.27.193.2','constants');
INSERT INTO constants_trident (title, val, url) VALUES ('username', 'admin','constants');
INSERT INTO constants_trident (title, val, url) VALUES ('password', 'bulat','constants');
INSERT INTO constants_trident (title, val, url) VALUES ('secret', 'enable','constants');
INSERT INTO constants_trident (title, val, url) VALUES ('port', '0000','constants');
