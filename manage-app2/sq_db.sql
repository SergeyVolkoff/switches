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

INSERT INTO mainmenu (title, url) VALUES ('Меню тестов', '/');
INSERT INTO mainmenu (title, url) VALUES ('Меню конфигов', '/cfg');
INSERT INTO mainmenu (title, url) VALUES ('Меню сброса настроек', '/reset');
INSERT INTO mainmenu (title, url) VALUES ('Меню настроек теста', '/constants');
INSERT INTO mainmenu (title, url) VALUES ('Авторизация', '/login');

INSERT INTO secondmenu (title, url) VALUES ('Проверка поддержки GRE', '1');
INSERT INTO secondmenu (title, url) VALUES ('Проверка поддержки test2', '2');
INSERT INTO secondmenu (title, url) VALUES ('Проверка поддержки test3', '3');

INSERT INTO thirdmenu (title, url) VALUES ('Конфиг под тест GRE', '/cfg/1');
INSERT INTO thirdmenu (title, url) VALUES ('Конфиг под test2', '/cfg/2');
INSERT INTO thirdmenu (title, url) VALUES ('Конфиг под  test3', '/cfg/3');

INSERT INTO posts (title, schema, test_specification, test_progress,test_result) 
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
'Test Проверка поддержки test3', ?,
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
