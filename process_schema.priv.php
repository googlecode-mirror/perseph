<?php

require_once 'php_datamanip/dbschema_parser.inc';
require_once 'php_datamanip/dbschema_phpemitter.inc';

if( $argc != 3 )
	die( "Syntax: input.schema output/dir/base_\n" );
	
$input = $argv[1];
$output = $argv[2];


$data = file_get_contents( $input );

$schema = DBSchema::parse( $data );
//var_dump( $schema );

$emit = new DBSchema_PHPEmitter( $schema );
$emit->emit( $output );

?>