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

require_once dirname(__FILE__).'/base.inc';
require_once dirname(__FILE__).'/dbsource.inc';

/* Some common functions used in the schems -- these could be implemented direclty in the processor/
	converter, but it is easier to define them here. */
/* TypeConvert should really be done in the converter as it should check the types! */
function TypeConvert( $value ) { return $value; }
function TypeConvert_inv( $value ) { return $value; }


/**
 * Wraps a reference for assignment.
 */
class DBS_Ref {
	public $ref;
	
	public function __construct( &$ref ) {
		$this->ref =& $ref;
	}
}

/**
 * TODO: Ensure these things are actually copy/clone safe.  Currently all data is stored within arrays
 * which are never reallocated, so in theory the *real* objects are always passed by reference (as deep
 * copies are not done?)
 * Some variables are however not arrays, and these need to be handled correctly.
 */
abstract class DBS_EntityBase {
	
	const STATUS_UNKNOWN = 0;
	const STATUS_NEW = 1;
	const STATUS_EXTANT = 2;
	const STATUS_DELETED = 3;	//should prevent all operations
	
	/* a special LOADING case is needed so that __getref doesn't incorrectly
		attempt to load data while already loading. */
	protected $_isLoading = false;
	
	protected $_status = self::STATUS_UNKNOWN;
	
	protected $_data = array();	//to hold the actual field data
	protected $_data_has = array();	//fields which are actually set (to distinguish null as a real value)
	protected $_data_dirty = array();	//has the field be modified or changed in some way
				
	protected $_data_names = array();	//names=>types of all members, to be overridden in derived class
	protected $_data_defaults = array();	//names=>defaults of all members with defaults
	protected $_data_aliases = array();	//alias=>name of available aliases
	
	protected $_load_keys = null;	//which keys were used to load this instance
	
	//public only for helpers
	public $_logic_block_save = null;	//a reason (code from DBS_LogicException) why save can't be performed
		
	protected function __construct() {
	}
	
	/**
	 * NOTE: This should not be used, it is a private support function.
	 */
	public function __declExtant() {
		$this->_status = self::STATUS_EXTANT;
	}
	
	private function _fieldName( $field ) {
		if( isset( $this->_data_names[ $field ] ) )
			return $field;
		if( isset( $this->_data_aliases[ $field ] ) )
			return $this->_data_aliases[ $field ];
			
		throw new DBS_FieldException( $field, DBS_FieldException::UNDEFINED );
	}
	
	/**
	 * Indicates whether the field is define on this entity, whether or not
	 * it is actually set (contrast to __has)
	 */
	public function __defined( $field ) {
		return isset( $this->_data_names[$field] )
			|| isset( $this->_data_aliases[$field] );
	}
	
	public function &__getref( $field ) {
		$field = $this->_fieldName( $field );
			
		if( array_get_default( $field, $this->_data_has, false ) )
			return $this->_data[$field];
			
		//attempt to load if we may already exist
		if( $this->_status === self::STATUS_UNKNOWN && !$this->_isLoading && $this->maybeLoad( false ) ) {
			if( array_get_default( $field, $this->_data_has, false ) )	//then try to see if we have the data now
				return $this->_data[$field];
		}
			
		//defaults must come after attempting to load, since real data overrides a default
		if( array_key_exists( $field, $this->_data_defaults ) )
			return $this->_data_defaults[$field];
			
		throw new DBS_FieldException( $field, DBS_FieldException::UNAVAILABLE );
	}
	
	public function __get( $field ) {
		return $this->__getref( $field );
	}
	
	/**
	 * NOTE: *ALL* sets must come through here to actually set the value!
	 */
	public function __set( $field, $value ) {
		$field = $this->_fieldName( $field );
			
		if( $value instanceof DBS_Ref ) {
			$this->_checkType( $field, $value->ref );
			$this->_data[$field] =& $value->ref;
		} else {
			$this->_checkType( $field, $value );
			$this->_data[$field] = $value;
		}
		$this->_data_has[$field] = true;
		$this->_data_dirty[$field] = true;
	}
	
