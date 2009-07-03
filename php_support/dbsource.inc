<?php
/* ***** BEGIN LICENSE BLOCK *****
 * Version: LGPL 3.0
 * This file is part of Persephone's output and/or part of Persephone.
 *
 * This file is an exception to the main Persephone license in that
 * this file may be redistributed under the terms of the GNU
 * Lesser General Public License, version 3.
 * 
 * Contributors:
 *		edA-qa mort-ora-y <edA-qa@disemia.com>
 * ***** END LICENSE BLOCK ***** */
					  
@require_once 'MDB2.php';
@require_once 'MDB2/Date.php';
//@require_once 'Date.php';

interface DBSource {
	/**
	 * Used to perform read-only queries from the DB which
	 * return data.
	 */
	public function query( $q );
	
	/**
	 * For write operations.
	 */
	public function exec( $q );
	
	public function fetchRow( $res );
	
	public function getResult( $res, $name );
	
	public function decode( $value, $type );
	
	public function quote( $value, $type );
	
	public function endResult( $res );
	
	/**
	 * Escapes a column name for use in SQL. The name given as a parameter
	 * may be a structured name, such as "db.table" in which case it must be
	 * escaped appropriately (usually in parts).  This is of course means that there
	 * is no proper way to escape .'s for now...
	 */
	public function escapeColumn( $column );
	
	public function escapeTable( $table );
	
	public function getNewID( $table = null, $field = null );
	
	/**
	 * Allows the disabling (or reenabling) of error logging. By default DB errors
	 * will be logged using error_log
	 */
	public function setErrorLogging( $on );
	
	/**
	 * Returns the textual form of the last error which occurred.
	 */
	public function getLastError( );
}

class MDB2DBSource implements DBSource {

	private $mdb;
	private $textType;
	private $timezone;
	
	/**
	 *
	 * @param textType [in] speciifying a type other than 'text' allows you to use a custom
	 * 	custom text conversion, useful in cases where the backend/transport is not
	 *		charset aware and you need special conversions. Refer to the alltests.php for an
	 *		example of this.
	 *		NOTE: If your transport is character set aware, then you can use the setCharset
	 *		function of MDB2 and use the default 'text' type instead.
	 */
	public function __construct( MDB2_Driver_Common &$mdb, $textType = 'text' ) {
		$this->mdb =& $mdb;
		$this->textType = $textType;
		
		$this->timezone = new DateTimeZone( date_default_timezone_get() );
	}
	
	public function &getMDB() {
		return $this->mdb;
	}
	
	public function setTimezone( $tz ) {
		if( !($tz instanceof DateTimeZone) )
			$tz = new DateTimeZone( $tz );
		$this->timezone = $tz;
	}
	
	public function getTimezone( $tz ) {
		return $this->timezone;
	}
	
	/** 
	 * This function is mainly meant for the MDB2 direct mode in persephone to cache
	 * a DBSource object but replace the MDB2.
	 */
	public function switchMDB( MDB2_Driver_Common &$mdb ) {
		$this->mdb =& $mdb;
	}
	
	public function checkError( &$item ) {
		@$failed = PEAR::isError( $item );
		if( !$failed )
			return true;
			
		$this->lastError = $item->getMessage();
		if( $this->errorLogging )
			error_log( $this->lastError );
		return false;
	}
	
	private $errorLogging = true;
	public function setErrorLogging( $on ) {
		$this->errorLogging = $on;
	}
	
	private $lastError;
	public function getLastError( ) {
		return $this->lastError;
	}
	
	public function query( $q ) {
		$res = $this->mdb->query( $q );
		if( !$this->checkError( $res ) )
			return false;
			
		return new MDB2Result( $res );
	}
	
	public function exec( $q ) {
		$res = $this->mdb->exec( $q );
		if( !$this->checkError( $res ) )
			return false;
			
		return $res;
	}
	
	public function fetchRow( $res ) {
		//to allow people not to check the result of query
		if( $res === false )
			return false;
		$res->currow = $res->mdbres->fetchRow(MDB2_FETCHMODE_ASSOC);
		if( $res->currow === null )
			return false;
		return $this->checkError( $res->currow );
	}
	
	public function getResult( $res, $name ) {
		return $res->currow[strtolower($name)];
	}
	
