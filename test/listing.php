<?php
	require_once 'gen/SampleList.listing.inc';
	require_once 'common_test.inc';
	
	std_header();
	
	print( "<h2>DBS List (<a href='edit.php'>Add</a>)</h2>" );
	
	$table = ListingSampleList::search( DBS_Query::matchAll() );
	$table->execute();
	
/* formatting functions specific to one listing can be kept local to this file, they need not be
	seen everywhere, just as the listing itself need only be included in this file */
	
function _fmt_ruleaction( DBSTest $self ) {
	return "<a href='edit.php?ID={$self->id}'>Edit</a>"
		. " <a href='edit_full.php?ID={$self->id}'>Full</a>";
}

function _fmt_id( $id ) {
	return "<span style='border: thin solid'>$id</span>";
}
?>