<?php
/* ***** BEGIN LICENSE BLOCK *****
 * Version: LGPL 3.0
 * This file is part of Persephone's output and/or part of Persephone.
 *
 * This file is an exception to the main Persephone license in that
 * this file may be redistributed under the terms of the GNU
 * General Public License, version 3.
 * 
 * Contributors:
 *		edA-qa mort-ora-y <edA-qa@disemia.com>
 * ***** END LICENSE BLOCK ***** */

require_once dirname(__FILE__).'/base.inc';
require_once dirname(__FILE__).'/dbsource.inc';

/**
 * Wraps a reference for assignment.
 */
class DBS_Ref {
	public $ref;
	
	public function __construct( &$ref ) {
		$this->ref =& $ref;
	}
}

abstract class DBS_EntityBase {
	
	const STATUS_UNKNOWN = 0;
	const STATUS_NEW = 1;
	const STATUS_EXTANT = 2;
	const STATUS_DELETED = 3;	//should prevent all operations
	
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
	 * Allows specifically saying the object should be treated as a new entity now. Useful
	 * in entities without primary keys to reuse the object to add multiple items.
	 */
	public function __declNew() {
		$this->_status = self::STATUS_NEW;
	}
	
	/**
	 * This can be used in situations where you wish to save/chagne a field and do not
	 * need to load the data before hand. It should be limited to optimization scenarios
	 * only.
	 */
	public function __declExtant() {
		$this->_status = self::STATUS_EXTANT;
	}
	
	/**
	 * Allows specifically stating the status of the object is unknown.  This should not 
	 * ever really be needed and is used now strictly to makeup for limitations in the
	 * DBS System.
	 */
	public function __declUnknown() { 
		$this->_status = self::STATUS_UNKNOWN;
	}
	
	private function _fieldName( $field ) {
		if( isset( $this->_data_names[ $field ] ) )
			return $field;
		if( isset( $this->_data_aliases[ $field ] ) )
			return $this->_data_aliases[ $field ];
			
		throw new DBS_FieldException( $field, DBS_FieldException::UNDEFINED );
	}
	
