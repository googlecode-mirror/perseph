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
		
	$lfile = strtolower( $file );	//compare as lower-case to help with windows installs (which often use upper-case)
	//try to skip items in the pear folders, which aren't PHP 5 strict compliant
	if ( $no == E_STRICT && (
		strpos($lfile, '/pear/') ||
		strpos($lfile,'/php/') ||
		strpos($lfile, '\\pear\\') ||
		strpos($lfile,'\\php\\') 
		) ) {
		/* Don't execute PHP internal error handler */
		return true;
	}
	return false;
}
set_error_handler('strict_clean_error_handler');

assert_options( ASSERT_ACTIVE, 1 );
assert_options( ASSERT_WARNING, 1 );
assert_options( ASSERT_BAIL, 0 ); //throw exception below instead
assert_options( ASSERT_QUIET_EVAL, 0 );

//track the stack with assertions.
function exception_assert_handler($file, $line, $code)
{	
	throw new Exception( "Assert Fail: $file: $line: $code" );
}
assert_options(ASSERT_CALLBACK, 'exception_assert_handler');

?>