	public function __markDirty( $field ) {
		$field = $this->_fieldName( $field );
		$this->_data_dirty[$field] = true;
	}
	
	public function __markClean( $field ) {
		$field = $this->_fieldName( $field );
		$this->_data_dirty[$field] = false;
	}
	
	public function __has( $field ) {
		$field = $this->_fieldName( $field );
			
		return array_get_default( $field, $this->_data_has, false )
			|| array_key_exists( $field, $this->_data_defaults );
	}
	
	public function __isset( $field ) {
		throw new Exception( "Not supported: ambiguous wrt __defined and __has" );
	}
	public function __unset( $field ) {
		throw new Exception( "Not supported: ambigious wrt __defined and __has" );
	}
	
	/**
	 * Checks if a field is *effectively* dirty. This means that the field has been modified, or is
	 * otherwise different than what the persisted form might be.
	 *
	 * Note that if the entity is new then default fields are considered dirty, since they may not
	 * have the same default value in the backing store.
	 */
	public function __isDirty( $field ) {
		if( $this->_status == self::STATUS_UNKNOWN )
			throw new Exception( "isDirty is ambiguous when status is unknown" );
		$field = $this->_fieldName( $field );
		return array_get_default( $field, $this->_data_dirty, false )
			|| ($this->_status == DBS_EntityBase::STATUS_NEW && array_key_exists( $field, $this->_data_defaults ) );
	}
	
	public function __getTypeData( $field ) {
		$field = $this->_fieldName( $field );
		return $this->_data_names[$field];
	}
	
	/**
	 * Finds the entity in the backing store.
	 */
	public function find() {
		if( $this->_status != self::STATUS_UNKNOWN )
			throw new DBS_LogicException( DBS_LogicException::FIND_NOT_UNKNOWN );
			
		if( !$this->maybeLoad( false ) )
			throw new DBS_DBException( DBS_DBException::NOT_IN_DB );
		$this->_status = self::STATUS_EXTANT;
	}
	
	/**
	 * Forces a reload from the backing store using the keys of the object.  This
	 * cannot be called if there are modified fields -- they must be resolved first.
	 */
	public function reload() {
		if( $this->_status != self::STATUS_EXTANT )
			throw new DBS_LogicException( DBS_LogicException::RELOAD_NOT_EXTANT );
			
		if( !$this->maybeLoad( true ) )
			throw new DBS_DBException( DBS_DBException::NOT_IN_DB );
	}
	
	/**
	 * Use this to ensure teh status is correctly set all the time, since _maybeLoad
	 * will have to change the status to LOADING.
	 */
	protected function maybeLoad( $reload ) {
		$ret = $this->_maybeLoad( $reload );
		if( $ret )
			$this->_status = DBS_EntityBase::STATUS_EXTANT;
		else
			$this->_status = DBS_EntityBase::STATUS_NEW;
		return $ret;
	}
	
	/**
	 * Finds the entity in the backing store or creates it if not found -- not that
	 * creating it does not automatically save it in the backing store.
	 */
	public function findOrCreate() {
		if( $this->_status != self::STATUS_UNKNOWN )
			throw new Exception( "FindOrCreate called on non-unknown status" );
			
		return $this->maybeLoad( false);
	}
	
	public function add() {
		if( $this->_status != DBS_EntityBase::STATUS_NEW )
			throw new DBS_LogicException( DBS_LogicException::ONLY_ADD_NEW );
		$this->_blockSave( true );
	}
	
	public function save() {
		if( $this->_status != DBS_EntityBase::STATUS_EXTANT )
			throw new DBS_LogicException( DBS_LogicException::ONLY_SAVE_EXTANT );
		$this->_blockSave( false );
	}
	
