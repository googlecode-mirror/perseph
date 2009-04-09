<?php
	require_once 'persephone/listing_base.inc';
	require_once 'web_common.inc';
	require_once dirname(__FILE__).'/gen/DBSTest.inc';
	
class Listing extends DBS_HTMLTable_Listing {
	public $ENTITY = 'DBSTest';
	
	public function __construct() {
		parent::__construct();
		
		$this->addColumns( array(
			/* Custom formatters can be specified for any column */
			'id' => array( 'label' => 'Some ID', 'format' => '_fmt_id' ),
			'name' => array(),	/*User default label*/
			'decimal' => array( 'label' => 'Decimal Value' ),
			/*NameRef "Links To"; TODO: support without need for converter */
				
			/* Here the entity itself is provided to the formatter */
			'@SELF' => array( 'format' => '_fmt_ruleaction', 'label' => "Action" ),
			));
	}
}

	std_header();
	
	print( "<h2>DBS List (<a href='edit.php'>Add</a>)</h2>" );
	
	$listing = new Listing();
	print( $listing->render( DBSTest::search( DBS_Query::matchAll() ) ) );
	
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