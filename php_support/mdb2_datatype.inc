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
 * On some databases, or transports, (like MySQL 4) you cannot set a character
 * set for the client.  This means the strings you get back will not be decoded, and
 * those you send will not be encoded when using MDB2.  It is upsetting that the
 * MDB2 team did not address this issue, but alas...
 *
 * These callback functions are meant to assist in this.  The typical use is in
 * a factory() call as part of the options:
 *		array(
 *			//setup as utf8 for text columns
 *			'datatype_map' => array( 'cstring' => 'cstring' ),
 *			'datatype_map_callback' => array( 'cstring' => 'mdb2_cstring_utf8_callback' ),
 *			) 
 * Then use 'cstring' instead of 'text' to get the conversion.  Also use 'cstring' as
 * the second parameter to the MDB2DBSource constructor:
 *		$db_test = new MDB2DBSource( $mdb, 'cstring' );
 */

function mdb2_cstring_callback( $charset, &$db, $method, $aParameters )
{
	//we only need a subset of methods if we aren't dealing with schemas
	switch( strtolower( $method) ) {
		case 'convertresult':
			$halfraw = $db->datatype->convertResult( $aParameters['value'], 'text', $aParameters['rtrim']);
			return mb_convert_encoding( $halfraw, mb_internal_encoding(), $charset );
		case 'quote':
			$halfraw = mb_convert_encoding( $aParameters['value'],  $charset, mb_internal_encoding() );
			return $db->datatype->quote($halfraw, 'text');
		default:
			throw new Exception( "unexpected method $method" );
    }
}

function mdb2_cstring_utf8_callback(&$db, $method, $aParameters) {
	return mdb2_cstring_callback( 'utf-8', $db, $method, $aParameters );
}

function mdb2_cstring_iso88591_callback(&$db, $method, $aParameters) {
	return mdb2_cstring_callback( 'iso-8859-1', $db, $method, $aParameters );
}

function mdb2_cstring_latin1_callback(&$db, $method, $aParameters) {
	return mdb2_cstring_callback( 'iso-8859-1', $db, $method, $aParameters );
}

function mdb2_cstring_iso885915_callback(&$db, $method, $aParameters) {
	return mdb2_cstring_callback( 'iso-8859-15', $db, $method, $aParameters );
}

?>