	private function _blockSave( $adding ) {
		if( $this->_logic_block_save !== null )
			throw new DBS_LogicException( $this->_logic_block_save );
		$this->_save( $adding );
	}
	
	public function isNew() {
		return $this->_status === DBS_EntityBase::STATUS_NEW;
	}
	
	public function isExtant() {
		return $this->_status === DBS_EntityBase::STATUS_EXTANT;
	}
	
	public function exists() {
		if( $this->_status == DBS_EntityBase::STATUS_EXTANT )
			return true;
		if( $this->_status != DBS_EntityBase::STATUS_UNKNOWN )
			return false;
			
		return $this->maybeLoad( false );
	}
	
	/**
	 * TODO: Should only be called if loaded via a findOrCreate method, may
	 * produce exception in future if another sequence is followed
	 */
	public function saveOrAdd() {
		if( $this->_status == DBS_EntityBase::STATUS_NEW )
			$this->add();
		else
			$this->save();
	}
	
	protected function _maybeLoad( $reload ) {
		//allow this not to exist in case the enity has no associated mapper -- strict in memory or temporary entities
		throw new DBS_LogicException( DBS_LogicException::NO_LOAD_DEFINED );
	}
	
	protected function _save( $adding ) {
		throw new DBS_LogicException( DBS_LogicException::NO_SAVE_DEFINED );
	}
	
	abstract protected function _checkType( $field, $value );
}

/**
 * A base class for the set of exceptions generated by the dbs code.
 * This will never be directly instantiated.
 */
class DBS_Exception extends ErrorException {
	public function __construct( $msg, $code ) {
		parent::__construct( $msg, $code );
	}
}

/**
 * Logic exceptions are generated when the series of function calls/sets
 * do not yield a logically consistent behaviour.  That is, you have attempted
 * to do something which doesn't make sense, or would be ambiguous.
 */
class DBS_LogicException extends DBS_Exception {
	const SAVE_INCOMPLETE_LOAD = 1;
	const ONLY_SAVE_EXTANT = 2;
	const ONLY_ADD_NEW = 3;
	const NO_LOAD_DEFINED = 4;
	const NO_SAVE_DEFINED = 5;
	const FIND_NOT_UNKNOWN = 6;
	const RELOAD_NOT_EXTANT = 7;
	
	static private $codeToMsg = array(
		self::SAVE_INCOMPLETE_LOAD => 'Attempting to save entity resulting from an incomplete load/search',
		self::ONLY_SAVE_EXTANT => "Can only save entities with an Extant status.",
		self::ONLY_ADD_NEW => "Can only add entities with New status.",
		self::NO_LOAD_DEFINED => "No loading mechanism has been defined for this entity.",
		self::NO_SAVE_DEFINED => "No saving mechanism has been defined for this entity.",
		self::FIND_NOT_UNKNOWN => "Find called on non-unknown status",
		self::RELOAD_NOT_EXTANT => "Attempting to reload an entity that is in the backing store",
		);
	public function __construct( $code ) {
		parent::__construct( self::$codeToMsg[$code], $code );
	}
}

class DBS_DBException extends DBS_Exception {
	const ADD_ALREADY_IN_DB = 1;
	const SAVE_NOT_IN_DB = 2;
	const LOAD_FAILED = 3;
	const SAVE_FAILED = 4;
	const SAVE_ZERO_FIELDS = 5;
	const NOT_IN_DB = 6;
	
	static private $codeToMsg = array(
		self::ADD_ALREADY_IN_DB => "Attempting to add an entity that already exists in the DB.",
		self::SAVE_NOT_IN_DB => "Attempting to save an entity that is not already in the DB.",
		self::LOAD_FAILED => "A load operation has failed.",
		self::SAVE_FAILED => "A save operation has failed.",
		self::SAVE_ZERO_FIELDS => "A save was attempted with no modified fields, or defaults on add. There is no way to do this with most DBs, thus it isn't supported.",
		self::NOT_IN_DB => "Failed to find a record.",
		);
		
