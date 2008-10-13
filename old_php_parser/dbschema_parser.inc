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

require_once dirname(__FILE__) . '/dbschema.inc';
require_once dirname(__FILE__) . '/php_support/base.inc';

/**
 * This parser is rather unforgiving at the moment, not to mention inefficient.
 *
 * They are meant for one-time use, no multiple calls to parseInto.
 */
class DBSchema_Parser {
	var $input;
	var $offset;
	
	//rather raw, or half processed data
	var $data = array(
		);
	
	public function __construct( $text ) {
		$this->input = preg_replace( '/\/\*([^\*]|\*[^\/])*\*\//', '', $text );	//strip comments
		$this->offset = 0;
	}
	
	public function parseInto( DBSchema $sc ) {
		while( !$this->atEnd() ) {
			$this->parseDecl();
		}
		
		$this->process( $sc );
	}
	
	//////////////////////////////////////////////////////////
	// Semantic processing
	function process( $sc ) {
		$this->processDefaults( $sc );
		$this->processTypes( $sc );
		$this->processProviders( $sc );
		$this->processEntities( $sc );
		$this->processMappers( $sc );
		$this->processForms( $sc );
		$this->processListings( $sc );
	}
	
	function processDefaults( $sc ) {
		if( !isset( $this->data['default'] ) )
			return;
			
		//store defaults first
		foreach( $this->data['default'] as $name => $value )
			$sc->defaults[$name] = $value;
	}
	
	function processTypes( $sc ) {
		if( isset( $this->data['type'] ) )	{
			
			//then add all types
			foreach( $this->data['type'] as $name => $spec ) {
				$this->checkArray( "type $name 'base'", $spec, array( 'base'), array() );
				
				unset( $base );
				$base =& $this->parseType( "type $name", $sc, $spec['base'] );
					
				$sc->types[$name] = new DBSchema_CustomType( $name, $base );
			}
		}
		
		//we also need to treat entities as types now
		foreach( $this->data['entity'] as $name => $espec ) {
			$sc->types[$name] = new DBSchema_Entity($name);
		}
	}
	
	function &parseType( $src, $sc, $string ) {
		preg_match( '/([^<]*)(<([^>]*)>)?/', $string, $m );
		if( !isset( $m[2] ) ) {
			if( !isset( $sc->types[$m[1]] ) )
				$this->error( "$src has unrecognized type {$base}" );
				
			return $sc->types[$m[1]];
		}
			
		if( !isset( $sc->types[$m[3]] ) )
			$this->error( "$src has unrecognized collected type {$m[3]}" );
			
		if( $m[1] !== 'Array' )
			$this->error( "$src has unrecognized collection {$m[1]}" );
			
		$ret = new DBSchema_CollectionType( $m[1], $sc->types[$m[3]] );
		return $ret;
	}
	
	function processProviders( $sc ) {
		foreach( $this->data['provider'] as $name => $spec ) {
			$src = "provider $name ";
			if( !isset( $spec['type'] ) )
				$this->error( "$src requires type" );
				
			switch( $spec['type'] ) {
				case 'DBSource';
					$this->checkArray( $src, $spec, array( 'type', 'var' ), array() );
					$sc->providers[$name] = new DBSchema_Provider_DBSource( $spec['var'] );
					break;
				default:
					$this->error( "$src has invalid type: {$spec['type']}" );
			}
		}
	}
	
