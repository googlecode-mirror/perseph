<?php
	require_once 'gen/SampleFormFull.form.inc';
	require_once 'common_test.inc';
	
	std_header();
	
	dbs_standard_form(
		'FormSampleFormFull',
		'ID',
		array( ) 
		)->execute();
		
	print( "<p><a href='listing.php'>Return to listing</a></p>" );
?>