	public $sql;	//a possible associated SQL statement, or null if none
	public function __construct( $code, $sql = null, $msg = '' ) {
		$fullmsg =  self::$codeToMsg[$code] . $msg;
		if( $sql !== null )
			$fullmsg .= ": $sql";
		parent::__construct( $fullmsg, $code );
		$this->sql = $sql;
	}
}

/**
 * Field exceptions indicate a failure in operations relating to a specific field.
 * While in some cases they may seem to be more like Logic exceptions, the
 * deciding criteria is the relation to a specific field.
 */
class DBS_FieldException extends DBS_Exception {
	const SAVE_LOAD_ONLY = 1;
	const UNDEFINED = 2;
	const UNAVAILABLE = 3;
	const MISSING_REQ = 4;
	const SET_FIELD = 5;	//OR'd with one of the SetField types
	const LOAD_DIRTY = 6;
	
	static private $codeToMsg = array(
		self::SAVE_LOAD_ONLY => "Attempt to save LOAD_ONLY field",
		self::UNDEFINED => "Field not defined",
		self::UNAVAILABLE => "Field not available on this instance",
		self::MISSING_REQ => "Required field for operation not specified",
		self::LOAD_DIRTY => "Attempting to load into dirty field.",
		);
	public $field; //<String> the field on which the exception occurred
	
	public function __construct( $field, $code = 0, $msg = null ) {
		$this->field = $field;
		parent::__construct( 
			$msg === null  ? self::$codeToMsg[$code] . ":$field" : $msg,  
			$code 
			);
	}
}

class DBS_SetFieldException extends DBS_FieldException {
	
	const TYPE_MASK = 0xF000;
	const TYPE_NUMERIC = 0x1000;
	const TYPE_LEN = 0x2000;
	const TYPE_NULL = 0x3000;
	
	static private $codeToMsg = array(
		self::TYPE_NUMERIC => 'Attempt to set non-numeric value on numeric field',
		self::TYPE_LEN => 'Length exceeds maximum for field',
		self::TYPE_NULL => 'Attempt to set null on non-nullable field',
		);
		
	public function getType() {
		return $this->getCode() & self::TYPE_MASK;
	}
	
	public function __construct( $field, $code ) {
		parent::__construct( $field, $code | DBS_FieldException::SET_FIELD, self::$codeToMsg[$code] . ':' . $field );
	}
}

/**
 * STRUCTURE NOTES
 *
 * $table : array( db_table_name, internal_table_name )
 * 	The values differ when a prefix is being used.
 *
 *
 * $fields/$keys : array( 
 *		array( membername, dbname, dbtype [, $value ] )
 *		...
 *		)
 *
 * The membername may be repeated multiple times if multiple relations exist (not in all situations
 * however). $value exists during "_save"
 */

/**
 * Should the field be skipped.
 */
function _dbs_skipfield( $member, $fieldLimit ) {
	if( $fieldLimit === null )
		return false;
		
	return array_search( $member, $fieldLimit ) === false;
}

function _dbs_dbsource_sql_col( &$db, $fields, $fieldLimit = null ) {
	$cols = '';
	foreach( $fields as $tuple ) {
		list( $member, $dbname, $dbtype ) = $tuple;
		if( _dbs_skipfield( $member, $fieldLimit ) )
			continue;
			
		if( strlen( $cols ) )
			$cols .= ', ';
		$cols .= $db->escapeColumn( $dbname );
	}
	
	return $cols;
}

function dbs_cnvfunc_db_to_entity( &$entity, $member, $table, $dbname ) {
	$cnv = "_cnv_F{$table}_{$dbname}_T{$member}";
	if( !method_exists( $entity, $cnv ) )
		throw new Exception( "Generated PHP files are invalid, incorrect use, function does not exist: $cnv" );
	return $cnv;
}

