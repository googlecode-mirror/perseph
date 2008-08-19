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
//collection of basic scripts with no dependencies

/**
 * Gets the option value from an array, with an optional default
 *
 * @param   name    [in] name of the option
 * @param   opts    [in] array of options
 * @param   def     [in] default value if not specified
 * @return  [out] option value (whatever type it may be)
 */
function get_option( $name, $opts, $def = false ) {
    if( is_null( $opts ) )
        return $def;

    if( array_key_exists( $name, $opts ) )
        return $opts[$name];
    return $def;
}

/**
 * In some cases this name is clearer than "get_option"
 */
function array_get_default( $name, $arr, $def = false ) {
	return get_option( $name, $arr, $def );
}

function get_option_nodef( $name, $opts ) {
    if( array_key_exists( $name, $opts ) )
        return $opts[$name];
    die( "Missing options: $name" );
}

/**
 * Returns the ?first? element of an array, that is, the first
 * one which occurs in a foreach clause
 *
 * @return  [out] key
 */
function get_first_item_key( $array ) { 
    foreach( $array as $key => $value )
        return $key;
    return null;
}
 
/**
 * Creates an entry in the array if it does not already exist, setting it to the
 * default value
 */
function array_default( $key, &$array, $def ) {
    if( array_key_exists( $key, $array ) )
        return;
        
    $array[$key] = $def;
}

/**
 * Takes a value and map it to a canonical value
 */
//TODO: Move the sub-stuff from http.php to here...
function param_map_def( $value, $map, $def ) {
    if( is_null( $value ) )
        return $def;

    if( !array_ikey_exists( $value, $map ) )
        return $def;    //QUESTION: mabye null?!

    return array_iget( $value, $map );
}

/**
 * @deprecated use php microtime, now supports float return value
 */
function microtime_float() {
	return microtime( true );
}

/**
 * @deprecated use a db specific quote command
 */
function std_encodesqlstring( $str ) {
    return str_replace( "'", "''", $str );
}

function std_encodehtml( $str ) {
    return nl2br( htmlspecialchars( $str ) );
}

/**
 * @deprecated use xml
 */
function std_escapexml( $str ) {
    return htmlspecialchars( $str );
}

/**
 * @deprecated use xmlattr
 */
function std_encodehtmlattr( $str ) {
    return "'" . htmlspecialchars( $str, ENT_QUOTES ) . "'";
}

/**
 * For encoding data on output this is the preferred function to be used
 * for HTML and XML.  Use the "xmlattr" variety for encoding attributes.
 *
 * NOTE: use the {$xml(str)} for within strings
 */
function xml( $str ) {
	return htmlspecialchars( $str );
}

function xmlattr( $str ) {
    return "'" . htmlspecialchars( $str, ENT_QUOTES ) . "'";
}

$xml = 'xml';
$xmlattr ='xmlattr';

/**
 * Extra function for XML in case it needs to be different from HTML,
 * and to provide better readability
 */
function std_encodexmlattr( $str ) {
    return std_encodehtmlattr( $str );
}


/**
 * Converts a number into a unicode character string (in the internal encoding)
 *
 * Source: darkodemon at gmail dot com
 */
function uchr ($codes) {
    if (is_scalar($codes)) $codes= func_get_args();
    $str= '';
    foreach ($codes as $code) 
        $str .= html_entity_decode( '&#' . $code . ';', ENT_NOQUOTES, 'iso-8859-1' );
    return $str;
}

//input must be iso-8859-1 (I'm guessing the charset parameter is that of the input!?)
function ustr( $str ) {
    return html_entity_decode( $str, ENT_NOQUOTES, 'iso-8859-1' );
}

/**
 * Merges one array into another but first prefixes all the keys in the source array
 */
function array_merge_prefix( &$to, $src, $prefix ) {
	foreach( $src as $key => &$value )
		$to[$prefix . $key] =& $value;
}

/**
 * Since PHP array_merge destroys numeric indexes...
 */
function array_merge_numeric( $a, $b ) {
	$out = array();
	foreach( $a as $id => $value )
		$out[$id] = $value;
	foreach( $b as $id => $value )
		$out[$id] = $value;
	return $out;
}

/**
 * like explode, but puts delimiters around the items.
 */
function array_implode_enclose( $array, $start, $end, $space = '' ) {
	$ret = '';
	$first = true;
	foreach( $array as $item ) {
		if( !$first )
			$ret .= $space;
		else
			$first = false;
			
		$ret .= $start . $item . $end;
	}
	
	return $ret;
}

function array_implode_key_value( $array, $keyvaluesplit = ':', $rowsplit = "\n" ) {
	$ret = '';
	$first = true;
	foreach( $array as $key => $value ) {
		if( !$first )
			$ret .= $rowsplit;
		else
			$first = false;
			
		$ret .= $key . $keyvaluesplit . $value;
	}
	
	return $ret;
}

/**
 * Extends gettype to return additionally the class name if an object.
 */
function gettype_full( $obj ) {
	$cl = get_class( $obj );
	if( $cl !== false )
		return $cl;
	return gettype( $obj );
}

/**
 * Checks if the array contains a given value.
 */
function array_contains( $value, $arr ) {
	return array_search( $value, $arr ) !== false;
}


/**
 * Extract the object members of objects in an array.
 *
 * @param mem [in] the member of the object to pass to the function instead
 *		of the object itself
 * @param array [in] which array
 */
function array_members( $mem, $arr ) {
	$ret = array();
	foreach( $arr as $item )
		$ret[] = $item->$mem;
	return $ret;
}
?>