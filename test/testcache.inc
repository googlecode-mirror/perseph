<?php

/**
 * Used by the tests to ensure that caching is working as expected.  That is, that the
 * generic caching logic works as expected -- the back-end caches should be tested
 * separately.
 */
class TestCache implements EntityCache {

	public $field;
	//so we have access to the caches
	static $caches = array();
	
	public function __construct( $field ) {
		$this->field = $field;
		self::$caches[$field] = $this;
	}
	
	public $lastIs;
	public $inCache = array();
	
	public function isCached( $key ) {
		$this->lastIs = $key;
		if( isset( $this->inCache[$key] ) )
			return true;
			
		return false;
	}
	
	public function getCached( $key ) {
		return $this->inCache[$key];
	}
	
	public $lastAddKey;
	public $lastAddObject;
	
	public function add( $key, &$object ) {
		$this->lastAddKey = $key;
		$this->lastAddObject = $object;
	}
}

?>