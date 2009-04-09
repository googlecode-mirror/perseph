<?php

/* The customer classes for the entites */

class DerivedStrings extends DBSStrings {

	//TODO: Show how to provide custom static constructors
	
	/**
	 * A very simple example of how to provide custom functionality.
	 */
	public function contains( $str ) {
		return (bool)array_search( $str, $this->labels );
	}
}

?>