	public function &__getref( $field ) {
		$field = $this->_fieldName( $field );
			
		if( array_get_default( $field, $this->_data_has, false ) )
			return $this->_data[$field];
			
		//attempt to load if we may already exist
		if( $this->_status === self::STATUS_UNKNOWN && $this->_maybeLoad() ) {
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
		throw new Exception( "Not supported" );
	}
	public function __unset( $field ) {
		throw new Exception( "Not supported" );
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
	
	public function find() {
		if( $this->_status != self::STATUS_UNKNOWN )
			throw new Exception( "Find called on non-unknown status" );
			
		if( !$this->_maybeLoad() )
			throw new Exception( "Failed to find a matching record." );
		$this->_status = self::STATUS_EXTANT;
	}
	
	public function findOrCreate() {
		if( $this->_status != self::STATUS_UNKNOWN )
			throw new Exception( "FindOrCreate called on non-unknown status" );
			
		if( $this->_maybeLoad() )
			$this->_status = DBS_EntityBase::STATUS_EXTANT;
		else
			$this->_status = DBS_EntityBase::STATUS_NEW;
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
	
	public function exists() {
		if( $this->_status == DBS_EntityBase::STATUS_EXTANT )
			return true;
		if( $this->_status != DBS_EntityBase::STATUS_UNKNOWN )
			return false;
			
		if( $this->_maybeLoad() ) {
			$this->_status = DBS_EntityBase::STATUS_EXTANT;
			return true;
		} else {
			$this->_status = DBS_EntityBase::STATUS_NEW;
			return false;
		}
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
	
	abstract protected function _maybeLoad();
	
	abstract protected function _save( $adding );
	
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
	
	static private $codeToMsg = array(
		self::SAVE_INCOMPLETE_LOAD => 'Attempting to save entity resulting from an incomplete load/search',
		self::ONLY_SAVE_EXTANT => "Can only save entities with an Extant status.",
		self::ONLY_ADD_NEW => "Can only add entities with New status.",
		);
	public function __construct( $code ) {
		parent::__construct( self::$codeToMsg[$code], $code );
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
	
	static private $codeToMsg = array(
		self::SAVE_LOAD_ONLY => "Attempt to save LOAD_ONLY field",
		self::UNDEFINED => "Field not defined",
		self::UNAVAILABLE => "Field not available on this instance",
		self::MISSING_REQ => "Required field for operation not specified",
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
	foreach( $fields as $member => $data ) {
		if( _dbs_skipfield( $member, $fieldLimit ) )
			continue;
			
		if( strlen( $cols ) )
			$cols .= ', ';
		$cols .= $db->escapeColumn( $data[0] );
	}
	
	return $cols;
}

function _dbs_dbsource_result_acquire( &$db, &$result, &$into, $table, $fields, $fieldLimit = null ) {
	foreach( $fields as $member => $data ) {
		if( _dbs_skipfield( $member, $fieldLimit ) )
			continue;
		
		list( $dbname, $dbtype ) = $data;
		$cnv = "_cnv_F{$table[1]}_{$dbname}_T{$member}";
		
		$value = $into->$cnv( $db->decode( $db->getResult( $result, $dbname ), $dbtype ) );
		$into->__set( $member, $value );
		$into->__markClean( $member );
	}
}

/**
 * @params keys [in] membername => (dbname,dbtype)
 * @params fields [in] membername => (dbname,dbtype)
 */
function dbs_dbsource_load( &$db, $table, DBS_EntityBase &$into, $keys, $fields ) {
	$where = '';
	foreach( $keys as $member => $data  ) {
		list( $dbname, $dbtype ) = $data;
		if( strlen( $where ) )
			$where .= ' AND ';
			
		$cnv = "_cnv_F{$member}_T{$table[1]}_{$dbname}";
		$value = $into->$cnv( $into->__get( $member ) );
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

function _dbs_dbsource_where( &$db, $table, $fields, DBS_Where_Item $q, &$proto ) {
	if( $q instanceof DBS_Where_Member ) {
		if( !isset( $fields[$q->member] ) )
			throw new Exception( "Unknown field: " . $q->member );
			
		if( $q instanceof DBS_Where_Match ) {
			$cnv = "_cnv_F{$q->member}_T{$table[1]}_{$fields[$q->member][0]}";
			$value = $proto->$cnv( $q->value );
			
			$op = $q->op;	//TODO: Check for correctness
			$value = $db->quote( $value, $fields[$q->member][1] );
		} else if( $q instanceof DBS_Where_MatchString ) {
			if( $fields[$q->member][1] !== 'String' && $fields[$q->member][1] != 'Text' )
				throw new Exception( 'MatchString can only be used with string/text columns, attempted: ' . $fields[$q->member][1] );
				
			if( $q->positive )
				$op = ' LIKE ';
			else
				$op = ' NOT LIKE ';
				
			//TODO: What if the quote escapes the * char?
			$value = str_replace( '*', '%', $db->quote( $q->pattern, 'String' ) );
		} else {
			throw new Exception( "Unknown query item: " . gettype_full( $q ) );
		}
		
		return $db->escapeColumn( $fields[$q->member][0] ) . $op . $value;
	} 
	
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
		
		if( !isset( $fields[$qSort->member] ) )
			throw new Exception( "Unknown field: " . $qSort->member );
		$sort = "ORDER BY " 
			. $db->escapeColumn( $fields[$qSort->member][0] )
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

function dbs_dbsource_search( &$db, $table, $item_construct, $fields, $opts ) {
	$proto =& $item_construct();
	list( $dbWhere, $dbSort, $dbLimit, $fieldLimit ) = _dbs_dbsource_extract_options( $db, $table, $fields, $opts, $proto );

	$cols = _dbs_dbsource_sql_col( $db, $fields, $fieldLimit );
	$sql = "SELECT $cols FROM {$db->escapeTable($table[0])} $dbWhere $dbSort $dbLimit";
	$res = $db->query( $sql );
	return new _DBS_DBSource_Result_Iterator( $db, $res, $item_construct, $table, $fields, $fieldLimit );
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
	 */
	public function loadAll( $key = null ) {
		if( !$this->start )	
			throw new Exception( "loadAll is only meant to be called on a full result" );
			
		$ret = array();
		foreach( $this as $item ) {
			if( $key === null )
				$ret[] = $item;
			else
				$ret[$item->$key] = $item;
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
		if( !$into->_set_load_keys() )
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
 * @param keys [in] "member" => array( dbname, dbtype, value )
 */
function dbs_dbsource_save( &$db, $table, DBS_EntityBase &$into, $keys, $fields, $lastInsert ) {
	$cols = array();
	$vals = array();
	$keycols = array();
	$keyvals = array();
	
	foreach( $fields as $member => $data ) {
		list( $dbname, $dbtype ) = $data;
		if( !$into->__isDirty( $member ) )
			continue;
			
		$cnv = "_cnv_F{$member}_T{$table[1]}_{$dbname}";
		$cols[] = $dbname;
		$vals[] = $db->quote( $into->$cnv( $into->__get( $member ) ), $dbtype );
	}
	
	foreach( $keys as $member => $data ) {
		list( $dbname, $dbtype, $value ) = $data;
		
		$cnv = "_cnv_F{$member}_T{$table[1]}_{$dbname}";
		$keycols[] = $dbname;
		$keyvals[] = $db->quote( $into->$cnv( $value ), $dbtype );
	}
	
	//if key based we must check for existence first
	if( count( $keycols ) ) {
		$keywhere = '';
		for( $i = 0; $i < count($keycols); $i++ ) {
			if( $i )
				$keywhere .= ' AND ';
			$keywhere .= $db->escapeColumn( $keycols[$i] );
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
	
	//TODO: shouldn't we check the "adding" status to ensure newRecord matches what we expect?
	
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
		throw new Exception( "Error while saving data." );
	$db->endResult( $res );
	
	//if we are using the lastInsert mechanism, then handle it here
	if( $newRecord && $lastInsert !== null ) {
		$id = $db->getNewID();
		
		$member = key( $lastInsert );
		list( $dbname, $dbtype ) = current( $lastInsert );
		
		if( $into->__has( $member ) )
			throw new Exception( "LastInsert field $member already set in data!" );
		
		$cnv = "_cnv_F{$table[1]}_{$dbname}_T{$member}";
		
		$value = $into->$cnv( $id );
		$into->__set( $member, $value );
		$into->__markClean( $member );
	}
}

?>