	function processEntities( $sc ) {
		foreach( $this->data['entity'] as $name => $espec ) {
			$src = "entity $name";
			$this->checkArray( $src, $espec, array( 'fields' ), array( 'class', 'aliases' ) );
			
			$entity =& $sc->types[$name];	//was created in the types phase
			
			if( isset( $espec['class'] ) )
				$entity->class = $espec['class'];
				
			///////////////////////////////////////////////////////////////////
			// fields
			foreach( $espec['fields'] as $fname => $spec ) {
				unset( $type );
				$type =& $this->parseType( "entity $name, $fname", $sc, $spec[0] );
				
				$field = new DBSchema_Entity_Field( $fname, $type );
				foreach( $spec[1] as $opt ) {
					if( $opt == 'RECORD_KEY' )
						$field->keyType = DBSchema_Entity_Field::KEY_TYPE_RECORD;
					else if( $opt == 'ALT_RECORD_KEY' )
						$field->keyType = DBSchema_Entity_Field::KEY_TYPE_ALT;
					else if( preg_match( '/DEFAULT\(([^\)]*)\)/', $opt, $m ) ) {
						$field->hasDefault = true;
						$field->defaultValue = $m[1];
					} else if( $opt == 'LOAD_ONLY' )
						$field->loadOnly = true;
					else if( $opt == 'TITLE' )
						$field->title = true;
					else if( preg_match( '/MAXLEN\(([^\)]*)\)/', $opt, $m ) )
						$field->maxLen = intval( $m[1] );
					else if( $opt == 'ALLOW_NULL' )
						$field->allowNull = true;
					else
						$this->error( "entity $name, unrecognized option: $opt" );
				}
					
				$entity->fields[$fname] = &$field;
				unset( $field );
			}
			
			///////////////////////////////////////////////////////////////////
			// aliases
			if( isset( $espec['aliases'] ) ) {
				foreach( $espec['aliases'] as $spec ) {
					list( $nameA, $nameB ) = $spec;
					
					$aField = isset( $entity->fields[$nameA] );
					$bField = isset( $entity->fields[$nameB] );
					if( $aField === $bField )
						$this->error( "alias $nameA = $nameB, one must be field, one not" );
						
					if( $aField ) {
						$field = $nameA;
						$alias = $nameB;
					} else {
						$field = $nameB;
						$alias = $nameA;
					}
					
					$entity->aliases[$alias] = $field;
				}
			}
			
			$sc->entities[$name] =& $entity;
			unset( $entity );
		}
	}
	
	function processMappers( $sc ) {
			
		foreach( $this->data['mapper'] as $name => $spec ) {
			$src = "mapper $name";
			//TODO: may be partially provider speficic
			$this->checkArray( $src, $spec, array( 'provider', 'table', 'fields' ), array( 'insertField' ) );
			
			if( !isset( $sc->providers[$spec['provider']] ) )
				$this->error( "$src invalid provider {$spec['provider']}" );
				
			if( !isset( $sc->entities[$name] ) )
				$this->error( "$src $name does not match any entity" );
				
			$mapper = new DBSchema_Mapper( $sc->providers[$spec['provider']] );
			$mapper->table = $spec['table'];
			$mapper->entity =& $sc->entities[$name];
			
			//setup fields
			$fields = array();
			foreach( $spec['fields'] as $data ) {
				list( $dbname, $dbtype, $func, $field, $fieldfield ) = $data;
				if( !isset( $mapper->entity->fields[$field] ) )
					$this->error( "$src field entry $dbname, $field is not in entity" );
					
				$locf = new DBSchema_Mapper_Field();
				if( $func !== null ) {
					$locf->db_convert_func = $func[0];
					$locf->db_convert_type = $this->parseType( $src, $sc, $func[1] );
				}
				$locf->db_col = $dbname;
				$locf->db_type = $this->parseType( $src, $sc, $dbtype );
				$locf->ent_field =& $mapper->entity->fields[$field];
				
				if( $fieldfield !== null ) {
					if( !($locf->ent_field->type instanceof DBSchema_Entity) )
						$this->error( "$src field $field.$fieldfield refers to sub-field of non-entity type." );
						
					if( !isset( $locf->ent_field->type->fields[$fieldfield] ) )
						$this->error( "$src field $field.$fieldfield does not exist." );
						
					$locf->ent_field_field = $locf->ent_field->type->fields[$fieldfield];
				}
				$fields[$locf->db_col] = $locf;	//naming only has value for unique items, for the purpose of insertField
			}
			$mapper->fields =& $fields;
			unset( $fields );
			
			//setup lastInsert
			if( isset( $spec['insertField'] ) ) {
				$col = $spec['insertField'];
				if( !isset( $mapper->fields[$col] ) )
					$this->error( "$src has invalid column in insertField: $col" );
				$mapper->insertField =& $mapper->fields[$col];
			}
			
			$sc->mappers[$name] =& $mapper;
			unset( $mapper );
		}
	}
	
	function processForms( $sc ) {
		if( !isset( $this->data['form'] ) )	
			return;
			
		foreach( $this->data['form'] as $name => $spec ) {
			$src = "Form $name";
			$this->checkArray( $src, $spec, array( 'entity', 'fields' ), array( 'allowDelete' ) );
			
			$form = new DBSchema_Form();
			$form->name = $name;
			$form->allowDelete = array_get_default( 'allowDelete', $spec, false );	//TODO: perhaps delete is higher level yet?
			
			//link to entity
			if( !isset( $sc->types[$spec['entity']] ) )
				$this->error( "$src refers to non-extant entity: {$spec['entity']}" );
			$form->entity = $sc->types[$spec['entity']];
			if( ! $form->entity instanceof DBSchema_Entity )
				$this->error( "$src refers to non-entity: {$spec['entity']}" );
				
			//link special fields
			foreach( $spec['fields'] as $name => $fspec ) {
				$ff = new DBSchema_Form_Field( $name );
				
				//collect options
				foreach( $fspec as $tag ) {
					switch( $tag ) {
						case 'HIDDEN':
							$ff->hidden = true;
							break;
						case 'READ_ONLY':
							$ff->readonly = true;
							break;
						default:
							$this->error( "$src field $name unrecognized option $tag" );
					}
				}
				
				$form->fields[$name] = $ff;
			}
			
			//fill in all default fields (by default, all entity fields are included)
			foreach( $form->entity->fields as $name => $field ) {
				if( !isset( $form->fields[$name] ) )
					$form->fields[$name] = new DBSchema_Form_Field( $name );
			}
			
			$sc->forms[$name] = $form;
		}
	}
	
