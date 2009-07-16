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

/* Bool to Integer conversion is rather essential since some DBs expose Bool type as Integers */
function convert_Bool_to_Integer( $val ) { return $val ? 1 : 0; }
function convert_Integer_to_Bool( $val ) { return $val != 0; }

/* Non-conversions */
function convert_Text_to_String( $val ) { return $val; }
function convert_String_to_Text( $val ) { return $val; }
/* Non-conversion for now, maybe a special class is needed in PHP */
function convert_Float_to_Decimal( $val ) { return $val; }
function convert_Decimal_to_Float( $val ) { return $val; }

/* Convert any Null String into an empty string, only on input, output is untouched */
function convert_InStringNull_to_StringEmpty( $val ) { return $val === null ? '' : $val; }
function convert_InStringNull_to_StringEmpty_inv( $val ) { return $val; }

/* Convert empty strings and null on both in and out */
function convert_StringNull_to_StringEmpty( $val ) { return $val === null ? '' : $val; }
function convert_StringNull_to_StringEmpty_inv( $val ) { return strlen( $val ) ? $val : null; }

/* Functions for those still using PHP 5.2 lacking some fundamental date operations */
require_once dirname(__FILE__).'/date_funcs.inc';

/**
 * WARNING: DO NOT USE the data members in this descriptor directly. They are public only
 * since other framework classes need them.  If you need this data use *ONLY* the accessor
 * functions to be shielded from changes
 */
abstract class DBS_TypeDescriptor {
	public $names = array();	//names=> (customtype, basetype, options) of all members, to be overridden in derived class
	public $defaults = array();	//names=>defaults of all members with defaults
	public $aliases = array();	//alias=>name of available aliases
	public $options = array();
	
	public function getFields() {
		return array_keys( $this->names );
	}
	
	public function getBaseType( $field ) {
		return $this->names[$field][1];
	}
	
	public function getCustomType( $field ) {
		return $this->names[$field][0];
	}
	
	public function getDefaultLabel( $field ) {
		$opt = $this->getFieldOption( $field, 'label' );
		if( $opt !== null )
			return $opt;
		return $field;
	}
	
	/**
	 * Returns an option value with the given name. This may be null -- in which
	 * case the default is returned.
	 *
	 * Known options:
	 *		title	=> <Bool> is this a title field (Warning: only ever true, null if false)
	 *		maxLength => <Integer> maximum length of a field
	 *		label => <String> label of the field
	 *		trueName => <String> the true name (not php mangled/converted) of this object
	 */
	public function getFieldOption( $field, $name, $def = null ) {
		if( isset( $this->names[$field][2][$name] ) )
			return $this->names[$field][2][$name];
		return $def;
	}
	
	public function getFieldName( $trueName ) {
		foreach( $this->names as $name => $data )
			if( $trueName === $data[2]['trueName'] )
				return $name;
		throw new Exception( "Unknown truename for field: $trueName" );
	}
	
	/**
	 * As with getFieldOption any of these can be null.
	 * Known options:
	 *		titleField => <Field> which field represents a title
	 */
	public function getOption( $name, $def = null ) {
		if( isset( $this->options[$name] ) )
			return $this->options[$name];
		return $def;
	}
	
	abstract protected function checkType( $field, $value );
}

abstract class DBS_EntityBase {
	protected $_data_type = null; //<DBS_TypeDescriptor> to be set in derived class
	
	public function getType() {
		return $this->_data_type;
	}
	
	const STATUS_UNKNOWN = 0;
	const STATUS_NEW = 1;
	const STATUS_EXTANT = 2;
	const STATUS_DELETED = 3;	//should prevent all operations
	protected $_status = self::STATUS_UNKNOWN;
	
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
	
	/**
	 * Finds the entity in the backing store.
	 *
	 * @param strict [in] if an object is already known to be extant than find will normally
	 *		just accept that and not try to find it again.  Using the strict flag can force this
	 *		logic to be skipped, such that find ensures it is looking for an unknown item.
	 */
	public function find( $strict = false ) {
		if( $this->_status == self::STATUS_EXTANT && !$strict )
			return;
			
		if( $this->_status != self::STATUS_UNKNOWN )
			throw new DBS_LogicException( DBS_LogicException::FIND_NOT_UNKNOWN );
			
		if( !$this->maybeLoad( false ) )
			throw new DBS_DBException( DBS_DBException::NOT_IN_DB, null, $this->getAnyIdentifier() );
		$this->_status = self::STATUS_EXTANT;
	}
	