	const TEXTTYPE = '_textType';
	static private $typeMap = array( 
		'string' => self::TEXTTYPE,
		'text' => self::TEXTTYPE,
		'decimal' => 'decimal',
		'integer' => 'integer',
		'float' => 'float',
		'date' => 'date',
		'time' => 'time',
		'datetime' => 'timestamp',
		'bool' => 'boolean'
		);
	private function getMDBType( $type ) {
		$type = strtolower( $type );
		if( !isset( self::$typeMap[$type] ) )
			throw new Exception( "Unsupported quote type: $type" );
			
		$type = self::$typeMap[$type];
		if( $type === self::TEXTTYPE )
			return $this->textType; 
		return $type;
	}
	
	public function decode( $value, $type ) {
		$mtype = $this->getMDBType( $type );
		
		//datatype may not yet be initialized (lazy init with quote it appears)
		if( !isset( $this->mdb->datatype ) )
			$this->mdb->loadModule('Datatype', null, true);
		$halfraw = $this->mdb->datatype->convertResult( $value, $mtype );
		
		if( $value === null )
			return $value;
			
		switch( strtolower( $type ) ) {
			case 'decimal':
				$out = floatval( $halfraw );	//MDB leaves them as strings (probably correct, but well...)
				break;
				
			case 'date':
			case 'datetime':
				$out = $this->mdb2_DateToDate( $value );
				break;
				
			case 'time':
				$out = _dbs_decode_time( $value );
				break;
				
			default:
				$out = $halfraw;
				break;
		}
		
		return $out;
	}
	
	public function quote( $value, $type ) {
		$mtype = $this->getMDBType( $type );
					
		if( $value === null ) {
			$halfraw = null;
		} else {
				
			switch( strtolower( $type ) ) {
				case 'date':
				case 'datetime':
					$halfraw = $this->dateToMDB2_Date( $value );
					break;
					
				case 'time':
					$halfraw = _dbs_encode_time( $value );
					break;
					
				default:
					$halfraw = $value;
					break;
			}
		}
		
		$q = $this->mdb->quote( $halfraw, $mtype );
		if( $this->checkError( $q ) )
			return $q;
			
		throw new Exception( "Could not convert type/value: $type" );
	}
	
	public function endResult( $res ) {
		if( $res instanceof MDB2Result )
			$res->mdbres->free();
	}
	
	public function escapeColumn( $column ) {
		return $this->mdb->quoteIdentifier( $column );
	}
	
	public function escapeTable( $table ) {
		return $this->mdb->quoteIdentifier( $table );
	}
	
	public function getNewID( $table = null, $field = null ) {
		return $this->mdb->lastInsertID( $table, $field );
	}
	
	public function dateToMDB2_Date( $date ) {
		$ndate = clone $date;
		$ndate->setTimezone( $this->timezone );
		return $ndate->format( 'Y-m-d H:i:s' );	//though the default, be explicit, this is what MDB2 timestamps are
	}
	
	public function mdb2_DateToDate( $mdate ) {
		return new DateTime( $mdate, $this->timezone );
	}
}

class MDB2Result {
	public $mdbres;
	public $currow;
	
	public function __construct( &$mdbres ) {
		$this->mdbres =& $mdbres;
	}
}

///////////////////////////////////////////////////////////////////////////////////////////////////
// DEPRACATED WARNING
//
// The classes below expose more than they should according to
// the interface.  These need to be cleaned up and/or replaced.
// The MDB2 method is likely to be the long-term preferred option.
					  
/* The class structure seems a little unusual here, each fucntion the parent
 * explicitly calls the child class function.  This is since the parent class
 * is really the main class, and the child is just a Driver, not really meant
 * to be called directly -- using the same mechanism for all functions
 * allows consistancy.
 */
abstract class DBSourceBase implements DBSource {

	var $connect;
	var $isinit;
	var $str_enc;   //the string encoding used in the DB (what is returned raw)
	
	private $timezone;

	public function setTimezone( $tz ) {
		if( !($tz instanceof DateTimeZone) )
			$tz = new DateTimeZone( $tz );
		$this->timezone = $tz;
	}
	
	public function getTimezone( $tz ) {
		return $this->timezone;
	}
	
