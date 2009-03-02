-- 
--	This creates/recreates the tables for a test DB in MySql.
--
--	DROP DATABASE if exists dbs_test;
--	CREATE DATABASE "dbs_test" DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci; 
--
-- CREATE USER DBSTestUser PASSWORD 'password';
--	GRANT ALL PRIVILEGES ON DATABASE dbs_test TO DBSTestUser;
--

DROP TABLE IF EXISTS "basic";

CREATE TABLE "basic" (
"ID" INT NOT NULL /*TODO: AUTO_INCREMENT */,
"Name" VARCHAR( 50 ) UNIQUE,
"Date" DATE NOT NULL ,
"Time" TIME NOT NULL ,
"DateTime" TIMESTAMP,
"Bool" BOOL NOT NULL ,
"Decimal" DECIMAL( 10, 5 ) NOT NULL ,
"Float" FLOAT NOT NULL ,
"NameRef" SMALLINT NULL ,
"NullStr" VARCHAR( 10 ) NULL,
PRIMARY KEY ( "ID" ) ,
UNIQUE ("Name")
);

DROP TABLE IF EXISTS "twokeys";

 CREATE TABLE "twokeys" (
"KeyNum" INT NOT NULL ,
"KeyString" VARCHAR( 20 ) NOT NULL ,
"Value" VARCHAR( 50 ) NOT NULL 
) ;
CREATE UNIQUE INDEX twokeys_index on twokeys ("KeyNum","KeyString");

DROP TABLE IF EXISTS "convert";

 CREATE TABLE "convert" (
"Labels" VARCHAR( 255 ) NOT NULL ,
"Index" INT NOT NULL /*TODO:AUTO_INCREMENT */,
"LabelCount" INT NOT NULL ,
"Code" CHAR( 5 ) DEFAULT 'xx-yy',
PRIMARY KEY ( "Index" )
) ;


DROP TABLE IF EXISTS "pre_names";

CREATE TABLE "pre_names" (
"Name" VARCHAR( 50 ) NOT NULL ,
"ID" INT NOT NULL ,
PRIMARY KEY ( "ID" ) 
);
CREATE INDEX pre_names_index ON pre_names ("Name");

DROP TABLE IF EXISTS "link";

CREATE TABLE "link" (
	"ID" INT NOT NULL /*TODO: AUTO_INCREMENT*/,
	"BasicID" INT NOT NULL,
	PRIMARY KEY("ID")
);

DROP TABLE IF EXISTS "link2";

CREATE TABLE "link2" (
	"NameA" INT NOT NULL,
	"NameB" INT NOT NULL,
	"Value" INT
);

DROP TABLE IF EXISTS "idname";

CREATE TABLE "idname" (
"Name" VARCHAR( 50 ) NOT NULL ,
"ID" INT NOT NULL /*TODO: AUTO_INCREMENT*/,
PRIMARY KEY ( "ID" ) 
);
CREATE INDEX idname_index ON idname ("Name");

DROP TABLE IF EXISTS "mergebasic";

 CREATE TABLE "mergebasic" (
"ID" INT NOT NULL,
"Name" VARCHAR( 50 ) UNIQUE,
"Date" DATE NOT NULL ,
"Time" TIME NOT NULL ,
"DateTime" TIMESTAMP,
"Bool" BOOL NOT NULL ,
"Decimal" DECIMAL( 10, 5 ) NOT NULL ,
"Float" FLOAT NOT NULL ,
PRIMARY KEY ( "ID" )
);
