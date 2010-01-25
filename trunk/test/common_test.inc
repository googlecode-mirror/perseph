<?php
require_once 'php_settings.inc';

require_once dirname(__FILE__).'/../php_support/cache.inc';
require_once dirname(__FILE__) . '/testcache.inc';

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