	function processListings( DBSchema $sc ) {
		if( !isset( $this->data['listing'] ) )
			return;
			
		foreach( $this->data['listing'] as $name => $spec ) {
			$src = "Listing $name";
			$this->checkArray( $src, $spec, array( 'entity', 'fields' ), array( ) );
			
			$listing = new DBSchema_Listing();
			$listing->name = $name;
			
			//TODO: duplicate code from processForm
			if( !isset( $sc->types[$spec['entity']] ) )
				$this->error( "$src refers to non-extant entity: {$spec['entity']}" );
			$listing->entity =& $sc->types[$spec['entity']];
			if( ! $listing->entity instanceof DBSchema_Entity )
				$this->error( "$src refers to non-entity: {$spec['entity']}" );
			
			foreach( $spec['fields'] as $fspec ) {
				$field = new DBSchema_Listing_Field();
				$field->convertFunc = $fspec[1];
				
				$entfield = $fspec[0];
				if( $entfield === '@SELF' ) {
					$field->entField = null;
				} else {
					if( !isset( $listing->entity->fields[ $entfield ] ) )
						$this->error( "$src refers to non-entity field $entfield" );
					$field->entField =& $listing->entity->fields[$entfield];
				}
				
				$opts = $fspec[2];
				foreach( $opts as $opt ) {
					if( $opt[0] === '"' ) {
						if( $field->label !== null )
							$this->error( "$src duplicate label for field" );
						$field->label = substr( $opt, 1, strlen( $opt ) -2 );
					} else
						$this->error( "$src contains unknown option" );
				}
				
				if( $field->label === null )
					$field->label = $field->entField->name;	//TODO: universal labelling scheme
					
				$listing->fields[] = $field;
			}
			
			$sc->listings[$name] = $listing;
		}
	}
		
	//////////////////////////////////////////////////////////
	// Tokenizer/AST building
	
	function error( $msg ) {
		$at = substr( $this->input, $this->offset, 100 );
		throw new Exception( "$msg:@{$this->offset}: near $at" );
	}
	
	/**
	 * Ensures the that provided dataset matches what is expected of that
	 * type.
	 */
	function checkArray( $src, $array, $required, $optional ) {
		foreach( $required as $name )
			if( !isset( $array[$name] ) )
				$this->error( "$src requires $name" );
				
		foreach( $array as $name => $ignore )
			if( array_search( $name, $required ) === false && array_search( $name, $optional ) === false )
				$this->error( "$src contains superfluous $name" );
	}
	
	function addData( $decl, $name, $value ) {
		if( !isset( $this->data[$decl] ) )
			$this->data[$decl] = array();
			
		if( isset( $this->data[$decl][$name] ) )
			$this->error( "Duplicate definition for $decl $name" );
			
		$this->data[$decl][$name] = $value;
	}
	
	/**
	 * Parse decl will simply use the next found key and look for a matchin function
	 * in this with the appropriate name.
	 */
	function parseDecl()	{
		$key = $this->popDeclKey();
		$func = "parse_decl_$key";
		if( !method_exists( $this, $func ) )
			$this->error( "Unknown Decl $key" );
		$this->$func();
	}
		
	function parse_decl_default() {
		$name = $this->popID();
		$value = $this->popString();
		$this->popExprTerminal();
		
		$this->addData( 'default', $name, $value );
	}
	
	function parse_decl_type() {
		$type = $this->popID();
		$block = $this->parseBlock('var');
		$this->addData( 'type', $type, $block );
	}
	
	function parse_decl_provider() {
		$type = $this->popID();
		$block = $this->parseBlock('var');
		$this->addData( 'provider', $type, $block );
	}
	
