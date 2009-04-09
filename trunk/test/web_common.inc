<?php
	require_once dirname(__FILE__).'/common_test.inc';
	require_once dirname(__FILE__).'/../php_support/dbsource.inc';
	
	# These sources should be deprecated since I don't want to support them...
	#$db_test = new MySQLSource( 'localhost', "dbs_test", 'DBSTestUser', 'password', 'utf-8' );
	# Use the MDB for with character set support as the default (last to run in makefile)
	$mdb_test = @MDB2::factory( "mysqli://DBSTestUser:password@localhost/dbs_test" );
	$mdb_test->setCharset( "utf8" );
	$db_test = new MDB2DBSource( $mdb_test );	//since our scheme uses the wrapper
?>