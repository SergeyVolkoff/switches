CREATE TABLE IF NOT EXISTS mainmenu (
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
INSERT INTO mainmenu VALUES ('1','Меню тестов', '/');
INSERT INTO mainmenu VALUES ('2', 'Меню конфигов', 'cfg');
INSERT INTO mainmenu VALUES ('3', 'Меню сброса настроек', 'reset');