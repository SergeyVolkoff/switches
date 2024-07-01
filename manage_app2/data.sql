CREATE TABLE mainmenu (
id SERIAL PRIMARY KEY,
title text NOT NULL,
url text NOT NULL
);
CREATE TABLE sqlite_sequence(
name text, 
seq integer
);
CREATE TABLE thirdmenu (
id SERIAL PRIMARY KEY,
title text NOT NULL,
url text NOT NULL
);
CREATE TABLE constants_trident (
id SERIAL PRIMARY KEY,
title text NOT NULL,
val text NOT NULL,
url text
);
CREATE TABLE users (
id SERIAL PRIMARY KEY,
name text NOT NULL,
email text NOT NULL,
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
INSERT INTO mainmenu VALUES(1,'Конфигурация устройства','/cfg');
INSERT INTO mainmenu VALUES(2,'Сброс настроек устройства','/reset');
INSERT INTO mainmenu VALUES(3,'Настройки','/constants');
INSERT INTO mainmenu VALUES(4,'Авторизация пользователя','/login');
INSERT INTO mainmenu VALUES(5,'ГЛАВНАЯ','/');
INSERT INTO thirdmenu VALUES(1,'Конфигурация устройства под тест GRE','/cfg/1');
INSERT INTO thirdmenu VALUES(2,'Конфигурация устройства под test2','/cfg/2');
INSERT INTO thirdmenu VALUES(3,'Конфигурация устройства под  test3','/cfg/3');
INSERT INTO constants_trident VALUES(1,'device_type','cisco_ios_telnet','constants');
INSERT INTO constants_trident VALUES(2,'host','10.27.193.2','constants');
INSERT INTO constants_trident VALUES(3,'username','admin','constants');
INSERT INTO constants_trident VALUES(4,'password','bulat','constants');
INSERT INTO constants_trident VALUES(5,'secret','enable','constants');
INSERT INTO constants_trident VALUES(6,'port',2043,'constants');
INSERT INTO users VALUES(1,'admin','admin@admin.com','scrypt:32768:8:1$0yQ0WDvGNiEGzh8A$77de0cca096936fb8a683da1ca6a476421bb63548ec3bfdab246b0099d06524f7f6e9a45f5fc4f24b9d495c78dc925b7f0304f8a4e7438588e8007527a85b940','1718627249');
INSERT INTO users VALUES(2,'user','user@user.com','scrypt:32768:8:1$Zh2llC2tz62akzNj$fe97b3767bc574ecd8d3bad2989a6c9abfbb90fe8cc66fd6eaf7949851081292de230967a8e39d28bf220c715c8593b93b6936c0ddca1a7193805086348499b6','1719212310');
INSERT INTO users VALUES(3,'user1','user1@user1.com','scrypt:32768:8:1$bpkYfmiOA7UUqpDQ$f5350f96a79a1f0f71f3834b90c7a29bca7776e1d5c567e77f54bfc2b63f50866eac60e42a014b08a7446f3cd4ff2a521e5daf8d5d6a9cb3127c4dd4b6f7ae98','1719212344');
INSERT INTO users VALUES(4,'admin!','admin!@admin.co','pbkdf2:sha256:260000$1M02z3nXOKhl2gcK$fc7730debae477fb8d98e3476d29f8b0732f6806c61b1b777d1c3c88348a0f8a','1719470342');
INSERT INTO users VALUES(5,'user2','user2@user2.com','pbkdf2:sha256:260000$wdS7UVotgBO4hDkd$0be971f81872b04306b8d8668a4b29cbf993cb76e290cf85d64cd2fc4d1c37c7','1719470432');
INSERT INTO read_cfg VALUES(1,'Просмотр конфигурации под тест GRE','/read_cfg/1');
INSERT INTO read_cfg VALUES(2,'Просмотр конфигурации под тест 2','/read_cfg/2');
INSERT INTO read_cfg VALUES(3,'Просмотр конфигурации под тест 3','/read_cfg/3');
INSERT INTO device VALUES(1,'cpe','CPE','bm10-hp','BM10-HP-2xLTE','/bm10hp2xlte');
INSERT INTO device VALUES(2,'cpe','CPE','bm10-lte','BM10-LTE','/bm10lte');
INSERT INTO device VALUES(3,'router','Router','bm1300','BM1300','/bm1300');
INSERT INTO device VALUES(4,'switchboard','Switchboard','trident','Trident','/BS751048x6q');
INSERT INTO device_type VALUES(1,'cpe','CPE');
INSERT INTO device_type VALUES(2,'router','Router');
INSERT INTO device_type VALUES(3,'switchboard','Switchboard');
INSERT INTO tests_category VALUES(1,'l2','L2 тесты','/l2');
INSERT INTO tests_category VALUES(2,'l3','L3 тесты','/l3');
INSERT INTO tests_category VALUES(3,'manage','Management тесты','/manag_categor');
INSERT INTO tests_category VALUES(4,'secur','Security тесты','/secur_categor');
INSERT INTO tests_category VALUES(5,'amount1','Тесты с использованием 1 устройства','/amount1_categor ');
INSERT INTO tests_category VALUES(6,'amount2','Тесты с использованием 2 устройства','/amount2_categor ');
INSERT INTO tests_category VALUES(7,'amount3','Тесты с использованием 3 и более устройств','/amount3_categor ');
INSERT INTO tests_category VALUES(8,'ixia','Тесты с использованием IXIA','/ixia_categor');
INSERT INTO tests_category VALUES(9,'gns','Тесты с использованием GNS3','/gns_categor');
INSERT INTO tests_all VALUES(1,'l2','Проверка механизмов Learning, Forwarding, Filtering, Flooding','/static/tests_schema/','/static/tests_descr/');
INSERT INTO tests_all VALUES(2,'l2','Проверка поддержки Jumbo frame','/static/tests_schema/','/static/tests_descr/');
INSERT INTO tests_all VALUES(3,'l2','Проверка статических записей в MAC-таблице','/static/tests_schema/','/static/tests_descr/');
INSERT INTO tests_all VALUES(4,'l2','Проверка ограничения на размер MAC-таблицы per-port/per-bridge','/static/tests_schema/','/static/tests_descr/');
INSERT INTO tests_all VALUES(5,'l2','Проверка MAC Ageing Timer','/static/tests_schema/','/static/tests_descr/');
INSERT INTO tests_all VALUES(6,'l2','Проверка механизма Err-Disable','/static/tests_schema/','/static/tests_descr/');
INSERT INTO tests_all VALUES(7,'l2','Проверка механизма Port Security','/static/tests_schema/','/static/tests_descr/');
INSERT INTO tests_all VALUES(8,'l2','Проверка механизма Layer 2 Protocol Tunneling','/static/tests_schema/','/static/tests_descr/');
INSERT INTO tests_all VALUES(9,'l2','Проверка механизма Flow Control','/static/tests_schema/','/static/tests_descr/');
INSERT INTO tests_all VALUES(10,'l2','Проверка конфигурирования MAC на интерфейсе','/static/tests_schema/','/static/tests_descr/');
INSERT INTO tests_all VALUES(11,'l3','Проверка функционирования Static Routing','/static/tests_schema/','/static/tests_descr/');
INSERT INTO tests_all VALUES(12,'l3','Проверка возможности изменения параметра priority','/static/tests_schema/','/static/tests_descr/');
INSERT INTO tests_all VALUES(13,'l3','Проверка возможности включения OSPF на интерфейсе','/static/tests_schema/','/static/tests_descr/');
INSERT INTO tests_all VALUES(14,'manage','Проверка доступа (Console, Telnet, SSH)','/static/tests_schema/','/static/tests_descr/');
INSERT INTO tests_all VALUES(15,'manage','Обновление ПО','/static/tests_schema/','/static/tests_descr/');
INSERT INTO tests_all VALUES(16,'manage','Сохранение и восстановление конфигурации','/static/tests_schema/','/static/tests_descr/');
INSERT INTO tests_all VALUES(17,'secur','Проверка функционала AAA','/static/tests_schema/','/static/tests_descr/');
INSERT INTO tests_all VALUES(18,'secur','Проверка механизма Control Plane Protection ACL','/static/tests_schema/','/static/tests_descr/');
INSERT INTO tests_all VALUES(19,'secur','Проверка функционирования ACL (Access Lits) L2','/static/tests_schema/','/static/tests_descr/');
INSERT INTO tests_all VALUES(20,'gns','Проверка поддержки GRE','/static/tests_schema/','/static/tests_descr/');
INSERT INTO tests_all VALUES(21,'gns','Проверка поддержки Chego_to_Tam','/static/tests_schema/','/static/tests_descr/');
DELETE FROM sqlite_sequence;
INSERT INTO sqlite_sequence VALUES('device',4);
INSERT INTO sqlite_sequence VALUES('device_type',3);
INSERT INTO sqlite_sequence VALUES('tests_category',9);
INSERT INTO sqlite_sequence VALUES('tests_all',21);
INSERT INTO sqlite_sequence VALUES('read_cfg',3);
INSERT INTO sqlite_sequence VALUES('mainmenu',5);
INSERT INTO sqlite_sequence VALUES('thirdmenu',3);
INSERT INTO sqlite_sequence VALUES('constants_trident',6);
INSERT INTO sqlite_sequence VALUES('users',5);
COMMIT;