	/* The default encoding is Windows-1252 since most of the system have an
	 * Access front-end which seems to be using this encoding, at least initially 
	 *
	 * PHP: Should be "protected", but then can't have public in derived classes
	 */
	public function __construct( $astr_enc = "windows-1252" ) {
		$this->connect = NULL;
		$this->isinit = False;
		$this->str_enc = $astr_enc;
		$this->timezone = new DateTimeZone( date_default_timezone_get() );
	}

	public function fetchRow( $res ) {
		return $this->fetch_row( $res );
	}
	
	public function endResult( $res ) {
		return $this->endresult( $res );
	}
	
	function init( ) {
		if( $this->isinit )
			return;

		$this->connect = $this->int_connect();
		if( $this->connect == 0 )
			die( "Cannot connect to " . $this->name );
		$this->isinit = True;
	}

	function deinit( ) {
		if( $this->isinit ) {
			$this->int_close();
			$this->isinit = False;
		}
	}

	/**
	 * Wrapper to execute queries by calling the exec method
	 *
	 * The exec method of the driver class is called to execute this
	 * function.
	 *
	 * If an error occurs the program will break (by calling the
	 * Error_handler)
	 */
	function query( $q ) {
		$this->init();

		$ret = $this->int_exec( $q );
		if( $ret === false ) {
			$this->lastError = "Could not execute query: $q: " . $this->int_errormsg();
			if( $this->errorLogging )
				error_log( $this->lastError );
		}

		return $ret;
	}

	private $errorLogging = true;
	public function setErrorLogging( $on ) {
		$this->errorLogging = $on;
	}
	
	private $lastError;
	public function getLastError( ) {
		return $this->lastError;
	}

	function exec( $q ) {
		return $this->query( $q );
	}

	function getResult( $res, $col ) {
		return $this->int_result( $res, $col );
	}
	
	/**
	 * @deprecated use getResult
	 */
	function result( $res, $col ) {
		return $this->int_result( $res, $col );
	}	 

	/**
	 * @return  [out] reference to a created result set. Each call
	 *  to fetch_resultset produces a new copy
	 */
	function &fetch_resultset( $res, $rowNum = null ) {
		//map to new unified function with appropriate params
		return $this->allresults( $res,
			array(
				'row_name' => $rowNum
			) );
	}
	function &allresults( $res, $opts ) {
		return $this->int_allresults( $res, $opts );
	}

	function fetch_row( $res ) {
		return $this->int_fetch_row( $res );
	}

	/**
	 * Helper function, since we don't know which encoding the DB has
	 * this converets from DB encoding to PHP string encoding.
	 *
	 * @deprecated use decode (though internal still uses this)
	 */
	function decode_str( $str ) {
		return mb_convert_encoding( $str, mb_internal_encoding(), $this->str_enc );
	}

	/**
	 * @deprecated use quote
	 */
	function encode_str( $str ) {
		return mb_convert_encoding( $str, $this->str_enc );
	}

	/**
	 * @deprecated use quote
	 */
	function escape_sql_str( $str ) {
		die("Unsupported!");
	}

	/**
	 * @deprecated use quote
	 */
	function escape_encode_str( $str ) {
		return $this->escape_sql_str( $this->encode_str( $str ) );
	}

	function escape_sql_blob( $data ) {
		die("Unsupported!");
	}

	public function getNewID( $table = null, $field = null ) {
 		die("Unsupported!");
 	}

	function escapeColumn( $column ) {
		die("Unsupported!");
	}
		 
	public function escapeTable( $table ) {
		return $this->escapeColumn( $table );
	}
	
	/**
	 * Returns a bracketed clause for the specified ids (as numbers)
	 *
	 * @param ids   [in] array of ids
	 * @return  [out] SQL bracketed,comma'd clause
	 *
	 * @deprecated use the SQL class or something else
	 */
	function get_in_for_ids( $ids ) {
		$ret = '(';
		$c = 0;
		foreach( $ids as $id ) {
			if( $c )
				$ret .= ',';
			$ret .= $id;
			$c++;
		}
		$ret .= ')';
		return $ret;
	}
	
