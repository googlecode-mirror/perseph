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

function strict_clean_error_handler( $no, $msg, $file, $line ) {
	//allow error suppression to always work
	if( error_reporting() === 0 )
		return true;
		
	//try to skip items in the pear folders, which aren't PHP 5 strict compliant
	if ( $no == E_STRICT && (
		strpos($file, '/pear/') ||
		strpos($file,'/php/') ||
		strpos($file, '\\pear\\') ||
		strpos($file,'\\php\\') 
		) ) {
		/* Don't execute PHP internal error handler */
		return true;
	}
	return false;
}
set_error_handler('strict_clean_error_handler');

assert_options( ASSERT_ACTIVE, 1);
assert_options( ASSERT_WARNING, 1);
assert_options( ASSERT_BAIL, 1);

?>