function dbs_cnvfunc_entity_to_db( &$entity, $member, $table, $dbname ) {
	$cnv = "_cnv_F{$member}_T{$table}_{$dbname}";
	if( !method_exists( $entity, $cnv ) )
		throw new Exception( "Generated PHP files are invalid, incorrect use, function does not exist: $cnv" );
	return $cnv;
}

function _dbs_dbsource_result_acquire( &$db, &$result, &$into, $table, $fields, $fieldLimit = null ) {
	foreach( $fields as $tuple ) {
		list( $member, $dbname, $dbtype ) = $tuple;
		if( _dbs_skipfield( $member, $fieldLimit ) )
			continue;
					
		if( $into->isExtant() && $into->__isDirty( $member ) )
			throw new DBS_FieldException( $member, DBS_FieldException::LOAD_DIRTY );
			
		$cnv = dbs_cnvfunc_db_to_entity( $into, $member, $table[1], $dbname );
		$value = $into->$cnv( $db->decode( $db->getResult( $result, $dbname ), $dbtype ) );
		$into->__set( $member, $value );
		$into->__markClean( $member );
	}
}

function dbs_dbsource_load( &$db, $table, DBS_EntityBase &$into, $keys, $fields ) {
	$where = '';
	foreach( $keys as $tuple ) {
		list( $member, $dbname, $dbtype ) = $tuple;
		if( strlen( $where ) )
			$where .= ' AND ';
			
		$cnv = dbs_cnvfunc_entity_to_db( $into, $member, $table[1], $dbname );
		$value = $into->$cnv( $into->__get( $member ) );
		if( $value === null )
			$where .= $db->escapeColumn( $dbname ) . ' IS NULL';
		else
			$where .= $db->escapeColumn( $dbname ) . ' = ' . $db->quote( $value, $dbtype );
	}	
	
	$cols = _dbs_dbsource_sql_col( $db, $fields );
	$sql = "SELECT $cols FROM {$db->escapeTable($table[0])} WHERE $where";
	$res = $db->query( $sql );
	if( !$db->fetchRow( $res ) ) {
		$db->endResult( $res );
		return false;
	}
	 
	_dbs_dbsource_result_acquire( $db, $res, $into, $table, $fields );
	
	$db->endResult( $res );
	return true;
}

function _find_member( $member, $fields ) {
	foreach( $fields as $tuple ) {
		if( $tuple[0] === $member )
			return $tuple;
	}
	return null;
}

function _dbs_dbsource_where( &$db, $table, $fields, DBS_Where_Item $q, &$proto ) {
	if( $q instanceof DBS_Where_Member ) {
		//TODO: This should actually be *ALL* matching fields!
		$tuple = _find_member( $q->member, $fields );
		if( $tuple === null )
			throw new Exception( "Unknown field: " . $q->member );
		list( $member, $dbname, $dbtype ) = $tuple;
			
		if( $q instanceof DBS_Where_Match ) {
			if( $q->value === null ) {
				//special null wackiness
				if( $q->op == '=' ) {
					$op = 'IS';
					$value = 'NULL';
				} else if( $q->op == '!=' ) {
					$op = 'IS NOT';
					$value = 'NULL';
				} else
					throw new Exception( "NULL can only be matched with = or !=" );
			} else {
				$cnv = dbs_cnvfunc_entity_to_db( $proto, $member, $table[1], $dbname );
				$value = $proto->$cnv( $q->value );
			
				$op = $q->op;	//TODO: Check for correctness
				$value = $db->quote( $value, $dbtype );
			}
		} else if( $q instanceof DBS_Where_MatchString ) {
			if( $dbtype !== 'String' && $dbtype !== 'Text' )
				throw new Exception( 'MatchString can only be used with string/text columns, attempted: ' . $dbtype );
				
			if( $q->positive )
				$op = ' LIKE ';
			else
				$op = ' NOT LIKE ';
				
			//TODO: What if the quote escapes the * char?
			$value = str_replace( '*', '%', $db->quote( $q->pattern, 'String' ) );
		} else {
			throw new Exception( "Unknown query item: " . gettype_full( $q ) );
		}
		
		return $db->escapeColumn( $dbname ) . $op . $value;
	} 
	
	if( $q instanceof DBS_Where_MatchSQL )
		return $q->sql;
		
	if( $q instanceof DBS_Where_Group ) {
		$buf = " ( ";
		for( $i =0; $i < count( $q->members); $i++ ) {
			if( $i )
				$buf .= " {$q->type} ";
			$buf .= _dbs_dbsource_where( $db, $table, $fields, $q->members[$i], $proto );
		}
		$buf .= " ) ";
		return $buf;
	}
	
	throw new Exception( "Unknown query item: " . gettype_full( $q ) );
}

