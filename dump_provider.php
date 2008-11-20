<?php
/**
 * Produces the provider declaration for a DB.
 *
 * FEATURE: This is only known to support MySQL for now (other DBs may likely produce invalid results)
 */
require_once dirname(__FILE__).'/php_support/error_handling.inc';

require_once 'MDB2.php';

if( $argc < 3 ) {
	print( "Syntax: {$argv[0]} provider_name dsn
	
DSN Example: mysqli://DBSTestUser:password@localhost/dbs_test
" );
	exit(1);
}

function check_error( $res ) {
	if( !@PEAR::isError( $res ) ) 
		return true;
		
	error_log( $res->getMessage() );
	exit(1);
}

$typeMap = array( 
	'int' => 'Integer',
	'tinyint' => 'Integer',
	'char' => 'String',
	'varchar' => 'String',
	'text' => 'Text',
	'date' => 'Date',
	'time' => 'Time',
	'datetime' => 'DateTime',
	'decimal' => 'Decimal',
	'float' => 'Float',
	);
$provider = $argv[1];
$dsn = $argv[2];

//turn off all portability to get most correct representation
$mdb = @MDB2::factory( $dsn, array( 'portability' => MDB2_PORTABILITY_NONE ) );
check_error( $mdb );
$mdb->loadModule('Manager');
$mdb->loadModule('Reverse');

print( '/* File generated by dump_provider */\n' );
print( "provider $provider {\n" );

foreach( $mdb->listTables() as $table ) {
	print( "\ttable $table {\n" );
	//TODO: http://pear.php.net/bugs/bug.php?id=15100
	foreach( $mdb->listTableFields( "`$table`" ) as $field ) {
		
		$decl = $mdb->getTableFieldDefinition( "`$table`", $field );
		$decl = $decl[0];
		if( !array_key_exists( $decl['nativetype'], $typeMap ) )
			die( "Unknown nativetype: {$decl['nativetype']}\n" );
		$type = $typeMap[$decl['nativetype']];
		$ext = '';
		
		if( isset($decl['autoincrement']) && $decl['autoincrement'] )
			$ext = ' LAST_INSERT_ID';
		print( "\t\t$field<$type>$ext;\n" );
	}	
	print( "\t}\n" );
}
print( "}\n" );

?>