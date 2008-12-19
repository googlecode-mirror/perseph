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

abstract class DBS_Listing {
	public $ENTITY = null;	//the class of the entity involved (Override in derived class )
	
	protected $typeDesc = null;
	protected $cols = array();
	
	protected function __construct( ) {
		$this->typeDesc = call_user_func( "{$this->ENTITY}::getTypeDescriptor" );
	}
	
	public $numRows = 0;	//the number of rows which were rendered from the resultSet
	
	/**
	 * Options:
	 *			format => an explicit formatting function (name) (Default: that of formatType)
	 *			formatType => override or specify the type of the column (Default: as in ENTITY)
	 *			label => label for the listing field (Default: as in ENTITY)
	 *			sub => use the sub-field instead of the main entry (NOTE: formatType or format required!)
	 *				FEATURE: we could detect Entity subtypes and field type
	 */
	public function addColumn( $field, $opts = array() ) {
		if( !isset( $opts['format'] ) ) { 
			if( !isset( $opts['formatType'] ) ) {
				$asType = $this->typeDesc->getCustomType( $field );
				if( $asType == null )
					$asType = $this->typeDesc->getBaseType( $field );
				$opts['formatType'] = $asType;			
			}
			$opts['format'] = null;
		} else if( !isset( $opts['formatType'] ) ) 
			$opts['formatType'] = 'Undefined';	//so that it always exists
		
		if( !isset( $opts['label'] ) )
			$opts['label'] = $this->typeDesc->getDefaultLabel( $field );
			
		$this->cols[] = array( $field, $opts );
	}
	
	/**
	 * Convenience function to add multiple columns at once.
	 *
	 * @param cols [in] an array of name=> opts entries, as would
	 *		be passed to addColumn.  Optionally just a name can be
	 * 	specified as a value (with automatic numeric index) and the
	 *		default options will be used)
	 */
	public function addColumns( $cols ) {
		foreach( $cols as $field => $opts ) {
			if( is_int( $field ) && is_string( $opts ) )
				$this->addColumn( $opts );
			else
				$this->addColumn( $field, $opts );
		}
	}
	
	/**
	 * Render the rows of the search.
	 *
	 * @param search [in] Search<ENTITY>
	 */
	public function render( $search ) {
		$buf = $this->renderOpen();
		$buf .= $this->renderHeader();
		foreach( $search as $row ) {
			if( !$this->filterRow( $row ) )
				continue;
				
			$buf .= $this->renderRow( $row );
		}
		$buf .= $this->renderClose();
		return $buf;
	}
	
	public function renderSearch( ) {
		$args = func_get_args();
		if( count( $args ) === 1 && is_array( $args[0] ) )
			$args = $args[0];			
		
		$search = call_user_func( "{$this->ENTITY}::search", $args );
		return $this->render( $search );
	}
	
	protected function renderHeader() {
		$buf = $this->renderOpenRow( true );
		foreach( $this->cols as $col )
			$buf .= $this->renderHeaderCell( $col[1]['label'], false /*TODO*/ );
		$buf .= $this->renderCloseRow();
		return $buf;
	}
	
	protected function renderRow( $row ) {
		$this->numRows++;
		$buf = $this->renderOpenRow( false );
		foreach( $this->cols as $col ) {
			$field = $col[0];
			if( $field === '@SELF' )
				$raw = $row;
			else {
				$raw = $row->$field;
				$sub = array_get_default( 'sub', $col[1], null );
				if( $sub !== null )
					$raw = $raw->$sub;
			}
			
			$buf .= $this->renderCell( $raw, $col[1]['formatType'], $col[1]['format'], false /*TODO*/ );
		}
		$buf .= $this->renderCloseRow();
		return $buf;
	}
	
	/**
	 * Allows a hook to provide post-search filtering on the result-set.
	 *
	 * FEATURE: perhaps a Search wrapper would make more sense here?
	 * @return [out] true to include row, false to exclude
	 */
	protected function filterRow( /*ENTITY*/ $row ) {
		return true;
	}
	
	abstract function renderOpen();
	abstract function renderClose();
	abstract function renderOpenRow( $header );
	abstract function renderCloseRow();
	abstract function renderCell( $raw, $type, $renderFunc, $final );
	abstract function renderHeaderCell( $title, $final );
}

class DBS_CSV_Listing extends DBS_Listing {
	public $separator = ',';
	
	function renderOpen() { 
		return "";
	}
	
	function renderClose() {
		return "";
	}
	
	function renderOpenRow( $header ) {
		return "";
	}
	
