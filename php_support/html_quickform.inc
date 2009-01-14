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

require_once dirname(__FILE__).'/form_base.inc';

require_once 'HTML/QuickForm.php';
require_once 'HTML/QuickForm/Renderer/Default.php';	

/**
 * A convenience class to use QuickForm with a standard layout for a form.
 *
 * NOTE: we split of the initial form creation and actions as the action part
 * changes depending on validation (which requires the basics to be setup
 * already).
 */
abstract class DBS_FormBase_QuickForm extends DBS_FormBase_HTMLForm {
	
	protected $form;	//<HTML_QuickForm>
	
	public function validate() {
		$this->checkExtract( null );
		return $this->form->validate();
	}
	
	protected $elements = array();
	private $nameMap = array();	//field => form name
	
	/**
	 * A parallel to the QuickForm addElement this will add an appropriate field for
	 * the member -- extracting default options as appropriate.
	 *
	 * @param type [in] QuickForm type
	 * @param field [in] field in the entity mapped to this element
	 * @param label [in] label to use, if null the persephone default label will be used
	 * @param options [in] options for this element.
	 *		NOTE: unlike QuickForm, the options for a "select" type should be passed
	 *		as an sub-array under the name "options"
	 *
	 * @return [out] the final HTML name of the element which will be created
	 */
	protected function addElement( $type, $field, $label = null, $options = array() ) {
		$typeDesc = call_user_func( "{$this->ENTITY}::getTypeDescriptor" );
		
		if( $label === null )
			$label = $typeDesc->getDefaultLabel( $field );
			
		$fieldName = "_dbs_{$field}";
		if( $type == 'static' ) {
			$this->form->addElement( 'static', "_ro__dbs_{$field}", $label );
			//add a readable form for JS or checking programs
			$fieldName = "_hro__dbs_{$field}";
			$this->form->addElement( 'hidden', $fieldName );
			
			$this->elements[] = array( $field, false, "_ro__dbs_{$field}", $options );
			$this->elements[] = array( $field, false, $fieldName, $options );
		} else if( $type == 'select' ) {
			$selOpts = $options['options'];
			$this->form->addElement( 'select', $fieldName, $label, $selOpts );
			$this->elements[] = array( $field, true, $fieldName, $options );
		} else {
			//add max length if there
			$maxLen = $typeDesc->getFieldOption( $field, 'maxLength' );
			if( $maxLen !== null && !array_key_exists( 'maxlength', $options ) )	//don't overwrite an existing value
				$options['maxlength'] = $maxLen;
				
			$this->form->addElement( $type, $fieldName, $label, $options );
			$this->elements[] = array( $field, true, $fieldName, $options );
			
			//check numeric types
			if( array_search( $typeDesc->getBaseType( $field ), array( 'Integer', 'Decimal', 'Float' ) ) !== false )
				$this->form->addRule( $fieldName, "{$label} must be numeric.", 'numeric', true, 'client' );
		}
		
		$this->nameMap[$field] = $fieldName;
		return $fieldName;
	}
	
	/**
	 * @return [out] as in addElement
	 */
	protected function addStaticElement( $field, $label = null ) {
		return $this->addElement( 'static', $field, $label );
	}
	
	/**
	 * @return [out] as in addElement
	 */
	protected function addTypicalElement( $field, $label = null ) {
		$typeDesc = call_user_func( "{$this->ENTITY}::getTypeDescriptor" );
		$baseType = $typeDesc->getBaseType( $field );
		if( array_search( $baseType, array( 'String', 'Integer', 'Decimal', 'Float', 'DateTime', 'Date', 'Time' ) ) !== false )
			return $this->addElement( 'text', $field, $label );
		else if( $baseType === 'Text' )
			return $this->addElement( 'textarea', $field, $label );
		else if( $baseType === 'Bool' )
			return $this->addSelectElement( $field, array( 0 => 'False', 1 => 'True' ), $label );		
		else
			throw new Exception( "Unsupported type: $baseType" );
	}
	
