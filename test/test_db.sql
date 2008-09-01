-- 
--	This creates/recreates the tables for a test DB in MySql.
--
--	DROP DATABASE if exists dbs_test;
--	CREATE DATABASE `dbs_test` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci; 
--
--	GRANT ALL PRIVILEGES ON dbs_test.* to 'DBSTestUser'@'localhost' IDENTIFIED BY 'password';
--

USE dbs_test;

DROP TABLE IF EXISTS `basic`;

 CREATE TABLE `basic` (
`ID` INT( 11 ) NOT NULL AUTO_INCREMENT ,
`Name` VARCHAR( 50 ) NOT NULL ,
`Date` DATE NOT NULL ,
`Time` TIME NOT NULL ,
`DateTime` DATETIME,
`Bool` BOOL NOT NULL ,
`Decimal` DECIMAL( 10, 5 ) NOT NULL ,
`Float` FLOAT NOT NULL ,
`NameRef` INT( 2 ) NULL ,
PRIMARY KEY ( `ID` ) ,
UNIQUE (`Name`)
);

DROP TABLE IF EXISTS `twokeys`;

 CREATE TABLE `dbs_test`.`twokeys` (
`KeyNum` INT( 11 ) NOT NULL ,
`KeyString` VARCHAR( 20 ) NOT NULL ,
`Value` VARCHAR( 50 ) NOT NULL ,
INDEX ( `KeyNum` , `KeyString` )
) ;

DROP TABLE IF EXISTS `convert`;

 CREATE TABLE `dbs_test`.`convert` (
`Labels` VARCHAR( 255 ) NOT NULL ,
`Index` INT( 11 ) NOT NULL AUTO_INCREMENT ,
`LabelCount` INT( 5 ) NOT NULL ,
PRIMARY KEY ( `Index` )
) ;


DROP TABLE IF EXISTS `pre_names`;

CREATE TABLE `dbs_test`.`pre_names` (
`Name` VARCHAR( 50 ) NOT NULL ,
`ID` INT( 2 ) NOT NULL ,
PRIMARY KEY ( `ID` ) ,
INDEX ( `Name` )
);

DROP TABLE IF EXISTS `link`;

CREATE TABLE `link` (
	`ID` INT(11) NOT NULL AUTO_INCREMENT,
	`BasicID` INT(11) NOT NULL,
	PRIMARY KEY(`ID`)
);
