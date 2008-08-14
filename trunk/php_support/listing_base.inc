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

class DBS_ListingBase {

	protected $searchArgs;	//the search criteria for data to display
	
	protected $fields; //array of field data array( name, Label, formatting function )
		
	protected $entity;	//entity data to search/display
	
	protected function __construct( $searchArgs ) {
		$this->searchArgs = $searchArgs;
	}
	
	public function execute() {
		print( "<table class='overview'>\n" );
		
		$this->printHeaderRow();
		
		$data = call_user_func( "{$this->entity}::search", $this->searchArgs );
		$this->printContent( $data );
		$data->endSearch();
		
		print( "</table>" );
	}
	
	private function printHeaderRow() {
		global $xml;
		
		print( "<tr class='header'>" );
		foreach( $this->fields as $spec )
			print( "<th>{$xml($spec[1])}</th>" );
		print( "</tr>\n" );
	}
	
	private function printContent( $data ) {
		global $xml;
		
		$rownum = 0;
		foreach( $data as $d ) {
			$crow = $rownum % 6;
			$rc = "count_$crow";
			
			print( "<tr class='$rc'>" );
			foreach( $this->fields as $spec ) {
				if( $spec[0] === '@SELF' )
					$formatted = $spec[2]( $d );
				else
					$formatted = $spec[2]( $d->$spec[0] );
					
				print( "<td>$formatted</td>" );
			}
			print( "</tr>" );
	
			$rownum++;
		}
	}
}

///////////////////////////////////////////////////////////////////////////////
// Standard Formatters
function format_listing_Integer( $value ) {
	if( is_null( $value ) )
		return 'n/a';
	return $value;
}

function format_listing_Decimal( $value ) {
	if( is_null( $value ) )
		return 'n/a';
	return $value;
}

function format_listing_DateTime( $value ) {
	if( is_null( $value ) )
		return 'n/a';
		
	return date( 'Y-m-d H:i:s', $value );
}

function format_listing_Date( $value ) {
	if( is_null( $value ) )
		return 'n/a';
		
	return date( 'Y-m-d', $value );
}

function format_listing_Boolean( $value ) {
	if( is_null( $value ) )
		return 'n/a';

	return $value ? 'true' : 'false';
}

function format_listing_String( $value ) {
	return xml( $value );
}

function format_listing_Text( $value ) {
	return xml( $value );
}
?>