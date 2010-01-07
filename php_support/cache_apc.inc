<?php

require_once dirname(__FILE__).'/cache.inc';

/**
 * This cache stores objects via APC. It is currently not suitable for objects that will be
 * changed during the life of the request -- as it may return independent versions of 
 * those objects.
 */
class APCCache implements EntityCache {
	
	private $ttl;
	private $prefix;
	
	/**
	 * @param $prefix [in] the prefix for items stored in APC
	 * @param $ttl [in] the lifetime (in seconds) for the APC stored objects
	 */
	public function __construct( $prefix, $ttl ) {
		$this->ttl = $ttl;
		$this->prefix = $prefix;
	}
	
	private $lastKey;
	private $lastObject;
	public function isCached( $key ) {
		$cName = $this->prefix . $key;
		$this->lastKey = $key;
		$this->lastObject = apc_fetch( $cName, $has ); //PHP: there is no function to just check if it is there or not :(
		return $has;
	}
	
	public function getCached( $key ) {
		//shortcut to prevent the double apc_fetch in most common use cases
		if( $this->lastKey === $key )
			return $this->lastObject;
			
		$cName = $this->prefix . $key;
		$object = apc_fetch( $cName, $has );
		if( !$has )
			throw new Exception( "Object not in cache: $key" );
		return $object;
	}
	
	public function add( $key, &$object ) {
		$cName = $this->prefix . $key;
		if( !apc_store( $cName, $object, $this->ttl ) )
			apc_delete( $cName ); //if we can't store ensure whatever was there is deleted
	}
}

?>