	//MDB2 like interface, used in the DBSchema code
	function quote( $value, $type ) {	
		if( $value === null )
			return 'NULL';
			
		switch( strtolower( $type ) ) {
			case 'string':
			case 'text':
				return '\'' . $this->escape_encode_str( $value ) . '\'';
			case 'integer':
				return intval( $value );
			case 'decimal':
			case 'float':
				return floatval( $value );
			case 'datetime': {
				$nvalue = clone $value;
				$nvalue->setTimezone( $this->timezone );
				return '\'' . $value->format( "Y-m-d H:i:s" ) . '\'';
			} case 'date':
				return '\'' . $value->format( "Y-m-d" ) . '\'';
			case 'time':
				return '\'' . _dbs_encode_time( $value ) . '\'';
			case 'bool':
				return $value ? 1 : 0;	//TODO: MYSQL/Oracle specific, Postgres uses True/false!
			default:
				throw new Exception( "Unrecognized quote type: $type" );
		}
	}
	
	function decode( $value, $type ) {
		if( $value === null )
			return null;
			
		switch( strtolower( $type ) ) {
			case 'string':
			case 'text':
				return $this->decode_str( $value );
			case 'integer':
				return intval( $value );
			case 'decimal':
			case 'float':
				return floatval( $value );
			case 'datetime':
			case 'date':
				//remove trailing milliseconds if there (quick and dirty... *sigh* new PHP should parse them)		
				$dot = strrpos( $value, '.' );
				if( $dot !== false )
					$value = substr( $value, 0, $dot );
			
				$ret = new DateTime( $value, $this->timezone );
				return $ret;
				
			case 'time':
				return _dbs_decode_time( $value );
				
			case 'bool':
				return $value == '1' || strtolower( $value ) === 'true';
			default:
				throw new Exception( "Unrecognized decode type: $type" );
		}
	}
	
	function result_query( $query ) {
		return new DBResult( $this, $this->query( $query ) );
	}
}

function _dbs_decode_time( $value ) {
	if( !strlen( $value ) )
		return $value;
	if( $value[0] == '-' ) {
		$neg = true;
		$value = substr( $value, 1 );
	} else
		$neg = false;
	
	$parts = explode( ':', $value );
	if( count( $parts ) != 3 )	
		return null;
		
	$ret = $parts[0] * 3600 + $parts[1] * 60 + $parts[2];
	if( $neg )
		$ret = -$ret;
	return $ret;
}

function _dbs_encode_time( $value ) {
	if( $value < 0 ) {
		$neg = true;
		$value = -$value;
	} else
		$neg = false;
	$ret = sprintf( "%d:%02d:%02d", floor($value/3600), floor($value/60) % 60, $value % 60 );
	if( $neg )
		$ret = '-' . $ret;
	return $ret;
}

//NOTE: This is not used anymore is it...?
class ODBCSource extends DBSourceBase {

	var $name;
	var $user;
	var $pass;

	public function __construct( $aname, $auser, $apass, $astr_enc = "windows-1252" ) {
		$this->name = $aname;
		$this->user = $auser;
		$this->pass = $apass;

		parent::__construct( $astr_enc );
	}

	function int_exec( $q ) {
		return odbc_exec( $this->connect, $q );
	}

	function int_errormsg( ) {
		return odbc_errormsg();
	}

	function int_close() {
		return odbc_close( $this->connect );
	}

	function int_connect() {
		return odbc_connect( $this->name, $this->user, $this->pass );
	}

	function &int_allresults( $res, $opts = null ) {
		return odbc_fetch_resultset( $res, $opts );
	}

	function int_result( $res, $col ) {
		return odbc_result( $res, $col );
	}

	function int_fetch_row( $res ) {
		return odbc_fetch_row( $res );
	}

	function escape_sql_str( $str ) {
		return str_replace( "'", "''", $str );
	}

	function escape_sql_blob( $data ) {
		die("Unsupported!");
	}

	function endresult( $res ) {
	}
}

class MySQLSource extends DBSourceBase {

	var $server;
	var $name;
	var $user;
	var $pass;

