<?php

require_once dirname(__FILE__).'/cache.inc';

/**
 * Implements a FIFO cache for entities.  This cache has a maximum size and
 * the most recently added items are preferred to older items.
 */
final class FIFOCache implements EntityCache {
	
	private $size;
	private $at;
	private $cache = array();
	private $order = array();
	
	public function __construct( $size ) {
		$this->size = $size;
		$this->at = 0;
	}
	
	public function isCached( $key ) {
		return array_key_exists( $key, $this->cache );
	}
	
	public function getCached( $key ) {
		return $this->cache[$key];
	}
	
	public function add( $key, &$object ) {
		if( $this->at < count($this->order ) )
			unset( $this->cache[$this->order[$this->at]] );
		$this->cache[$key] =& $object;
		$this->order[$this->at] = $key;
		$this->at++;
		if( $this->at >= $this->size )
			$this->at = 0;
	}
}

?>