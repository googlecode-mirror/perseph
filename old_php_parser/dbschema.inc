<?php
/* ***** BEGIN LICENSE BLOCK *****
 * Version: GPL 3.0
 * This file is part of Persephone.
 *
 * Persephone is free software: you can redistribute it and/or modify it under the 
 * terms of the GNU General Public License as published by the Free Software
 * Foundation, version 3 of the License.
 *
 * Persephone is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with Persephone.  If not, see <http://www.gnu.org/licenses/>.
 *
 * Copyright (C) 2008 eCircle AG
 * 
 * Contributors:
 *		edA-qa mort-ora-y <edA-qa@disemia.com>
 * ***** END LICENSE BLOCK ***** */

/**
 * Encapsulates the complete information about a data Schema.
 */
class DBSchema {

	//public only for DBSchema_Parser
	public $defaults = array();	//<String,String>
	public $types = array();	//<String,DBSchema_Type>
	public $providers = array();		//<String,DBSchema_Provider>
	public $entities = array();	//<String,DBSchema_Entity>
	public $mappers = array(); //<String,DBSchema_Mapper>
	public $forms = array();	//<String,DBSchema_Form>
	public $listings = array(); //<String,DBSchema_Listing>
	
	public function __construct() {
		$this->types['String'] = new DBSchema_Type( 'String' );
		$this->types['Integer'] = new DBSchema_Type( 'Integer' );
		$this->types['DateTime'] = new DBSchema_Type( 'DateTime' );
		$this->types['Date'] = new DBSchema_Type( 'Date' );
		$this->types['Time'] = new DBSchema_Type( 'Time' );
		$this->types['Decimal'] = new DBSchema_Type( 'Decimal' );
		$this->types['Float'] = new DBSchema_Type( 'Float' );
		$this->types['Bool'] = new DBSchema_Type( 'Bool' );
		$this->types['Text'] = new DBSchema_Type( 'Text' );
	}
	
	/**
	 * Parses a standard formatted schema file
	 */
	static public function parse( $text ) {
		return _dbschema_parse( $text );
	}
}

class DBSchema_Type {
	public $name;	//<String>
	
	public function __construct( $name ) {
		$this->name = $name;
	}
	
	public function &getRootType() {
		return $this;
	}
	
	public function baseType() {
		return true;
	}
}

class DBSchema_CollectionType extends DBSchema_Type {
	public $of;	//<DBSchema_Type> what it contains
	
	public function __construct( $name, DBSchema_Type &$of ) {
		parent::__construct( $name );
		$this->of =& $of;
	}
}

class DBSchema_CustomType extends DBSchema_Type {
	public $base;		//<DBSchema_Type>
	
	public function __construct( $name, DBSchema_Type &$base ) {
		parent::__construct( $name );
		$this->base =& $base;
	}
	
	public function &getRootType() {
		return $this->base;
	}
	
	public function baseType() {
		return false;
	}
}

abstract class DBSchema_Provider {

}

class DBSchema_Provider_DBSource extends DBSchema_Provider {
	public $varname;	//variable name in PHP which is this source
	
	public function __construct( $varname ) {
		$this->varname = $varname;
	}
}

class DBSchema_Entity extends DBSchema_Type {
	public $fields = array(); //<String,$DBSchema_Entity_Field>
	public $aliases = array();	//Alias => Internal, simple support for now
	
	public $class;	//<String> if not null specifies the instance classname to use instead of "name"
	
	public function __construct( $name ) {
		parent::__construct( $name );
	}
	
	/**
	 * Obtains the sets of keys which can identify this record for loading/saving
	 */
	public function getRecordKeyFields() {
		$ret = array();
		foreach( $this->fields as $field )
			if( $field->keyType !== DBSchema_Entity_Field::KEY_TYPE_NONE )
				$ret[] = $field;
				
		return $ret;
	}
	
	/**
	 * Obtains a set of all keys/composites which can identify the identity.
	 */
	public function getKeySet() {
		$ret = array();
		$comp = array();
		foreach( $this->fields as $field ) {
			if( $field->keyType == DBSchema_Entity_Field::KEY_TYPE_RECORD )
				$comp[] = $field;
			if( $field->keyType == DBSchema_Entity_Field::KEY_TYPE_ALT )
				$ret[] = array( $field );
		}
		
		if( count( $comp ) )
			$ret[] = $comp;
			
		return $ret;
	}
	
	public function getTitle() {
		foreach( $this->fields as $field ) {
			if( $field->title )
				return $field;
		}
		return null;
	}
}

class DBSchema_Entity_Field {
	const KEY_TYPE_NONE = 0;
	const KEY_TYPE_RECORD = 1;
	const KEY_TYPE_ALT = 2;
	
	public $name; //<String>
	public $type;	//<DBSchema_Type>
	public $keyType = self::KEY_TYPE_NONE;
	public $hasDefault = false;	//<Boolean>
	public $defaultValue;
	public $loadOnly = false;	//<Boolean>
	public $title = false; //<String> the logical title of the entity
	public $maxLen = null;	//Null<Integer>, if non-null indicates the maximum logical length to the entity
	public $allowNull = false;	//does the field allow a null assignment
	
	public function __construct( $name, DBSchema_Type &$type ) {
		$this->name = $name;
		$this->type =& $type;
	}
}

class DBSchema_Mapper_Field {
	public $db_convert_func;
	public $db_convert_type; //<DBSchema_Type>
	public $db_col; 
	public $db_type; //<String>
	
	public $ent_field; //<DBSchema_Entity_Field>
	public $ent_field_field;	//<DBSchema_Entity_Field> name of field in the entity field, may be null (no sub-field in use)
}

class DBSchema_Mapper {
	public $provider;	//<DBSchema_Provider>
	public $entity;	//<DBSchema_Entity>
	
	//some of this is likely provider specific, I can look at this once a second provider is needed
	public $table;	
	public $fields;	//array<DBSchema_Mapper_Field>
	public $insertField;	//array<DBSchema_Mapper_Field>
	
	public function __construct( DBSchema_Provider &$provider ) {
		$this->provider =& $provider;
	}
	
	public function getDBFieldForEntityField( DBSchema_Entity_Field &$ef ) {
		foreach( $this->fields as $locfield )
			if( $locfield->ent_field->name == $ef->name )
				return $locfield;
		throw new Exception( "No DBField for the entity {$ef->name}" );
	}
}

class DBSchema_Form {
	public $name	;	//<String>
	public $entity;	//<DBSchema_Entity>
	public $allowDelete;	//<Bool>
	public $fields = array(); //Array<String,DBSchema_Form_Field>
}

class DBSchema_Form_Field {
	public $name;
	public $hidden = false;
	public $readonly = false;
	
	public function __construct( $name ) {
		$this->name = $name;
	}
}

class DBSchema_Listing {
	public $name;	//<String>
	public $entity;	//<DBSchema_Entity>
	public $fields = array();	//Array<DBSchema_Listing_Field>
}

class DBSchema_Listing_Field {
	public $entField; //<DBSchema_Entity_Field> or null for the entity itself
	public $label;	//<String> 
	public $convertFunc;	//<FunctionName>
}

?>