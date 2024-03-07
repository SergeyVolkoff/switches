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

CREATE TABLE IF NOT EXISTS posts (
id integer  PRIMARY KEY AUTOINCREMENT,
title text NOT NULL,
schema blob DEFAULT NULL,
test_specification text NOT NULL,
test_progress text NOT NULL,
result text NOT NULL
);

CREATE TABLE IF NOT EXISTS constants_trident (
id integer  PRIMARY KEY AUTOINCREMENT,
title text NOT NULL,
val integer NOT NULL,
url text
);

INSERT INTO mainmenu (title, url) VALUES ('Меню тестов', '/');
INSERT INTO mainmenu (title, url) VALUES ('Меню конфигов', 'cfg');
INSERT INTO mainmenu (title, url) VALUES ('Меню сброса настроек', 'reset');
INSERT INTO mainmenu (title, url) VALUES ('Меню настроек теста', 'constants');

INSERT INTO secondmenu (title, url) VALUES ('Проверка поддержки GRE', 'test1');
INSERT INTO secondmenu (title, url) VALUES ('Проверка поддержки test2', 'test2');
INSERT INTO secondmenu (title, url) VALUES ('Проверка поддержки test3', 'test3');

INSERT INTO posts (title, schema, test_specification, test_progress,result) 
VALUES (
'Test Проверка поддержки GRE', ?,
'Здесь будет описание теста',
'Здесь будет прогресс теста',
'Здесь будет результат теста'
);


INSERT INTO constants_trident (title, val, url) VALUES ('device_type', 'cisco_ios_telnet','constants');
INSERT INTO constants_trident (title, val, url) VALUES ('host', '10.27.193.2','constants');
INSERT INTO constants_trident (title, val, url) VALUES ('username', 'admin','constants');
INSERT INTO constants_trident (title, val, url) VALUES ('password', 'bulat','constants');
INSERT INTO constants_trident (title, val, url) VALUES ('secret', 'enable','constants');
INSERT INTO constants_trident (title, val, url) VALUES ('port', '0000','constants');