	/**
	 * @return [out] as in addElement
	 */
	protected function addSelectElement( $field, $options, $label = null ) {
		assert( 'count($options) > 0' );
		$typeDesc = call_user_func( "{$this->ENTITY}::getTypeDescriptor" );
		$baseType = $typeDesc->getBaseType( $field );
		if( $baseType === 'Entity' ) {
			$customType = $typeDesc->getCustomType($field);
			$titleField = call_user_func( "{$customType}::getTypeDescriptor" )->getOption( 'titleField' );
			if( $titleField === null )
				throw new Exception( "{$customType} does not define a title field for {$baseType}::{$field}" );
			//use "identifier" here, not solo identifier, to ensure a correct match is done.
			//FEATURE: create a better matching routine so that fource loading is not required...
			return $this->addElement( 'select', $field, $label, array( 'options' => _dbs_form_loadentityselect( $options, 'identifier', $titleField ) ) );
		} else
			return $this->addElement( 'select', $field, $label, array( 'options' => $options ) );
		
	}
	
	/** 
	 * NOTE: derived classes must call the parent version of this function!
	 */
	protected function _setup() {
		$this->form = new HTML_QuickForm( get_class($this), 'POST', '', '', array( 'class' => 'dbsform' ) );
		$this->form->addElement( 'hidden', '_key_ident' );
		
		foreach( $this->privateValues as $name => $value )
			$this->form->addElement( 'hidden', $name );
	}
	
	
	public function inject( $entity, $overrideRequest = false ) {
		$values = array();
		
		$typeDesc = call_user_func( "{$this->ENTITY}::getTypeDescriptor" );
		
		foreach( $this->elements as $element ) {
			//either use the existing value or a defaultForNew if applicable
			if( $entity !== null && $entity->__has( $element[0] ) )
				$raw = $entity->__get( $element[0] );
			else if( $this->isNew && isset( $this->defaultsForNew[ $element[0] ] ) )
				$raw = $this->defaultsForNew[ $element[0] ];
			else
				continue;
				
			$baseType = $typeDesc->getBaseType( $element[0] );
			if( isset( $element[3]['convertIn'] ) ) {	
				$func = $element[3]['convertIn']; 
				$raw = $func($raw);
			} else if( $baseType === 'Entity' )
				$raw = $raw->identifier;	//see comment in addSelect
			else {
				$func = "_dbs_formin_{$baseType}";
				$raw = $func( $raw );
			}
				
			$values[$element[2]] = $raw;
		}
				
		if( $entity !== null )
			$values['_key_ident'] = $entity->getAnyIdentifier();
		
		foreach( $this->privateValues as $name => $value )
			$values[$name] = $value;
			
		if( $overrideRequest )
			$this->form->setConstants( $values );
		else
			$this->form->setDefaults( $values );
		
	}
	
	protected function getIdentifier( ) {
		return $this->form->exportValue( '_key_ident' );
	}
	
	/**
	 * Check extract is an internal function which either extracts the value or checks it
	 * for correctness (used in validate).
	 */
	function checkExtract( $entity ) {
		$typeDesc = call_user_func( "{$this->ENTITY}::getTypeDescriptor" );
		foreach( $this->elements as $element ) {
			if( !$element[1] )
				continue;
				
			try {
				$baseType = $typeDesc->getBaseType( $element[0] );
				$raw = $this->form->exportValue( $element[2] );
				if( $baseType === 'Entity' ) {
					$raw = call_user_func( "{$typeDesc->getCustomType($element[0])}::withIdentifier", $raw );
				} else {
					$func = "_dbs_formout_{$baseType}";
					$raw = $func( $raw );
				}
			
				if( $entity !== null )
					$entity->__set( $element[0], $raw );
					
			} catch( Exception $ex ) {
				$this->form->setElementError( $element[2], $ex->getMessage() );
			}
		}
	}
	
