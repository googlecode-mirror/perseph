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

/* This comes from ems-php-utils and it would be preferred to use that file
 * there, but we don't want to be dependent on that distribution.  Once PHP 5.3
 * is common then we can use namespaces to properly copy/import the
 * desired functions.
 */

/**
 * Gets the option value from an array, with an optional default
 *
 * @param   name    [in] name of the option
 * @param   opts    [in] array of options
 * @param   def     [in] default value if not specified
 * @return  [out] option value (whatever type it may be)
 */
function _pers_array_get_default( $name, $opts, $def = false ) {
    if( is_null( $opts ) )
        return $def;

    if( array_key_exists( $name, $opts ) )
        return $opts[$name];
    return $def;
}

?>