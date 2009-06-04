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

/**
 * This produces a hierarchical view of the object -- essentially all
 * the data less the persphone wrappers and overhead.  The data
 * will have names equivalent to the True Names coming from the
 * schema (not the internal PHPized names)
 *
 * @param $object [in] from which object to export the data
 * @param $recurse [in] if a further entity is found it will also be exported,
 *		limited to this depth.  If the depth would clip the entity then the
 *		identifier of the entity is exported instead.
 *
 * NOTE: if the object is incomplete then this will simply export the
 * parts which are defined.  You need to take care of loading before hand.
 *
 * NOTE: Internally used, or common types, which are used as basic
 * types (like Date) will also be flattened to a string representation.  This
 * means that export should never contain objects in the returned data. It
 * may however contain arrays if they are part of the entity.
 */
function export_entity( DBS_EntityBase $object, $recurse = 0 ) {
	$root = array();
	
	$type = $object->getType();
	foreach( $type->getFields() as $field ) {
		if( !$object->__has( $field ) )
			continue;
			
		$value = $object->$field;
		if( $value instanceof DBS_EntityBase ) {
			if( $recurse > 0 )
				$value = export_entity( $value, $recurse - 1 );
			else
				$value = $value->identifier;
		} else if( $value instanceof DateTime ) {
			$value = $value->format( DateTime::ISO8601 );
		}
		
			
		$root[$type->getFieldOption( $field, 'trueName' )] = $value;
	}
	return $root;
}

function import_entity( $entityType, $data ) {
	$entity = call_user_func( "$entityType::withNothing" );
	
	$type = $entity->getType();
	foreach( $data as $name => $value ) {
		$field = $type->getFieldName( $name );
		
		//TODO: just allow the type descriptor to fail if field is not found for now, the todo is
		//that it doesn't have an explicit check (PHP standard failure)
		$base = $type->getBaseType( $field );

		if( $base === 'Entity' ) {
			$etype = $type->getCustomType( $field );
			if( is_array( $value ) )
				$value = import_entity( $etype, $value );
			else if( is_null( $value ) )
				$value = null;
			else
				$value = call_user_func( "$etype::withIdentifier", $value );
		} else if( $base === 'DateTime' || $base === 'Date' ) {
			$value = new DateTime( $value );
		}
		
		$entity->$field = $value;
	}
	
	return $entity;
}

?>