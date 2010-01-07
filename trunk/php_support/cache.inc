<?php

interface EntityCache {
	/**
	 * @return [out] true if the item with this key is in the cache, false otherwise
	 */
	public function isCached( $key );
	
	/**
	 * @return [out] the value cached with this key, undefined if key is not in the cache
	 */
	public function getCached( $key );
	
	/**
	 * This adds an item to the cache or updates an existing item.
	 *
	 * @param key [in] how to reference the entity in the cache
	 * @param object [in] the object/value to store in the cache
	 */
	public function add( $key, &$object );
}

?>