	function parse_decl_entity() {
		$name = $this->popID();
		$block = $this->parseBlock('var', array( 'fields' => 'entity_fields', 'aliases' => 'entity_aliases' ) );
		$this->addData( 'entity', $name, $block );
	}
	
	function parse_decl_mapper() {
		$name = $this->popID();
		$block = $this->parseBlock( 'var', array( 'fields' => 'mapper_fields' ) );
		$this->addData( 'mapper', $name, $block );
	}
	
	function parse_decl_form() {
		$name = $this->popID();
		$block = $this->parseBlock( 'var', array( 'fields' => 'form_fields' ) );
		$this->addData( 'form', $name, $block );
	}
	
	function parse_decl_listing() {
		$name = $this->popID();
		$block = $this->parseBlock( 'var', array( 'fields' => 'listing_fields' ) );
		$this->addData( 'listing', $name, $block );
	}
	
	function parseBlock( $type, $field_types = array(), $setfields = true ) {
		$func = "parse_expr_$type";
		
		$block = array();
		$this->popOpen();
		while( !$this->atClose() ) {
			if( $setfields )
				list( $name, $value ) = $this->$func( $field_types );
			else
				$value = $this->$func( $field_types );
			
			if( $setfields ) {
				if( isset( $block[$name] ) )
					$this->error( "Duplicate field $name" );
				
				$block[$name] = $value;
			} else {
				$block[] = $value;
			}
		}
		$this->popClose();
		
		return $block;
	}
	
	function parse_expr_var( $field_types ) {
		$key = $this->popTypeKey();
		
		$rvalue = isset( $field_types[$key] ) ? $field_types[$key] : 'string';
		$func = "parse_rvalue_$rvalue";
		$value = $this->$func();
		
		return array( $key, $value );
	}	
	
	function parse_expr_entity() {
		$field = $this->popID();
		$type = $this->popType();
		$flags = $this->parse_flags_list();
		
		return array( $field, array( $type, $flags ) );
	}
	
	function parse_expr_field_modifier() {
		$field = $this->popID();
		$flags = $this->parse_flags_list();
		
		return array( $field, $flags );
	}
	
	function parse_flags_list() {
		$flags = array();
		while( !$this->atExprEnd() ) {	
			$tok = $this->popString();
			$flags[] = $tok;
		}
		$this->popExprTerminal();
		return $flags;
	}

	function parse_expr_listing_field() {
		//UniversalIDReg "Universal ID Regex";
		$maybeName = $this->popRefID();
		
		if( $this->atParamsOpen() ) {
			$list = $this->parseParamsList();
			
			if( count( $list ) !== 1 )
				$this->error( "Only a single field support now." );
				
			$func = $maybeName;
			$name = $list[0];
		} else {
			$name = $maybeName;
			$func = null;
		}
		
		$flags = $this->parse_flags_list();
		return array( $name, $func, $flags );
	}
	
	function parseParamsList() {
		$this->popParamsOpen();
		
		$ret = array();
		while( !$this->atParamsClose() ) {
			$ret[] = $this->popRefID();
		}
		
		$this->popParamsClose();
		return $ret;
	}
	
	function parse_expr_field() {
		$left = $this->parse_field( $this->popEqLeft() );
		$right = $this->parse_field( $this->popEqRight() );
		if( $left[0] === $right[0] )
			$this->error( "Left and right must all of DB type and intern field" );
		if( $left[0] ) {	//0 "isDB" column
			$dbcol = $left[1];
			$dbtype = $left[2];
			$dbfunc = $left[3];
			$entfield = $right[1];
			$entfieldfield = $right[4];
		} else {
			$dbcol = $right[1];
			$dbtype = $right[2];
			$dbfunc = $right[3];
			$entfield = $left[1];
			$entfieldfield = $right[4];
		}

		return array( $dbcol, $dbtype, $dbfunc, $entfield, $entfieldfield );
	}
	
	function parse_expr_alias_field() {
		//quick version, should ultimately support the same as parse_expr_field, accepting conversion functions
		$left = $this->parse_field( $this->popEqLeft() );
		$right = $this->parse_field( $this->popEqRight() );
		
		return array( $left[1], $right[1] );
	}
	