	function renderCloseRow() {
		return "\n";
	}
	
	function renderCell( $raw, $type, $renderFunc, $final ) {
		if( $renderFunc == null )
			$renderFunc = "format_csv_$type";
		if( !function_exists( $renderFunc ) )
			throw new Exception ( "Formatting function $renderFunc does not exist" );
		
		$buf = $renderFunc( $raw );
		
		if( !$final )
			$buf .= ',';
			
		return $buf;
	}
	
	function renderHeaderCell( $title, $final ) {
		$buf = format_csv_raw( $title );
		if( !$final )
			$buf .= ',';
		return $buf;
	}
}

class DBS_HTMLTable_Listing extends DBS_Listing {
	public $separator = ',';
	protected $rowCount = 0;
		
	protected $pageSize = null;
	
	function renderOpen() { 
		return "<table class='overview'>";
	}
	
	function renderClose() {
		return "</table>";
	}
	
	function renderOpenRow( $header ) {
		if( $header ) {
			return "<tr class='header'>";
		} else {
			$crow = $this->rowCount % 6;
			$rc = "count_$crow";
			$this->rowCount++;
			return "<tr class='$rc'>";
		}
	}
	
	function renderCloseRow() {
		return "</tr>";
	}
	
	function renderCell( $raw, $type, $renderFunc, $final ) {
		if( $renderFunc == null )
			$renderFunc = "format_html_$type";
		if( !function_exists( $renderFunc ) )
			throw new Exception ( "Formatting function $renderFunc does not exist" );
		
		$buf = $renderFunc( $raw );
			
		return "<td>$buf</td>";
	}
	
	function renderHeaderCell( $title, $final ) {
		$buf = format_html_raw( $title );
		return "<th>$buf</th>";
	}
}

///////////////////////////////////////////////////////////////////////////////
// Standard HTML Formatters

function format_html_raw( $value ) {
	return htmlspecialchars( $value, ENT_QUOTES );
}

function format_html_Integer( $value ) {
	if( is_null( $value ) )
		return 'n/a';
	return $value;
}

function format_html_Decimal( $value ) {
	if( is_null( $value ) )
		return 'n/a';
	return $value;
}

function format_html_DateTime( $value ) {
	if( is_null( $value ) )
		return 'n/a';
		
	return date( 'Y-m-d H:i:s', $value );
}

function format_html_Date( $value ) {
	if( is_null( $value ) )
		return 'n/a';
		
	return date( 'Y-m-d', $value );
}

function format_html_Time( $value ) {
	if( is_null( $value ) )
		return 'n/a';
		
	//borrow the DBS function (use SQL format)
	return _dbs_encode_time( $value );
}

function format_html_Boolean( $value ) {
	if( is_null( $value ) )
		return 'n/a';

	return $value ? 'true' : 'false';
}

function format_html_String( $value ) {
	return format_html_raw( $value );
}

function format_listing_Text( $value ) {
	return format_html_raw( $value );
}

///////////////////////////////////////////////////////////////////////////////
// Standard CSV Formatters

function format_csv_raw( $value ) {
	if( $value === null )
		return '';
	//convert to string
	$value = "$value";
	
	//check for a clean string, be quite restrictive to be safe
	if( preg_match( '/^[a-zA-Z0-9\.\-\_]*$/', $value ) !== 0)
		return $value;
		
	//escape whole string and quotes
	return '"' 
		. preg_replace( '/"/', '""', $value )
		. '"';
}

function format_csv_Integer( $value ) {
	if( is_null( $value ) )
		return 'n/a';
	return $value;
}

function format_csv_Decimal( $value ) {
	if( is_null( $value ) )
		return 'n/a';
	return $value;
}

function format_csv_Time( $value ) {
	if( is_null( $value ) )
		return 'n/a';
		
	//borrow the DBS function (use SQL format)
	return _dbs_encode_time( $value );
}

function format_csv_DateTime( $value ) {
	if( is_null( $value ) )
		return 'n/a';
		
	return date( 'Y-m-d H:i:s', $value );
}

function format_csv_Date( $value ) {
	if( is_null( $value ) )
		return 'n/a';
		
	return date( 'Y-m-d', $value );
}

function format_csv_Boolean( $value ) {
	if( is_null( $value ) )
		return 'n/a';

	return $value ? 'true' : 'false';
}

function format_csv_String( $value ) {
	return format_csv_raw( $value );
}

function format_csv_Text( $value ) {
	return format_csv_raw( $value );
}

?>