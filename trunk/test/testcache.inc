<?php

/**
 * Used by the tests to ensure that caching is working as expected.  That is, that the
 * generic caching logic works as expected -- the back-end caches should be tested
 * separately.
 */
class TestCache implements EntityCache {

	private $field;
	
	public function __construct( $field ) {
		$this->field = $field;
	}
	
	public function isCached( $key ) {
		return false;
	}
	
	public function getCached( $key ) {
		//
	}
	
	public function add( $key, &$object ) {
	}
}

?>