	var $curRow;
	var $curNames;
	var $mapRes;	//maps ids to results
	var $refCount = 1;

		
	/* Queries will be scanned syntax %TABLE[tablename] and be translated
	 * into just tablename.  This allows the translation of table names in
	 * queries while maintaining a readable syntax.  The sytnax is additionally
	 * chosen to prevent the string from accidentally occuring anywhere
	 * else in a query.  (It can't exist in SQL raw and the escape_str function
	 * *should* escape such a sequence -- TODO: it doesn't now, %'s are ignored...)).
	 */
	var $ucaseTables = false;   

	public $enableCharsetNames = 'utf8';	//use to set the Names communication value (false is to use default is used)
	
	function __construct( $aserver, $aname, $auser, $apass, $astr_enc = "windows-1252" ) {
		$this->server = $aserver;
		$this->name = $aname;
		$this->user = $auser;
		$this->pass = $apass;

		$this->curRow = array();
		$this->curNames = array();
		$this->mapRes = array();   

		parent::__construct( $astr_enc );
	}

	function int_exec( $q ) {
		$res = mysql_query( $this->translate_query( $q ), $this->connect );
		if( !$res )
			return false;//so a direct comparison works.
		$ref = $this->refCount++;
		$this->mapRes[ $ref] = $res;
		$this->curRow[ $ref ] = null;
		$this->curNames[ $ref ] = null;
		return $ref;
	}

	function int_errormsg( ) {
		return mysql_error();
	}

	function int_close() {
		return mysql_close( $this->connect );
	}

	function int_connect() {
		$result = mysql_connect( $this->server, $this->user, $this->pass, true  ) or die( "<p class='error'>MySql Connect: $this->server/$this->name: " . mysql_error() );
		mysql_select_db( $this->name, $result ) or die( "<p class='error'>MySql Select: $this->name: " . mysql_error() );		
		if( $this->enableCharsetNames !== false )
			mysql_query( "SET NAMES {$this->enableCharsetNames}", $result);
		return $result;
	}

	function &int_allresults( $ref, $opts = null ) {
		return mysql_fetch_resultset( $this->mapRes[ $ref ], $opts );
	}

	function int_result( $ref, $col ) {
		$res = $this->mapRes[ $ref ];
		if( is_null( $this->curRow[ $ref ] ) )
			$this->curRow[ $ref ] = $this->_get_row( $ref );

		$row =& $this->curRow[ $ref ];

		if( is_int( $col ) )
			return $row[ $col - 1 ];	//normal DB 1-based, mysql is 0-based
		else {
			$names =& $this->curNames[ $ref ];
			if( is_null( $names ) ) {
				$names = array();
				$fCount = mysql_num_fields( $res );
				for( $i=0; $i < $fCount; $i++)
					$names[ strtoupper( mysql_field_name( $res, $i ) ) ] = $i;

				$this->curNames[ $ref ] =& $names;
			}
			return $row[ $names[ strtoupper( $col ) ] ];
		}
	}

	function int_fetch_row( $ref ) {
		$res = $this->_get_row( $ref );
		if( !$res ) 
			return false;
		return true;
	}

	function _get_row( $ref ) {
		$res = $this->mapRes[ $ref ];
		$row = mysql_fetch_row( $res );
		$this->curRow[ $ref ] = $row;
		return $row;
	}
	
	function escape_sql_str( $str ) {
		$this->init(); //we need a connection
		return mysql_real_escape_string( $str, $this->connect );
	}

	function escape_sql_blob( $data ) {
		$this->init(); //we need a connection
		return mysql_real_escape_string( $data, $this->connect );
	}

	public function getNewID( $table = null, $field = null ) {
		return mysql_insert_id( $this->connect );
	}
	
	function escapeColumn( $column ) {
		$parts = explode( '.', $column );
		foreach( $parts as $key => $col )
			$parts[$key] = '`' . $this->escape_sql_str( $col ) . '`';
		return implode('.',$parts);
	}	
	
	function translate_query( $sql ) {
		if( $this->ucaseTables ) {
			$reg = '@\%TABLE\[([^\]]*)\]@';
			$ret = preg_replace_callback(
				$reg,
				create_function( '$matches',
					'return strtoupper($matches[1]);'
					),	
				$sql
				);
			return $ret;
		} else {
			return $sql;
		}
	}
	
