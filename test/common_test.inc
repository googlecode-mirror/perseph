<?php
require_once dirname(__FILE__).'/../php_support/error_handling.inc';
if( !isset( $skipCommonSchema ) )
	require_once dirname(__FILE__).'/gen/schema.inc';
	
//date_default_timezone_set('Europe/Berlin'); 
date_default_timezone_set('UTC'); //TODO: consider impact of this in Date conversions... (already breaks!)
//force our defaults
ini_set( 'mbstring.internal_encoding', 'UTF-8' );
ini_set( 'mbstring.http_output',  'UTF-8' );
ini_set( 'mbstring.http_input', 'UTF-8' );
ini_set( 'mbstring.func_overload', 7 );

$db_test = new MySQLSource( 'localhost', "dbs_test", 'DBSTestUser', 'password', 'utf-8' );
	
function std_header( ) {
	header( "Content-Type: text/html; charset=utf-8" );	//TODO: hmm, depends/requires itnernal encoding to be utf-8...
}

/* In the schema we indicate a variable which defines a prefix for some tables */
$dbtest2_prefix = "pre_";

/* we also said to use a function to get the DB, here we'll simply return the global
	variable. Note, it must return by reference in PHP! */
function &dbtest2_get() {
	return $GLOBALS['db_test'];
}

/* The customer classes for the entites */

class DerivedStrings extends DBSStrings {

	//TODO: Show how to provide custom static constructors
	
	/**
	 * A very simple example of how to provide custom functionality.
	 */
	public function contains( $str ) {
		return (bool)array_search( $str, $this->labels );
	}
}

/* The converters for custom types */

function convert_Integer_to_CustomID( $value ) {
	return $value;
}

function convert_CustomID_to_Integer( $value ) {
	return $value;
}

/* The converters for the entity mappers */

function convert_labels( $str ) {
	$ret = explode( ',', $str );
	if( $ret === false )
		return array();
	return $ret;
}

function convert_labels_inv( $arr ) {
	return implode( ',', $arr );
}

//no _inv form is needed since this is save only (to the DB)
function count_labels( $labels ) {
	return count( $labels );
}

function convert_id( $id ) {
	return $id - 1000;
}

function convert_id_inv( $id ) {
	return $id + 1000;
}

?>