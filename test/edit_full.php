<?php
	require_once 'persephone/html_quickform.inc';
	require_once 'common_test.inc';
	
	std_header();
	
class EditForm extends DBS_FormBase_QuickForm {
	public $ENTITY = 'DBSTest';
	
	protected function _setup() {
		parent::_setup();
		$this->addStaticElement( 'id' );
		foreach( array( 'name', 'date', 'time', 'dateTime', 'bool', 'decimal', 'float', 'memoryOnly', 'otherDecimal', 'nullStr' ) as $element )
			$this->addTypicalElement( $element );
		$this->addSelectElement( 'nameRef', 	DBSName::search( DBS_Query::matchAll() ) );
	}
}
	
	dbs_standard_form( new EditForm(), 'ID' )->execute();
		
	print( "<p><a href='listing.php'>Return to listing</a></p>" );
?>