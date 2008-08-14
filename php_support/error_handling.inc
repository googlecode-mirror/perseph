<?php

function strict_clean_error_handler( $no, $msg, $file, $line ) {
    if ( $no == E_STRICT && (
    		strpos($file, '/pear/') ||
    		strpos($file,'/php/') ||
    		preg_match('/(PEAR|MDB2_Date)::.*?should not be called statically/', $msg)
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