	function endresult( $ref ) {
		//PHP: for some queries the query API returns a boolean instead of an object...
		$res = $this->mapRes[ $ref ];
		if( !is_bool( $res ) )
			mysql_free_result( $res );
		unset( $this->mapRes[$ref] );
		unset( $this->curRow[$ref] );	//clean up row data as well
		unset( $this->curNames[$ref] );
	}
}

class PGSQLSource extends DBSourceBase {

	var $server;
	var $name;
	var $user;
	var $pass;

	var $curRow;
	var $curNames;	//TODO: use ref System as in MySql (otherwise memory problem?)

	//The mapRes system is also used in MySQL, perhaps it should be abstracted..
	var $mapRes;	//maps ids to results
	
	function __construct( $aserver, $aname, $auser, $apass, $astr_enc = "windows-1252" ) {
		$this->server = $aserver;
		$this->name = $aname;
		$this->user = $auser;
		$this->pass = $apass;

		$this->curRow = array();
		$this->curNames = array();

		$this->mapRes = array();   
		array_push( $this->mapRes, "Junk" );	//to ensure id=0 is never used
		parent::__construct( $astr_enc );
	}

	function int_exec( $q ) {
		$res = pg_query( $this->connect, $q );
		$ref = array_push( $this->mapRes, $res ) - 1;
		$this->curRow[ $ref ] = null;
		$this->curNames[ $ref ] = null;
		if( !$res )
			return false;
		return $ref;
	}

	function int_errormsg( ) {
		return pg_last_error( $this->connect );
	}

	function int_close() {
		return pg_close( $this->connect );
	}

	function int_connect() {
		$connstr = "host='$this->server' dbname='$this->name' user='$this->user' password='$this->pass'";
		$result = pg_connect( $connstr  );
		return $result;
	}

	function &int_allresults( $res, $opts = null ) {
		die("Unsupported!");
	}

	function int_result( $ref, $col ) {
		$res = $this->mapRes[$ref];
		if( is_null( $this->curRow[ $ref ] ) )
			$this->curRow[ $ref ] = $this->_get_row( $ref );

		$row =& $this->curRow[ $ref ];

		if( is_int( $col ) )
			return $row[ $col - 1 ];	//normal DB 1-based, postgres is 0-based
		else {
			$names =& $this->curNames[ $ref ];
			if( is_null( $names ) ) {
				$names = array();
				$fCount = pg_num_fields( $res );
				for( $i=0; $i < $fCount; $i++)
					$names[ strtoupper( pg_field_name( $res, $i ) ) ] = $i;

				$this->curNames[ $ref ] =& $names;
			}
			return $row[ $names[ strtoupper( $col ) ] ];
		}
	}

	function int_fetch_row( $ref ) {
		$res = $this->_get_row( $ref );
		if( !$res )
			return false;
		return true;
	}
	
	function _get_row( $ref ) {
		$res = $this->mapRes[ $ref ];
		$row = pg_fetch_row( $res );
		$this->curRow[ $ref ] = $row;
		return $row;
	}

	function escape_sql_str( $str ) {
		//TODO: does this actually escape special characters as well?
		$this->init(); //we need a connection
		return pg_escape_string( $this->connect, $str );
	}

	function escape_sql_blob( $data ) {
		$this->init(); //we need a connection
		return pgl_escape_bytea( $this->connect, $data );
	}

	//TODO: this is copied from MySQL, does it work here too?	
	function escapeColumn( $column ) {
		$parts = explode( '.', $column );
		foreach( $parts as $key => $col )
			$parts[$key] = '`' . $this->escape_sql_str( $col ) . '`';
		return implode('.',$parts);
	}	
	
	function endresult( $ref ) {
		pg_free_result( $this->mapRes[$ref] );
		unset( $this->curNames[$ref] );
		unset( $this->curRow[$ref] );
	}
}

class OCISQLSource extends DBSourceBase {

	var $server;
	var $name;
	var $user;
	var $pass;

	var $curRow;
	var $curNames;

	function __construct( $aserver, $aname, $auser, $apass, $astr_enc = "iso-8859-1" ) {
		$this->server = $aserver;
		$this->name = $aname;
		$this->user = $auser;
		$this->pass = $apass;

		$this->curRow = array();
		$this->curNames = array();

		parent::__construct( $astr_enc );
	}