function _dbs_dbsource_extract_options( &$db, $table, $fields, $opts, &$proto ) {
	$qWhere = null;
	$qSort = null;
	$qLimit = null;
	$fieldLimit = null;
	
	//Extract options
	$qWhere = null;
	foreach( $opts as $opt ) {
		if( $opt instanceof DBS_Where_Item ) {
			if( $qWhere !== null )	
				throw new Exception( "Duplicate where specification" );
			$qWhere = $opt;
			
		} else if( $opt instanceof DBS_Sort_Item ) {
			if( $qSort !== null )
				throw new Exception ( "Duplicate sort specification" );
			$qSort = $opt;
		} else if( $opt instanceof DBS_Limit ) {
			$qLimit = $opt;
		} else if( $opt instanceof DBS_FieldLimiter ) {
			$fieldLimit = $opt->fields;
		} else {
			throw new Exception( "Unknown specification: " . gettype_full( $opt ) );
		} 
	}
	
	//produce where clause
	if( $qWhere !== null ) {
		if( $qWhere instanceof DBS_Where_MatchAll )
			$where = '';
		else
			$where = 'WHERE ' . _dbs_dbsource_where( $db, $table, $fields, $qWhere, $proto );
	} else {
		throw new Exception( "Operation requires a match specification" );
	}
	
	//produce sort clause
	if( $qSort !== null ) {
		if( !( $qSort instanceof DBS_Sort_Single ) )
			throw new Exception( "Unknown sort item: " . get_class( $qSort ) );
		
		$columns = array();
		foreach( $qSort->members as $sorton ) {
			$tuple = _find_member( $sorton, $fields );
			if( $tuple === null )
				throw new Exception( "Unknown field: " . $sorton );
			list( $member, $dbname, $dbtype ) = $tuple;
			$columns[] = $db->escapeColumn( $dbname );
		}
		
		$sort = "ORDER BY " 
			. implode( ',', $columns )
			. " {$qSort->mode}";
	} else {
		$sort = '';
	}
	
	if( $qLimit !== null ) {
		$limit = " LIMIT {$qLimit->limit}";
		if( $qLimit->offset != 0 )
			$limit .= " OFFSET {$qLimit->offset}";
	} else {
		$limit = '';
	}
	return array( $where, $sort, $limit, $fieldLimit );
}

function dbs_dbsource_search( &$db, $table, $item_construct, $search_fields, $load_fields, $opts ) {
	$proto =& $item_construct();
	list( $dbWhere, $dbSort, $dbLimit, $fieldLimit ) = _dbs_dbsource_extract_options( $db, $table, $search_fields, $opts, $proto );

	$cols = _dbs_dbsource_sql_col( $db, $load_fields, $fieldLimit );
	$sql = "SELECT $cols FROM {$db->escapeTable($table[0])} $dbWhere $dbSort $dbLimit";
	$res = $db->query( $sql );
	if( $res === false )
		throw new DBS_DBException( DBS_DBException::LOAD_FAILED, $sql );
	return new _DBS_DBSource_Result_Iterator( $db, $res, $item_construct, $table, $load_fields, $fieldLimit );
}

