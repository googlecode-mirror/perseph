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

/**
 * Defines operators and means for searching the Entities
 */
class DBS_Query {

	const SORT_ASC = 'ASC';
	const SORT_DESC = 'DESC';
	
	static public function match( $member, $value, $op = '=' ) {
		$ret = new DBS_Where_Match();
		$ret->member = $member;
		$ret->value = $value;
		$ret->op = $op;
		return $ret;
	}
	
	/**
	 * Matches a field against any item in a list of values.
	 * 
	 * @param member [in] which member to match
	 * @param values [in] it must reside in this list of values.  This is an iterable object
	 */
	static public function matchIn( $member, $values ) {
		if( !_pers_is_iterable( $values ) )
			throw new Exception( "'values' to matchIn must be an iterable object" );
			
		$ret = new DBS_Where_MatchIn();
		$ret->member = $member;
		$ret->values = $values;
		return $ret;
	}
	
	/**
	 * Matches a string type column against a pattern string.
	 *
	 * @param member
	 * @param pattern [in] the pattern to match, use * to match any number of characters
	 *			TODO: complete patterns/escaping; reserved characters: ? \
	 * @param positive [in] true to select those matching the pattern, false for those not matching
	 */
	static public function matchStringPattern( $member, $pattern, $positive = true ) {
		$ret = new DBS_Where_MatchString();
		$ret->member = $member;
		$ret->pattern = $pattern;
		$ret->positive = $positive;
		return $ret;
	}
	
	/**
	 * Allows matching of all records. Most functions require a matching query
	 * to always be present (no default of all)
	 */
	static public function matchAll() {
		return new DBS_Where_MatchAll();
	}
	
	/**
	 * Creates a boolean OR group of the provided match qualifiers. Accepts
	 * either an array of qualifiers, or variable argument syntax.
	 * Only qualifiers resulting from "match*" functions can be used.
	 */
	static public function matchOrGroup( ) {
		$args = func_get_args();
		return self::_group( "OR", $args );
	}
	
	/**
	 * As with matchOrGroup but uses the boolean AND operator.
	 */
	static public function matchAndGroup( ) {
		$args = func_get_args();
		return self::_group( "AND", $args );
	}
	
	/**
	 * Allows custom SQL to be added to the final query. This can be used
	 * in conjuction with groups as well.
	 *
	 * Note that no escaping of the provided SQL will be done, you will be
	 * responsible for that.
	 */
	static public function matchSQL( $sql ) {
		return new DBS_Where_MatchSQL( $sql );
	}
	
	static private function _group( $type, $args ) {
		//support passing array as well as multi-params
		if( count( $args ) === 1 && is_array( $args[0] ) )
			$args = $args[0];
			
		$ret = new DBS_Where_Group( $type );
		//note we allow one item since it makes using the functions easier in a dynamic fashion
		if( count( $args ) < 1 )
			throw new Exception( "An $type Group must have at least one item" );
			
		foreach( $args as $arg ) {
			if( (!$arg instanceof DBS_Where_Item) )
				throw new Exception( "Item needs to be instance of DBS_Where_Item, has type " . gettype_full( $arg ) );
			$ret->members[] = $arg;
		}
		return $ret;
	}
	
	/**
	 * Indicates that the results should be limited. That is, at most this
	 * number of rows will be returned.  Which rows are returned is
	 * generally only specified if a "sort" qualifier is used.
	 */
	static public function limit( $limit ) {
		return  new DBS_Limit( $limit );
	}
	
	static public function offset( $offset ) {
		return new DBS_Offset( $offset );
	}
		
	/**
	 * Sorts the results. If no such qualifier is used the results are in
	 * an undefined order.
	 *
	 * @param member [in] either a single member, or an array of 
	 *		members in precedence order to sort on
	 */
	static public function sort( $member, $mode ) {
		if( !is_array( $member ) )
			$member = array( $member );
			
		$ret = new DBS_Sort_Single();
		$ret->members = $member;
		$ret->mode = $mode;
		return $ret;
	}
	
	/**
	 * This is a special optimizing qualifier which indicates which fields
	 * should be loaded as part of a search operation. Should it not be
	 * specified then all entity fields are normally loaded.  When specified
	 * only the indicated fields will be loaded as part of the search.
	 *
	 * This is commonly used for Listings where not all fields are needed
	 * and loaded them may result in wasted resources.
	 *
	 * Variable arguments of an array is supported.
	 */
	static public function fieldLimit( ) {
		$args = func_get_args();
		if( count( $args ) === 1 && is_array( $args[0] ) )
			$args = $args[0];
			
		return new DBS_FieldLimiter( $args );
	}
	
	/**
	 * Obtains the offset set in this query, or default if not set
	 */
	static public function getOffset( $query, $def = 0 ) {
		$off = self::getItem( $query, 'DBS_Offset' );
		if( $off !== null )
			return $off->offset;
		return $def;
	}
	
	static public function getLimit( $query, $def = false ) {
		$limit = self::getItem( $query, 'DBS_Limit' );
		if( $limit !== null )
			return $limit->limit;
		return $def;
	}
	
	static private function getItem( $query, $class ) {
		foreach( $query as $q )
			if( $q instanceof $class )
				return $q;
		return null;
	}
}

///////////////////////////////////////////////////////////////////////////////
// NOTE: Items below this line are not meant to be used directly, instead only the above class should
// be used to create these objects.  They may change at any time and are not considered part of the
// public API.

class DBS_Where_Item {
}

class DBS_Where_Member extends DBS_Where_Item {
	public $member;	//<String>
}

class DBS_Where_MatchAll extends DBS_Where_Item {
}

class DBS_Where_MatchSQL extends DBS_Where_Item {
	public $sql;	//<String>
	
	public function __construct( $sql ) {
		$this->sql = $sql;
	}
}

class DBS_Where_Match extends DBS_Where_Member {
	public $value;	//<*>
	public $op;	//<String>
}

class DBS_Where_MatchString extends DBS_Where_Member {
	public $pattern;	//<String>
	public $positive;	//<Boolean>
}

class DBS_Where_MatchIn extends DBS_Where_Member {
	public $values;	//Array<*>
}

class DBS_Where_Group extends DBS_Where_Item {
	public $members = array();	//array<DBS_Where_Item>
	public $type;
	
	public function __construct( $type ) {
		$this->type = $type;
	}
}

/**
 * Limit and Offset are two distinct query items since they are actually
 * different, but also since they allow an easier page control mechanism:
 * a better way to alter a query with paged sets (such as listings).
 */
class DBS_Limit {
	public $limit;	//count of limit
	
	public function __construct( $limit ) {
		$this->limit = $limit;
	}
}

class DBS_Offset {
	public $offset; //offset
	
	public function __construct( $offset ) {
		$this->offset = $offset;
	}
}

class DBS_Sort_Item {
}

class DBS_Sort_Single extends DBS_Sort_Item {
	public $members;
	public $mode;
}

class DBS_FieldLimiter {
	public $fields;
	
	public function __construct( $fields ) {
		$this->fields = $fields;
	}
}

?>