<?php
//force our defaults
ini_set('mbstring.language','neutral');
ini_set( 'mbstring.internal_encoding', 'UTF-8' );
ini_set( 'mbstring.http_output',  'UTF-8' );
ini_set( 'mbstring.http_input', 'pass' );
ini_set( 'mbstring.substitute_character', 'long' );
ini_set( 'mbstring.func_overload', 7 );
ini_set( 'iconv_internal_encoding', 'UTF-8' );

//use standard handling to suppress strict messages from PEAR/MDB2
require_once dirname(__FILE__).'/../php_support/error_handling.inc';
	
//date_default_timezone_set('Europe/Berlin'); 
date_default_timezone_set('UTC'); //TODO: consider impact of this in Date conversions... (already breaks!)

?>