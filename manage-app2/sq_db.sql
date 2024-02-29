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
text text NOT NULL,
time integer NOT NULL
);

INSERT INTO mainmenu (title, url) VALUES ('Меню тестов', '/');
INSERT INTO mainmenu (title, url) VALUES ('Меню конфигов', 'cfg');
INSERT INTO mainmenu (title, url) VALUES ('Меню сброса настроек', 'reset');
INSERT INTO mainmenu (title, url) VALUES ('Меню настроек теста', 'constants');

INSERT INTO secondmenu (title, url) VALUES ('Проверка поддержки GRE', 'test1');
INSERT INTO secondmenu (title, url) VALUES ('Проверка поддержки test2', 'test2');
INSERT INTO secondmenu (title, url) VALUES ('Проверка поддержки test3', 'test3');