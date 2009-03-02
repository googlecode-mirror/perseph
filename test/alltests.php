<?php

require_once dirname(__FILE__).'/../php_support/error_handling.inc';

require_once 'PHPUnit/Framework.php';
require_once 'PHPUnit/TextUI/TestRunner.php';
require_once 'PHPUnit/Framework.php';

require_once dirname(__FILE__).'/../php_support/dbsource.inc';
require_once dirname(__FILE__).'/../php_support/mdb2_datatype.inc';
require_once dirname(__FILE__).'/../php_support/form_base.inc';

//Derive only from this testcase, other GLOBALS references will fail!
//Refer to <http://www.phpunit.de/ticket/497> which has now been fixed -- we await a new release
class TestCase extends PHPUnit_Framework_TestCase
{
	//since PHPUnit global handling is now RETARDED by default
	protected $backupGlobals = false;
	protected $createGlobalsReference = false;
}

require_once dirname( __FILE__ ) . '/gen/schema.inc';
require_once dirname( __FILE__ ) . '/gen/mdb2_schema.inc';

include 'common_test.inc';
include 'dbstest_basic.inc';
include 'dbstest_mdb2.inc';

class DBSchema_AllTests
{
	public static function main()
	{
		global $db_test, $argv;
		
		echo( "Running as MySQLSource...\n" );
		$db_test = new MySQLSource( 'localhost', "dbs_test", 'DBSTestUser', 'password', 'utf-8' );
		$db_test->setErrorLogging( false );
		$ret = PHPUnit_TextUI_TestRunner::run(self::suite(false));
		$okay = $ret->wasSuccessful();
		
		$mdburl_i = array_search( '--mdburl', $argv );
		if( $mdburl_i === false )
		{
			echo( "Skipping MDB2 Test!!!\n" );
			return $okay;
		}
		
		$mdburl = $argv[$mdburl_i+1];
		echo( "Running as MDB2DBSource...\n" );
		@$mdb =& MDB2::factory( $mdburl,
			
			//'mysqli://DBSTestUser:password@localhost/dbs_test',
			/*array(
				'phptype' => 'mysqli',
				'username' => 'DBSTestUser',
				'password' => 'password',
				'hostspec' => 'localhost',
				'database' => 'dbs_test' 
				),*/
			array(
				//setup as utf8 for text columns
				'datatype_map' => array( 'cstring' => 'cstring' ),
				'datatype_map_callback' => array( 'cstring' => 'mdb2_cstring_utf8_callback' ),
				) 
			);
		if( @PEAR::isError( $mdb ) ) 
		{
			error_log( $mdb->getMessage() );
			die( "Unable to create MDB2 DB instance\n" );
		}
		$GLOBALS['mdb'] =& $mdb;
		$db_test = new MDB2DBSource( $mdb, 'cstring' );
		//$db_test->setErrorLogging( false );
		//$mdb->setFetchMode(MDB2_FETCHMODE_ASSOC);	//Just as reference, dbsource doesn't need, nor should it need it
		//check_db_error( $mdb->setCharset( 'UTF8' ) );	//hmmm??? produces an error, MySQL 5 only perhaps?!
		//$mdb->loadModule( 'Extended' );	//also not needed by dbsource
		$ret = PHPUnit_TextUI_TestRunner::run(self::suite(true));
		$okay &= $ret->wasSuccessful();
		
		return $okay;
	}
	
	public static function suite( $directMDB2 )
	{
		$suite = new PHPUnit_Framework_TestSuite( 'DBSchema tests' );
		$suite->addTestSuite( 'DBSTest_Clean' );
		$suite->addTestSuite( 'DBSTest_Basic' );
		if( $directMDB2 )
			$suite->addTestSuite( 'DBSTest_DirectMDB2' );
		return $suite;
	}
}

$ret = DBSchema_AllTests::main();
exit( $ret ? 0 : 1 );

/**
 * To test the function lookup of DB is also working
 */
function &getMDB() { 
	return $GLOBALS['mdb'];
}
?>