class _DBS_DBSource_Result_Iterator implements Iterator {
	private $table;
	private $item_construct;
	private $fields;
	private $res;
	private $fieldLimit;
	private $db;
	
	private $okay = true;
	private $start = true;
	
	public function __construct( &$db, &$res, $item_construct, $table, $fields, $fieldLimit ) {
		$this->db =& $db;
		$this->table = $table;
		$this->res =& $res;
		$this->item_construct = $item_construct;
		$this->fields = $fields;
		$this->fieldLimit = $fieldLimit;
	}	
	
	/**
	 * Allows user code to indicate they are done with the results of
	 * the search operation.  This allows the code to recover/free
	 * resources.
	 */
	public function endSearch() {
		//if not okay, assume we had an auto-end after next(), so don't throw exception
		if( !$this->okay )
			return;
			
		$this->db->endresult( $this->res );
		$this->okay = false;
	}
	
	/**
	 * Allows complete loading of all results into an array. The iterator is thus invalidated.
	 *
	 * @param key [in] if specified the index of the returned array will be the given member
	 *		field, otherwise (if null) normal array extension is used
	 * @param member [in] if specified this member will be loaded as the value rather than
	 *		the entity itself
	 */
	public function loadAll( $key = null, $member = null ) {
		if( !$this->start )	
			throw new Exception( "loadAll is only meant to be called on a full result" );
			
		$ret = array();
		foreach( $this as $item ) {
			if( $key === null )
				$ret[] = $member === null ? $item : $item->$member;
			else
				$ret[$item->$key] = $member === null ? $item : $item->$member;
		}
		return $ret;
	}
	
	public function &current() {
		//PHP: it seems current is called before a call to next in foreach (no docs available on this behaviour however)
		if( $this->start )
			$this->next();
			
		if( !$this->okay )
			throw new Exception( "Attempting to get current item on non-started / completed DB request" );
		
		$c = $this->item_construct;
		$into =& $c();
		$into->__declExtant();
		
		_dbs_dbsource_result_acquire( $this->db, $this->res, $into, $this->table, $this->fields, $this->fieldLimit );
		if( !$into->_set_load_keys( false ) )
			$into->_logic_block_save = DBS_LogicException::SAVE_INCOMPLETE_LOAD;
		return $into;
	}
	
	public function key() {
		throw new Exception( "Search results are not keyed" );
	}
	
	public function next() {
		if( !$this->okay )
			throw new Exception( "Attempting to call next on completed/invalid db result" );
			
		$this->okay = (bool)$this->db->fetchRow( $this->res );
		$this->start = false;
		
		//if we're done now we can cleanup
		if( !$this->okay )
			$this->endSearch();
	}
	
	public function rewind() {
		//PHP: foreach appears to call rewind when being used in a foreach loop
		if( !$this->start )
			throw new Exception( "Rewind unsupported on DB search results" );
		//PHP: expects us to be on the first element after rewind
		$this->next();
	}
	
	public function valid() {
		return $this->okay;
	}
}

function dbs_dbsource_delete( &$db, $table, $item_construct, $fields, $opts ) {
	$proto =& $item_construct();
	list( $dbWhere, $dbSort, $dbLimit ) = _dbs_dbsource_extract_options( $db, $table, $fields, $opts, $proto );
	$sql = "DELETE FROM {$db->escapeTable($table[0])} $dbWhere $dbSort $dbLimit";
	$res = $db->exec( $sql );
	//TODO: Check errors
	$db->endResult( $res );
}

/**
 * Support function for _save created by phpemitter
 *
 */
