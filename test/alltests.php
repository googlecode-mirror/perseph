<?php

require_once 'php_settings.inc';

require_once dirname(__FILE__).'/../php_support/error_handling.inc';

require_once 'PHPUnit/Framework.php';
require_once 'PHPUnit/TextUI/TestRunner.php';
require_once 'PHPUnit/Framework.php';

require_once dirname(__FILE__).'/../php_support/dbsource.inc';
require_once dirname(__FILE__).'/../php_support/mdb2_datatype.inc';
require_once dirname(__FILE__).'/../php_support/form_base.inc';
require_once dirname(__FILE__).'/../php_support/exporter.inc';

//Derive only from this testcase, other GLOBALS references will fail!
//Refer to <http://www.phpunit.de/ticket/497> which has now been fixed -- we await a new release
class TestCase extends PHPUnit_Framework_TestCase
{
	//since PHPUnit global handling is now RETARDED by default
	protected $backupGlobals = false;
	protected $createGlobalsReference = false;
}

$mdburl_i = array_search( '--mdburl', $argv );
if( $mdburl_i === false )
{
	echo( "Skipping MDB2 Test!!!\n" );
	$mdburl = null;
}
else	
	$mdburl = $argv[$mdburl_i+1];

/**
 * Specifies limits per DB type that could alter the test cases
 */
class TestLimit
{
	static public $time24H = false;
}

require_once 'common_test.inc';

if( strpos( $mdburl, 'pgsql:' ) === 0 )
{
	TestLimit::$time24H = true;
	require_once dirname( __FILE__ ) . '/gen/pgsql.schema.inc';
}
else
	require_once dirname( __FILE__ ) . '/gen/schema.inc';
require_once dirname( __FILE__ ) . '/gen/mdb2_schema.inc';

include 'dbstest_basic.inc';
include 'dbstest_mdb2.inc';
include 'dbstest_functions.inc';

$skipCaseTest = false;

class DBSchema_AllTests
{
	public static function main()
	{
		global $db_test, $argv, $mdburl, $skipCaseTest;
		$okay = true;
		
		if( array_search( '--nomysql', $argv ) === false )
		{
			echo( "Running as MySQLSource...\n" );
			$db_test = new MySQLSource( 'localhost', "dbs_test", 'DBSTestUser', 'password', 'utf-8' );
			$db_test->setTimezone( 'America/Vancouver' );
			$db_test->setErrorLogging( false );
			$ret = PHPUnit_TextUI_TestRunner::run(self::suite(false));
			$okay &= $ret->wasSuccessful();
		}
		
		if( array_search( '--nomdb', $argv ) !== false )
			return $okay;
			
		//determine whether to use the DB driver conversion functions or our own
		//must be False For MySQL4. Strangely, if this is "false" when the backing DB has
		//a utf-8 character set the tests will still work -- the DB value will however be
		//corrupt (I'm not sure how to detect this)
		//NOTE: if "false" then the DMB2 textType will need to be set to cstring...
		$useDBCharset = array_search( '--usedbcharset', $argv ) !== false;
		
		$opts = array();
		if( !$useDBCharset )
		{
			//setup as utf8 for text columns
			$opts['datatype_map'] = array( 'cstring' => 'cstring' );
			$opts['datatype_map_callback'] = array( 'cstring' => 'mdb2_cstring_utf8_callback' );
			//the broken combination likely means the backing store can't do case-insensitve searching properly
			$skipCaseTest = true;
		}
		
		echo( "Running as MDB2DBSource...\n" );
		@$mdb =& MDB2::factory( $mdburl, $opts );
		if( @PEAR::isError( $mdb ) ) 
		{
			error_log( $mdb->getMessage() );
			die( "Unable to create MDB2 DB instance\n" );
		}
		$GLOBALS['mdb'] =& $mdb;
		if( $useDBCharset )
			$db_test = new MDB2DBSource( $mdb );
		else	
			$db_test = new MDB2DBSource( $mdb, 'cstring' );
		$db_test->setErrorLogging( false );
		$db_test->setTimezone( 'Pacific/Honolulu' );
		
		if( $useDBCharset )
		{
			$res = $mdb->setCharset( 'utf8' );	//Won't work on MySQL 4, actually the syntax of the name is DB specific it seems
			if( @PEAR::isError( $res ) )
			{
				error_log( $res->getMessage() );
				die( "Unable to set the character set\n" );
			}
		}
		
		//$mdb->loadModule( 'Extended' );	//also not needed by dbsource
		$ret = PHPUnit_TextUI_TestRunner::run(self::suite(true));
		$okay &= $ret->wasSuccessful();
		
		return $okay;
	}
	
	public static function suite( $directMDB2 )
	{
		global $argv;
		
		$skipdb = array_search( '--nodb', $argv ) !== false;
		
		$suite = new PHPUnit_Framework_TestSuite( 'DBSchema tests' );
		$suite->addTestSuite( 'DBSTest_Functions' );
		if( !$skipdb ) {
			$suite->addTestSuite( 'DBSTest_Clean' );
			$suite->addTestSuite( 'DBSTest_Basic' );
			if( $directMDB2 )
				$suite->addTestSuite( 'DBSTest_DirectMDB2' );
		}
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