	/**
	 * Forces a reload from the backing store using the keys of the object.  This
	 * cannot be called if there are modified fields -- they must be resolved first.
	 *
	 * @param strict [in] if an object has not been loaded at all then specifying "true"
	 *		here will cause this function to fail.  Otherwise it will proceed with a normal
	 *		load operation.
	 */
	public function reload( $strict = false ) {
		if( $this->_status == self::STATUS_UNKNOWN && !$strict ) {
			$this->find();
			return;
		}
		
		if( $this->_status != self::STATUS_EXTANT )
			throw new DBS_LogicException( DBS_LogicException::RELOAD_NOT_EXTANT );
			
		if( !$this->maybeLoad( true ) )
			throw new DBS_DBException( DBS_DBException::NOT_IN_DB );
	}
	
	//NOTE: not intended for public use at the moment, only for private use in Persephone!
	public $maybeLoadCallback;	//callback type
	
	/**
	 * Use this to ensure teh status is correctly set all the time, since _maybeLoad
	 * will have to change the status to LOADING.
	 */
	protected function maybeLoad( $reload ) {
		if( $this->maybeLoadCallback !== null )
			call_user_func( $this->maybeLoadCallback );
		$ret = $this->_maybeLoad( $reload );
		if( $ret )
			$this->_status = DBS_EntityBase::STATUS_EXTANT;
		else
			$this->_status = DBS_EntityBase::STATUS_NEW;
		return $ret;
	}
	
	/**
	 * This is to fulfill the behaviour defined by createWith.  It does nothing
	 * more than mark the entity as being new.
	 */
	public function create() {
		if( $this->_status == self::STATUS_NEW )
			return;
			
		if( $this->_status != self::STATUS_UNKNOWN )
			throw new DBS_LogicException( DBS_LogicException::CREATE_NON_UNKNOWN );
		$this->_status = DBS_EntityBase::STATUS_NEW;
	}
	