function dbs_dbsource_save( &$db, $table, DBS_EntityBase &$into, $keys, $fields, $lastInsert ) {
	$cols = array();
	$vals = array();
	$keycols = array();
	$keyvals = array();
	$clean = array();	//saved members will be marked as clean after saving
	
	foreach( $fields as $tuple ) {
		list( $member, $dbname, $dbtype ) = $tuple;
		if( !$into->__isDirty( $member ) )
			continue;
			
		$clean[] = $member;
		$cnv = dbs_cnvfunc_entity_to_db( $into, $member, $table[1], $dbname );
		$cols[] = $dbname;
		$vals[] = $db->quote( $into->$cnv( $into->__get( $member ) ), $dbtype );
	}
	
	if( count( $cols ) == 0 )
		throw new DBS_DBException( DBS_DBException::SAVE_ZERO_FIELDS );
		
	foreach( $keys as $tuple ) {
		list( $member, $dbname, $dbtype, $value ) = $tuple;
		
		$cnv = dbs_cnvfunc_entity_to_db( $into, $member, $table[1], $dbname );
		//don't pass null's to quote, since it actually changes the syntax, quoting won't help :(
		$unquoted = $into->$cnv( $value );
		$keyvals[] = $unquoted === null ? null : $db->quote( $unquoted, $dbtype );
		$keycols[] = $dbname;
	}
	
	//if key based we must check for existence first
	if( count( $keycols ) ) {
		$keywhere = '';
		for( $i = 0; $i < count($keycols); $i++ ) {
			if( $i )
				$keywhere .= ' AND ';
			$keywhere .= $db->escapeColumn( $keycols[$i] );
			if( $keyvals[$i] === null )
				$keywhere .= ' IS NULL';
			else
				$keywhere .= '=' . $keyvals[$i];
		}
		$sql = "SELECT Count(*) AS Count FROM {$db->escapeTable($table[0])} WHERE $keywhere";
		$res = $db->query( $sql );
		$db->fetchRow( $res );
		$newRecord = $db->decode( $db->getResult( $res, 'count' ), 'integer' ) == 0; //TODO: perhaps assert == 1?
		$db->endResult( $res );
	} else {
		$newRecord = true;
	}
		
	//for a new record insert keys as well as values
	//NOTE: hmm, not needed now as keys are already in the columns if modified...
	//if( $newRecord ) {
	//	$cols = array_merge( $cols, $keycols );
	//	$vals = array_merge( $vals, $keyvals );
	//}
	
	//we check the "adding" status to ensure newRecord matches what we expect?
	if( $newRecord !== $into->isNew() )
		throw new DBS_DBException( $newRecord ?  DBS_DBException::SAVE_NOT_IN_DB : DBS_DBException::ADD_ALREADY_IN_DB );
	
	if( $newRecord )
		$sql = "INSERT {$db->escapeTable($table[0])}  SET ";
	else
		$sql = "UPDATE {$db->escapeTable($table[0])} SET ";
	for( $i = 0; $i < count($cols); $i++ ) {
		if( $i )
			$sql .= ', ';
		$sql .= $db->escapeColumn( $cols[$i] );
		$sql .= '=' . $vals[$i];	//already escaped
	}
	 
	if( !$newRecord ) {
		$sql .= " WHERE $keywhere";
	}
	
	$res = $db->exec( $sql );
	if( $res === false )	
		throw new DBS_DBException( DBS_DBException::SAVE_FAILED, $sql );
	$db->endResult( $res );
	
	//clean all saved fields
	foreach( $clean as $cl )
		$into->__markClean( $cl );
		
	//if we are using the lastInsert mechanism, then handle it here
	if( $newRecord && $lastInsert !== null ) {
		$id = $db->getNewID();
		
		list( $member, $dbname, $dbtype ) = current( $lastInsert );
		
		if( $into->__has( $member ) )
			throw new Exception( "LastInsert field $member already set in data!" );
		
		$cnv = dbs_cnvfunc_db_to_entity( $into, $member, $table[1], $dbname );
		$value = $into->$cnv( $id );
		$into->__set( $member, $value );
		$into->__markClean( $member );
	}
}

?>