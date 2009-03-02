-- 
--	This creates/recreates the tables for a test DB in MySql.
--
--	DROP DATABASE if exists dbs_test;
--	CREATE DATABASE "dbs_test" DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci; 
--
-- CREATE USER "DBSTestUser" PASSWORD 'password';
--	GRANT ALL PRIVILEGES ON DATABASE dbs_test TO "DBSTestUser";
--
-- The rest should run as the DBSTestUser, since postgres doesn't have a grant which accepts all tables


DROP SEQUENCE IF EXISTS basic_seq CASCADE;
CREATE SEQUENCE basic_seq;

DROP TABLE IF EXISTS "basic";
CREATE TABLE "basic" (
	"ID" INT NOT NULL DEFAULT nextval('basic_seq'),
	"Name" VARCHAR( 50 ) UNIQUE,
	"Date" DATE NOT NULL DEFAULT current_timestamp,
	"Time" TIME NOT NULL DEFAULT '00:00:00.00',	/*TODO: Time type is completely different in Postgres*/
	"DateTime" TIMESTAMP DEFAULT current_timestamp,
	"Bool" BOOL NOT NULL DEFAULT false,
	"Decimal" DECIMAL( 10, 5 ) NOT NULL DEFAULT 0,
	"Float" FLOAT NOT NULL DEFAULT 0,
	"NameRef" SMALLINT NULL ,
	"NullStr" VARCHAR( 10 ) NULL,
	PRIMARY KEY ( "ID" ) ,
	UNIQUE ("Name")
);

DROP TABLE IF EXISTS "twokeys";

CREATE TABLE "twokeys" (
	"KeyNum" INT NOT NULL ,
	"KeyString" VARCHAR( 20 ) NOT NULL DEFAULT '',	/*The default only exists for use in BasicTwoKeys entity*/
	"Value" VARCHAR( 50 ) NOT NULL 
) ;
CREATE UNIQUE INDEX twokeys_index on twokeys ("KeyNum","KeyString");

DROP SEQUENCE IF EXISTS convert_seq CASCADE;
CREATE SEQUENCE convert_seq;

DROP TABLE IF EXISTS "convert";
CREATE TABLE "convert" (
	"Labels" VARCHAR( 255 ) NOT NULL ,
	"Index" INT NOT NULL DEFAULT nextval('convert_seq'),
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

DROP SEQUENCE IF EXISTS link_seq CASCADE;
CREATE SEQUENCE link_seq;

DROP TABLE IF EXISTS "link";
CREATE TABLE "link" (
	"ID" INT NOT NULL DEFAULT nextval('link_seq'),
	"BasicID" INT NOT NULL,
	PRIMARY KEY("ID")
);

DROP TABLE IF EXISTS "link2";

CREATE TABLE "link2" (
	"NameA" INT NOT NULL,
	"NameB" INT NOT NULL,
	"Value" INT
);


DROP SEQUENCE IF EXISTS idname_seq CASCADE;
CREATE SEQUENCE idname_seq;

DROP TABLE IF EXISTS "idname";
CREATE TABLE "idname" (
	"Name" VARCHAR( 50 ) NOT NULL ,
	"ID" INT NOT NULL DEFAULT nextval('idname_seq'),
	PRIMARY KEY ( "ID" ) 
);
CREATE INDEX idname_index ON idname ("Name");

DROP TABLE IF EXISTS "mergebasic";

CREATE TABLE "mergebasic" (
	"ID" INT NOT NULL,
	"Name" VARCHAR( 50 ) UNIQUE,
	"Date" DATE NOT NULL DEFAULT current_timestamp,
	"Time" TIME NOT NULL DEFAULT '00:00:00.00',
	"DateTime" TIMESTAMP DEFAULT current_timestamp,
	"Bool" BOOL NOT NULL DEFAULT false,
	"Decimal" DECIMAL( 10, 5 ) NOT NULL DEFAULT 0,
	"Float" FLOAT NOT NULL DEFAULT 0,
PRIMARY KEY ( "ID" )
);