	/**
	 * Finds the entity in the backing store or creates it if not found -- note that
	 * creating it does not automatically save it in the backing store.
	 */
	public function findOrCreate() {
		//the first two conditions allow for caching of objects and proper chaining from a ::withXXX call
		//in ::findOrCreateWithXXX
		if( $this->_status == self::STATUS_NEW )
			return false;
		if( $this->_status == self::STATUS_EXTANT )
			return true;
			
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
	
	public function isUnknown() {
		return $this->_status === DBS_EntityBase::STATUS_UNKNOWN;
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
	
	/**
	 * Objects in PHP 5 are like C pointers in that the actual object will never actually by
	 * copied in normal semantics, only via a clone operator.  In the persephone sense
	 * this doesn't have a clear meaning and is thus blocked.
	 */
	public function __clone() {
		throw new Exception( "Entity instances cannot be cloned." );
	}
	
	public function __isset( $field ) {
		throw new Exception( "Not supported: ambiguous wrt __defined and __has" );
	}
	public function __unset( $field ) {
		throw new Exception( "Not supported: ambigious wrt __defined and __has" );
	}
	
	/**
	 * Public only for helper functions, not to be used directly!
	 *
	 * Indicates that these fields have been modified by some backend operation, a load,
	 * search, or auto field of some kind.
	 */
	public function __backModified( $fields ) {
		if( $this->backModifiedCallback !== null )
			call_user_func( $this->backModifiedCallback, $fields );
	}
	public $backModifiedCallback = null;
	
	/**
	 * Should not be overridden as it is not the only manner in which an item may
	 * be loaded (search is an alternate method).  Consider using the __backModified
	 * item to watch for changes.
	 *
	 * @param $reload [in] true if item is being reloaded (that is, not for the first time
	 *		as this instance)
	 * @return [out] true if the object was found and loaded, false otherwise
	 */
	abstract protected function _maybeLoad( $reload );
	
	/**
	 * May be overridden.
	 *
	 * @param $adding [in] true if this entity is new and being added, false otherwise
	 * @return [out]
	 */
	abstract protected function _save( $adding );
	
	abstract public function getIdentifier();
}

abstract class DBS_NormalEntityBase extends DBS_EntityBase {
	
	/* a special LOADING case is needed so that __get doesn't incorrectly
		attempt to load data while already loading. */
	protected $_isLoading = false;
	
	protected $_data = array();	//array<name=>Value> to hold the actual field data
	
	//array<name=>Bool> has the field be modified or changed in some way
	// Only "TRUE" will ever be stored, the presence in the array indicates the item is dirty, absence clean
	// this is to save memory by reducing overall values in PHP
	protected $_data_dirty = array();	
	
	protected $_load_keys = null;	//which keys were used to load this instance
	
	protected function __construct() {
		parent::__construct();
	}
	
	private function _fieldName( $field ) {
		if( isset( $this->_data_type->names[ $field ] ) )
			return $field;
		if( isset( $this->_data_type->aliases[ $field ] ) )
			return $this->_data_type->aliases[ $field ];
			
		throw new DBS_FieldException( $field, DBS_FieldException::UNDEFINED );
	}
	
	/**
	 * Indicates whether the field is define on this entity, whether or not
	 * it is actually set (contrast to __has)
	 */
	public function __defined( $field ) {
		return isset( $this->_data_type->names[$field] )
			|| isset( $this->_data_type->aliases[$field] );
	}
	
	public function __get( $field ) {
		if( $field == 'identifier' ) {
			$id = $this->getIdentifier();
			return $id;
		}
		if( $field == 'anyIdentifier' ) {
			$id = $this->getAnyIdentifier();
			return $id;
		}
			
		$field = $this->_fieldName( $field );
			
		if( array_key_exists( $field, $this->_data ) )
			return $this->_data[$field];
			
		//attempt to load if we may already exist
		if( $this->_status === self::STATUS_UNKNOWN && !$this->_isLoading && $this->maybeLoad( false ) ) {
			if( array_key_exists( $field, $this->_data) )	//then try to see if we have the data now
				return $this->_data[$field];
		}
			
		//defaults must come after attempting to load, since real data overrides a default
		if( array_key_exists( $field, $this->_data_type->defaults ) )
			return $this->_data_type->defaults[$field];
			
		throw new DBS_FieldException( $field, DBS_FieldException::UNAVAILABLE );
	}
	
	/**
	 * NOTE: *ALL* sets must come through here to actually set the value!
	 */
	public function __set( $field, $value ) {
		$field = $this->_fieldName( $field );
			
		$this->_data_type->checkType( $field, $value );
		$this->_data[$field] = $value;
		$this->_data_dirty[$field] = true;
	}
	
	public function __markDirty( $field ) {
		$field = $this->_fieldName( $field );
		$this->_data_dirty[$field] = true;
	}
	
	public function __markClean( $field ) {
		$field = $this->_fieldName( $field );
		unset( $this->_data_dirty[$field] );
	}
	
	public function __has( $field ) {
		$field = $this->_fieldName( $field );
			
		return array_key_exists( $field, $this->_data )
			|| array_key_exists( $field, $this->_data_type->defaults );
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
		return array_key_exists( $field, $this->_data_dirty )
			|| ($this->_status == DBS_EntityBase::STATUS_NEW && array_key_exists( $field, $this->_data_type->defaults ) );
	}
	
	/**
	 * Used as a helper function for merges, though it may have a use publically as well.
	 * 
	 * @return [out] true if __isDirty for any field returns true, false otherwise
	 */
	public function __isAnythingDirty() {
		//easiest way for now is to call isDirty on all items
		foreach( $this->_data_type->names as $name => $ignore )
			if( $this->__isDirty( $name ) )
				return true;
		return false;
	}
	
	public function __getTypeData( $field ) {
		$field = $this->_fieldName( $field );
		return $this->_data_type->names[$field];
	}
	
	/**
	 * You may override this function in your custom classes to define pre/post load
	 * operations. Be sure to return the value of the parent class execution.
	 */
	protected function _maybeLoad( $reload ) {
		//allow this not to exist in case the enity has no associated mapper -- strict in memory or temporary entities
		throw new DBS_LogicException( DBS_LogicException::NO_LOAD_DEFINED );
	}
	
	/**
	 * You may override this function in your custom classes to define pre/post save
	 * operations. Be sure to return the value of the parent class execution.
	 */
	protected function _save( $adding ) {
		throw new DBS_LogicException( DBS_LogicException::NO_SAVE_DEFINED );
	}
}

abstract class DBS_MergeEntityBase extends DBS_EntityBase {
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
	const CREATE_NON_UNKNOWN = 8;
	
	static private $codeToMsg = array(
		self::SAVE_INCOMPLETE_LOAD => 'Attempting to save entity resulting from an incomplete load/search',
		self::ONLY_SAVE_EXTANT => "Can only save entities with an Extant status.",
		self::ONLY_ADD_NEW => "Can only add entities with New status.",
		self::NO_LOAD_DEFINED => "No loading mechanism has been defined for this entity.",
		self::NO_SAVE_DEFINED => "No saving mechanism has been defined for this entity.",
		self::FIND_NOT_UNKNOWN => "Find called on non-unknown status",
		self::RELOAD_NOT_EXTANT => "Attempting to reload an entity that is not in/loading from the backing store",
		self::CREATE_NON_UNKNOWN => "Attempting to mark for creation an object with a known status",
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
	const DELETE_FAILED = 7;
	
	static private $codeToMsg = array(
		self::ADD_ALREADY_IN_DB => "Attempting to add an entity that already exists in the DB",
		self::SAVE_NOT_IN_DB => "Attempting to save an entity that is not already in the DB",
		self::LOAD_FAILED => "A load operation has failed",
		self::SAVE_FAILED => "A save operation has failed",
		self::SAVE_ZERO_FIELDS => "A save was attempted with no modified fields, or defaults on add. There is no way to do this with most DBs, thus it isn't supported",
		self::NOT_IN_DB => "Failed to find a record",
		self::DELETE_FAILED => "A delete operation has failed",
		);
		
	public $sql;	//a possible associated SQL statement, or null if none
	public function __construct( $code, $sql = null, $msg = '' ) {
		$fullmsg =  self::$codeToMsg[$code];
		if( strlen($msg))
			$fullmsg .= ': ' . $msg;
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
	const TYPE_DATE = 0x4000;
	const TYPE_STRING = 0x8000;
	const TYPE_ENTITY = 0x10000;
	
	static private $codeToMsg = array(
		self::TYPE_NUMERIC => 'Attempt to set non-numeric value on numeric field',
		self::TYPE_LEN => 'Length exceeds maximum for field',
		self::TYPE_NULL => 'Attempt to set null on non-nullable field',
		self::TYPE_DATE => 'Attempt to set non-Date on Date or DateTime field',
		self::TYPE_STRING => 'Attempt to set non-string convertible value on string field',
		self::TYPE_ENTITY => 'Attempt to set invalid, or non-entity, on entity field',
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

function dbs_cnvfunc_db_to_entity( $entity, $member, $table, $dbname ) {
	$cnv = "_cnv_F{$table}_{$dbname}_T{$member}";
	if( !method_exists( $entity, $cnv ) )
		throw new Exception( "Generated PHP files are invalid, incorrect use, function does not exist: $cnv" );
	return $cnv;
}

function dbs_cnvfunc_entity_to_db( $entity, $member, $table, $dbname ) {
	$cnv = "_cnv_F{$member}_T{$table}_{$dbname}";
	if( !method_exists( $entity, $cnv ) )
		throw new Exception( "Generated PHP files are invalid, incorrect use, function does not exist: $cnv" );
	return $cnv;
}

function _dbs_dbsource_result_acquire( &$db, $result, $into, $table, $fields, $fieldLimit = null ) {
	$modified = array();
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
		$modified[] = $member;
	}
	
	$into->__backModified( $modified );
}

function dbs_dbsource_load( &$db, $table, DBS_EntityBase $into, $keys, $fields ) {
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

function _dbs_dbsource_where( &$db, $table, $fields, DBS_Where_Item $q, $proto ) {
	if( $q instanceof DBS_Where_Member ) {
		//TODO: This should actually be *ALL* matching fields!
		$tuple = _find_member( $q->member, $fields );
		if( $tuple === null )
			throw new Exception( "Unknown field: " . $q->member );
		list( $member, $dbname, $dbtype ) = $tuple;
		$cnv = dbs_cnvfunc_entity_to_db( $proto, $member, $table[1], $dbname );
			
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
				$proto->getType()->checkType( $member, $q->value ); //{LPBug:316730}
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
			$proto->getType()->checkType( $member, $q->pattern );
			$value = str_replace( '*', '%', $db->quote( $q->pattern, 'String' ) );
			
		} else if( $q instanceof DBS_Where_MatchIn ) {
		
			$op = 'IN';
			
			$valuesOut = array();
			$hasValues = false;
			foreach( $q->values as $v ) {
				$hasValues = true;
				$proto->getType()->checkType( $member, $v );
				$valuesOut[] = $db->quote( $proto->$cnv( $v ), $dbtype );
			}
			$value = '(' . implode( ',', $valuesOut ) . ')';
			
			//special case if list is empty then we select nothing (no results is the more preferred option to
			//an exception here -- matches more discussed use cases)
			if( !$hasValues )
				return '1=0';
		} else {
			throw new Exception( "Unknown query item: " . gettype_full( $q ) );
		}
		
		return $db->escapeColumn( $dbname ) . " $op " . $value;
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

function _dbs_dbsource_extract_options( &$db, $table, $fields, $opts, $proto ) {
	$qWhere = null;
	$qSort = null;
	$qLimit = null;
	$qOffset = null;
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
		} else if( $opt instanceof DBS_Offset ) {
			$qOffset = $opt;
		} else if( $opt instanceof DBS_FieldLimiter ) {
			$fieldLimit = $opt->fields;
		} else {
			throw new Exception( "Unknown search query specification: " . gettype_full( $opt ) );
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
		for( $i = 0; $i < count( $qSort->members ); $i++ ) {
			$tuple = _find_member( $qSort->members[$i], $fields );
			if( $tuple === null )
				throw new Exception( "Unknown field: " . $qSort->members[$i] );
			list( $member, $dbname, $dbtype ) = $tuple;
			$columns[] = $db->escapeColumn( $dbname )
				. " {$qSort->mode[$i]}";
		}
		
		$sort = "ORDER BY " 	. implode( ',', $columns );
	} else {
		$sort = '';
	}
	
	$limit = '';
	if( $qLimit !== null )
		$limit .= " LIMIT {$qLimit->limit}";
	if( $qOffset !== null )
		$limit .= " OFFSET {$qOffset->offset}";
		
	return array( $where, $sort, $limit, $fieldLimit );
}

function dbs_dbsource_search( &$db, $table, $item_construct, $search_fields, $load_fields, $opts ) {
	$proto = $item_construct();
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
			
		$this->db->endResult( $this->res );
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
	
	public function current() {
		//PHP: it seems current is called before a call to next in foreach (no docs available on this behaviour however)
		if( $this->start )
			$this->next();
			
		if( !$this->okay )
			throw new Exception( "Attempting to get current item on non-started / completed DB request" );
		
		$c = $this->item_construct;
		$into = $c();
		$into->__declExtant();
		
		_dbs_dbsource_result_acquire( $this->db, $this->res, $into, $this->table, $this->fields, $this->fieldLimit );
		if( !$into->_has_required_load_keys() )
			$into->_logic_block_save = DBS_LogicException::SAVE_INCOMPLETE_LOAD;
		else	
			$into->_set_load_keys( false );	//is this really needed?
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
	//TODO: postgres doesn't support the limit directly, though refer to
	//http://archives.postgresql.org/pgsql-patches/2002-09/msg00260.php
	$proto = $item_construct();
	list( $dbWhere, $dbSort, $dbLimit ) = _dbs_dbsource_extract_options( $db, $table, $fields, $opts, $proto );
	$sql = "DELETE FROM {$db->escapeTable($table[0])} $dbWhere $dbSort $dbLimit";
	$res = $db->exec( $sql );
	if( $res === false )	
		throw new DBS_DBException( DBS_DBException::DELETE_FAILED, $sql, $db->getLastError() );
	$db->endResult( $res );
}

/**
 * Support function for _save created by phpemitter
 *
 */
function dbs_dbsource_save( &$db, $table, DBS_EntityBase $into, $keys, $fields, $lastInsert ) {
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
	
	//use the SET syntax or the other SQL syntax, how to determine from the driver?!?!
	$useSet = !$newRecord;	//UPDATE seems to only use the SET syntax
	
	if( $newRecord )
		$sql = "INSERT INTO {$db->escapeTable($table[0])}";
	else
		$sql = "UPDATE {$db->escapeTable($table[0])}";
		
	if( $useSet )
	{
		$sql .= ' SET ';
		for( $i = 0; $i < count($cols); $i++ ) {
			if( $i )
				$sql .= ', ';
			$sql .= $db->escapeColumn( $cols[$i] );
			$sql .= '=' . $vals[$i];	//already escaped
		}
	}
	else
	{
		$sql .= ' (';
		for( $i = 0; $i < count($cols); $i++ ) {
			if( $i )
				$sql .= ', ';
			$sql .= $db->escapeColumn( $cols[$i] );
		}
		$sql .= ') VALUES (' . join(',',$vals) . ')';
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
		list( $member, $dbname, $dbtype ) = current( $lastInsert );
		
		$id = $db->getNewID( $table[0], $dbname );
		
		if( $into->__has( $member ) )
			throw new Exception( "LastInsert field $member already set in data!" );
		
		$cnv = dbs_cnvfunc_db_to_entity( $into, $member, $table[1], $dbname );
		$value = $into->$cnv( $id );
		$into->__set( $member, $value );
		$into->__markClean( $member );
		$into->__backModified( array( $member ) );
	}
}

/**
 * checks if a variable is convertible, or usable as a text/string type
 */
function is_convertible_to_string( $string ) {
	if( array_search( gettype( $string ), array( 'boolean', 'integer', 'double', 'string', 'NULL' ) ) !== false )
		return true;
	//NOTE: Don't check for __toString since those aren't true strings yet in PHP, they don't behave the same
	//Refer: http://be.php.net/manual/en/migration52.incompatible.php
	return false;
}
?>