	function parse_field( $text ) {
		$func = null;
		
		//Ex: 	fmearawnotice_tags<Array<String>>( @Tags<String> )
		if( preg_match( '/^\s*([\p{L}_]+)<([^\)]+)>\(\s*([^\)]+)\s*\)\s*$/u', $text, $m ) == 1 ) {
			$func = array( $m[1], $m[2] );	//Ex: array( 'fmearawnotice_tags', 'Array<String>' )
			$text = $m[3];	//Ex: '@Tags<String>'
		}
		
		//Ex: @Tags<String>
		//Ex: Score
		if( preg_match( '/^\s*(@)?([\p{L}_]+)(\.([\p{L}_]+))?(<([^\]]+)>)?\s*$/u', $text, $m ) != 1 )
			$this->error( "Invalid field: $text" );
		
		$db = isset($m[1]) && strlen( $m[1] );	// @ modifier
		$type = isset( $m[5] ) && strlen( $m[5] );	// <TYPE>
		if( $db !== $type )
			$this->error( "DB field marker and type must both be used: $text" );
			
		if( $db )
			return array( true, $m[2], $m[6], $func, null );
			
		return array( false, $m[2], null, $func, isset($m[4]) ? $m[4] : null );
	}
	
	function parse_rvalue_string() {
		$val = $this->popString();
		$this->popExprTerminal();
		return $val;
	}
	
	function parse_rvalue_block() {
		return $this->parseBlock( 'var' );
	}
	
	function parse_rvalue_mapper_fields() {
		return $this->parseBlock( 'field', array(), false /*setfields*/ );
	}
	
	function parse_rvalue_entity_fields() {
		return $this->parseBlock( 'entity', array(), true /*setfields*/ );
	}
	
	function parse_rvalue_form_fields() {
		return $this->parseBlock( 'field_modifier', array(), true /*setfields*/  );
	}
	
	function parse_rvalue_listing_fields() {
		return $this->parseBlock( 'listing_field', array(), false /*setfields*/ );
	}
	
	function parse_rvalue_entity_aliases() {
		return $this->parseBlock( 'alias_field', array(), false /*setfields*/ );
	}
	
	/** Checks for the end of the input stream */
	function atEnd()	{
		return $this->atRegex( '$' );
	}
	
	function atExprEnd()	{
		return $this->atRegex( ';' );
	}
	
	function atClose() {
		return $this->atRegex( '}' );
	}
	
	function atParamsOpen() {
		return $this->atRegex( '\(' );
	}
	
	function atParamsClose() {
		return $this->atRegex( '\)' );
	}
	
	function atRegex( $regex ) {
		return preg_match( '/^\s*' . $regex . '/', substr( $this->input, $this->offset) ) == 1;
	}
	
	/************************************************************************************
	 * the pop series of functions removes a token from the input stream. Generally
	 * each token is a regex and uses the popRegex function.
	 */
	function popRegex( $name, $regex ) {
		//is this continuous substr inefficient... we need it since offset mode doesn't work since we need ^ to match
		//NOTE: /u seems required on the old version on Suse@QA, but not in the newer PHP builds
		$ret = preg_match( '/^\s*' . $regex . '/u', substr( $this->input, $this->offset ), $m, PREG_OFFSET_CAPTURE );
		if( $ret != 1 )
			$this->error( "Expected $name" );
			
		$this->offset += $m[0][1] + strlen( $m[0][0] );
		return $m[1][0];		
	}
	
	function popDeclKey() {	
		return $this->popID( 'DeclKey' );
	}
	
	function popTypeKey() {
		return $this->popID( 'TypeKey' );
	}
	
	function popID( $name = 'ID' ) {
		return $this->popRegex( $name, '([\p{L}_]+)(?=[\s;\(])' );
	}
	
	function popRefID() {	//just like popID, but supports @SELF
		return $this->popRegex( 'Reference ID', '(([\p{L}_]+)|@SELF)(?=[\s;\(])' );
	}
	
	function popString() {
		return $this->popRegex( 'String', '(([^\s;"]+)|("[^"]+"))' );
	}
	
	function popExprTerminal() {
		return $this->popRegex( 'ExprTerminal', '(;)' );
	}
	
	function popOpen() {	
		return $this->popRegex( 'Open', '({)' );
	}
	
	function popClose() {	
		return $this->popRegex( 'Open', '(})' );
	}
	
	function popParamsOpen() {	
		return $this->popRegex( 'Params Open', '(\()' );
	}
	
	function popParamsClose() {	
		return $this->popRegex( 'Params Close', '(\))' );
	}
	
	function popType() {
		return $this->popRegex( 'Type', '([\p{L}_<>]+)' );
	}
	
	function popEqLeft() {
		return $this->popRegex( 'EqLeft', '([^=;]+)=' );
	}
	
	function popEqRight() {
		return $this->popRegex( 'EqRight', '([^;]*);' );
	}
	
}

function _dbschema_parse( $text ) {
	$sc = new DBSchema();
	$p = new DBSchema_Parser( $text );
	$p->parseInto( $sc );
	
	return $sc;
}

?>