	public function extract( $entity ) {
		$this->checkExtract( $entity );
				
		//additionally if the entity is new and we have not extracted the value from the form
		//we can get it from the defaultsForNew
		if( $this->isNew ) {
			foreach( $this->defaultsForNew as $field => $value )
				if( !$entity->__has( $field ) )
					$entity->__set( $field, $value );
		}
	}
	
	protected function addActions() {
		$submit = array();
		
		if( $this->allowAddSave ) {
			if( $this->isNew )
				$submit[] = $this->form->createElement( 'submit', DBS_FormBase_QuickForm::T_ACTION_ADD, 'Add' );
			else 
				$submit[] = $this->form->createElement( 'submit', DBS_FormBase_QuickForm::T_ACTION_SAVE, 'Save' );
		}
		
		if( $this->allowDelete && !$this->isNew )
			$submit[] = $this->form->createElement( 'submit', DBS_FormBase_QuickForm::T_ACTION_DELETE, 'Delete' );
		
		//allow nothign to be there -- perhaps only web form or read-only
		if( count( $submit ) )
			$this->form->addGroup( $submit, DBS_FormBase_QuickForm::T_SUBMITROW );
	}
	
	private $actionsAdded = false;
	
	public function toHTML() {
		//hopefully this is done after having validated the form
		if( !$this->actionsAdded ) {
			$this->addActions();
			$this->actionsAdded =true;
		}
	
		$render = $this->getRenderer();
		$this->form->accept( $render );
		return $render->toHtml();
	}
	
	private $renderElementTemplates = array();
	/**
	 * allows adjusting just the input part of the element control.  Useful to add a JS button
	 * or control.
	 *
	 * @param field [in] for which field to set the template
	 * @param tpl [in] the template to use, the {element} section of the normal template will
	 *		be replaced with this segment -- therefore be sure to use {element} in the text
	 */
	protected function renderSetElementInputTemplate( $field, $tpl ) {
		$full = str_replace( "{element}", $tpl, self::_renderElementTpl );
		$this->renderSetElementTemplate( $field, $full );
	}
	
	protected function renderSetElementTemplate( $field, $tpl ) {
		$this->renderElementTemplates[$field] = $tpl;
	}
	
	const _renderElementTpl = "
		<tr>
			<td class='name'>
				<!-- BEGIN required --><span style=\"color: #ff0000\">*</span><!-- END required -->
				{label}
			</td>
			<td class='value'>
				{element}
				<!-- BEGIN error --><br/><span style=\"color: #ff0000\">{error}</span><!-- END error -->
			</td>
		</tr>
			";
			
	/**
	 * This function may be overriden to either extend the renderer or provide
	 * an entirely new one.
	 */
	protected function getRenderer() {
		//////////////////////////////////////////////////////////////////////////////////////
		//The other template engines, being used with QuickForm suffer from a significant
		//lack of documentation, and several bugs, this one is also too limited, but it'll be
		//fine for now.
		$render = new HTML_QuickForm_Renderer_Default();
		$render->setFormTemplate( "
			<form{attributes}>
				<input type='hidden' name='" . self::T_ACTIONMARKER . "' value='1'/>
				<input type='hidden' name='" . self::T_MARKNEW . "' value='" . ($this->isNew ? '1' : '0') . "'/>
				<table class='data_bound'><tr><td><fieldset class='data table'><table class='data'>
					{content}
				</table></fieldset></tr></td></table>
			</form>
			");
		$render->setElementTemplate( self::_renderElementTpl );
		foreach( $this->renderElementTemplates as $field => $tpl )
			$render->setElementTemplate( $tpl, $this->nameMap[$field] );
		$render->setHeaderTemplate( "
			<tr class='header'>
				<td colspan='2'>{header}</td>
			</tr>
			");		
		$render->setGroupTemplate( "
			<tr class='submit'>
				<td colspan='2' class='submit'>
					{content}
				</td>
			</tr>
			", "submitrow"
			);
		return $render;
	}
}

?>