	function int_exec( $q ) {
		$sm = oci_parse( $this->connect, $q );
		$res = oci_execute( $sm );
		$this->curRow[ $sm ] = null;
		$this->curNames[ $sm ] = null;
		return $sm; //unlike other dbs we return the result of parse, and not execute
	}

	function int_errormsg( ) {
		return oci_error( $this->connect );
	}

	function int_close() {
		return oci_close( $this->connect );
	}

	function int_connect() {
		$result = oci_connect( $this->user, $this->pass, "//$this->server/$this->name" ); //TODO: use str_enc here?
		return $result;
	}

	function &int_allresults( $res, $opts = null ) {
		die("Unsupported!");
	}

	function int_result( $res, $col ) {
		if( is_null( $this->curRow[ $res ] ) )
			$this->curRow[ $res ] = $this->int_fetch_row( $res );

		$row =& $this->curRow[ $res ];

		if( is_int( $col ) )
			return $row[ $col ];	//oracle DB 1-based
		else {
			$names =& $this->curNames[ $res ];
			if( is_null( $names ) ) {
				$names = array();
				$fCount = oci_num_fields( $res );
				for( $i=0; $i < $fCount; $i++)
					$names[ strtoupper( oci_field_name( $res, $i+1 ) ) ] = $i;

				$this->curNames[ $res ] =& $names;
			}
			return $row[ $names[ strtoupper( $col ) ] ];
		}
	}

	function int_fetch_row( $res ) {
		$row = oci_fetch_row( $res );
		$this->curRow[ $res ] = $row;
		return $row;
	}

	function escape_sql_str( $str ) {
		//TODO: does this actually escape special characters as well?
		$this->init(); //we need a connection
		return pg_escape_string( $this->connect, $str );
	}

	function escape_sql_blob( $data ) {
		$this->init(); //we need a connection
		return pgl_escape_bytea( $this->connect, $data );
	}

	//TODO: this is copied from MySQL, does it work here too?	
	function escapeColumn( $column ) {
		$parts = explode( '.', $column );
		foreach( $parts as $key => $col )
			$parts[$key] = '`' . $this->escape_sql_str( $col ) . '`';
		return implode('.',$parts);
	}	
	
	function endresult( $res ) {
		oci_free_statement( $res );
		unset( $this->curNames[$ref] );
		unset( $this->curRow[$ref] );
	}
}

/**
 * Return all the rows returned by a query in an array.
 *   Array index will be the column name (lowercase -- though
 *   fieldName will be preserved as is)
 *
 *   Note: Resulting set will have each row as an item plus
 *   one additional row for the names.  So  the number of returned
 *   DB results is also count(result) - 1
 *
 *   @param opts [in] map of options, default is false if not set
 *	  'row_name'  => name of row to use as index for returned array
 *	  'keep_case' => maintain the case of the fields, otherwise all lowercase
 *
 * @result  [out] is an array of all rows in the resultSet
 *	  n = 1 ... number of rows returned
 *
 *	  if( row_name )
 *		  [column row_name of n] => rowdata
 *	  else
 *		  [n] => rowdata
 *  
 *	  rowdata = array( column_name_X => column_value_X )
 */
function &odbc_fetch_resultset($resID, $opts = null )
{
	$resultSet = array();

	$rowName = get_option( 'row_name', $opts, null );
	$keep_case = get_option( 'keep_case', $opts, false );

	//get the names
	$fNames = array();
	$fCount = odbc_num_fields($resID);
	for ($i=1; $i <= $fCount; $i++) {
		$fNames[$i] = odbc_field_name($resID, $i);
	}

	for ($i=1; odbc_fetch_row($resID,$i); $i++) {
		unset( $record );
		$record = array();
		for ($j = 1; $j <= $fCount; $j++) {
			$fName = $keep_case
				? odbc_field_name($resID, $j)
				: strtolower( odbc_field_name($resID, $j) );
			$record[$fName] = odbc_result($resID, $j);
		}

		if( !is_null( $rowName )  ) {
			$index =& $record[$rowName];
			$resultSet[ $index ] =& $record;
		} else
			$resultSet[$i] =& $record;
	}


	return $resultSet;
}

