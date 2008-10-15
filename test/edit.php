<?php
	require_once 'persephone/html_quickform.inc';
	require_once 'common_test.inc';
	
	std_header();
	
class EditForm extends DBS_FormBase_QuickForm {
	public $ENTITY = 'DBSTest';
	
	protected function _setup() {
		parent::_setup();
		$this->addStaticElement( 'id' );
		$this->addTypicalElement( 'name' );
		$this->addTypicalElement( 'date' );
		$this->addStaticElement( 'float' );
	}
}

	dbs_standard_form( new EditForm(), 'ID' )->execute();
	
	print( "<p><a href='listing.php'>Return to listing</a></p>" );
?>