function &mysql_fetch_resultset($resID, $opts = null )
{
	$resultSet=array();

	$rowName = get_option( 'row_name', $opts, null );
	$keep_case = get_option( 'keep_case', $opts, false );

	//get the names
	$fNames = array();
	$fCount = mysql_num_fields($resID);
	for ($i=0; $i < $fCount; $i++) {
		$fNames[$i] = mysql_field_name($resID, $i);
	}

	$i = 0;
	while( $row = mysql_fetch_row( $resID ) ) {
		unset( $record );
		$record = array();

		for ($j = 0; $j < $fCount; $j++) {
			$fName = $keep_case
				? $fNames[ $j ]
				: strtolower( $fNames[ $j ] );
			$record[$fName] = $row[ $j ];
		}

		if( !is_null( $rowName )  ) {
			$index = $record[$rowName];
			$resultSet[ $index ] =& $record;
		} else
			$resultSet[ $i + 1 ] =& $record;

		$i++;
	}


	return $resultSet;
}

/**
 * Abstracts the use of result data, in general making it easier to
 * work with results.
 */
class DBResult {
	var $result;	//result from the DB
	var $db;	//db result came from

	function DBResult( &$db, $result ) {
		$this->result = $result;
		$this->db =& $db;
	}

	/**
	 * Returns a raw result
	 */
	function result( $name ) {
		return $this->db->getResult( $this->result, $name );
	}

	function decode( $name, $type ) {
		return $this->db->decode( $this->result( $name ), $type );
	}
	
	function endResult() {
		$ret = $this->db->endResult( $this->result );
		unset( $this->result );
		return $ret;
	}
	
	/**
	 * Returns the string value of the given column name/index
	 */
	function string( $name ) {
		$raw = $this->db->getResult( $this->result, $name );
		if( is_null( $raw ) )
			return null;
		return $this->db->decode( $raw, 'string' );
	}

	/**
	 * Returns an integer result
	 */
	function integer( $name ) {
		$raw = $this->db->getResult( $this->result, $name );
		if( is_null( $raw ) )
			return null;
		return intval( $raw );
	}

	/**
	 * Returns a float result
	 */
	function float( $name ) {
		$raw = $this->db->getResult( $this->result, $name );
		if( is_null( $raw ) )
			return null;
		return floatval( $raw );
	}
	
	/**
	 * Returns a PHP timestamp for the date
	 */
	function date( $name ) {
		$raw = $this->db->getResult( $this->result, $name );
		if( is_null( $raw ) )
			return null;

		//remove trailing milliseconds if there (quick and dirty... *sigh* new PHP should parse them)		
		$dot = strrpos( $raw, '.' );
		if( $dot !== false )
			$raw = substr( $raw, 0, $dot );
			
		return strtotime( $raw );
	}

	/**
	 * Returns a PHP timestamp for the date
	 */
	function datetime( $name ) {
		return $this->date( $name );
	}
	
	/**
	 * Returns a PHP timestampe from a retrieved timestamp
	 */
	function timestamp( $name ) {
		$str = $this->db->getResult( $this->result, $name );
		if( is_null( $str ) )
			return null;
			
		//TODO: This might be MySQL specific
		$year = substr($str,0,4);
		$mon  = substr($str,4,2);
		$day  = substr($str,6,2);
		$hour = substr($str,8,2);
		$min  = substr($str,10,2);
		$sec  = substr($str,12,2);
		return mktime($hour,$min,$sec,$mon,$day,$year);
	}

	/**
	 * Returns a boolean value from the result
	 */
	function boolean( $name ) {
		$raw = $this->db->getResult( $this->result, $name );
		if( is_null( $raw ) )
			return null;
		if( is_bool( $raw ) ) 
			return $raw;
		return intval( $raw ) != 0;
	}
		 
	/**
	 * You can use this to determine if there are any results.
	 * if( $dbr->fetch_row() ) { ...result...}
	 * But you don't need to use it, the first result-set will be
	 * implicity retrieved on a first call to a previous function
	 */
	function fetch_row() {
		return $this->db->fetchRow( $this->result );
	}
	
	/**
	 * Used by data_formatter to indicate the "getter" of the
	 * current row.  For our implementation this is just
	 * ourselves.
	 */
	function obtain_getter() {
		return $this;
	}	 
}

?>