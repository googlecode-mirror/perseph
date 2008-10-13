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

require_once dirname(__FILE__).'/dbsource.inc';
require_once dirname(__FILE__).'/base.inc';

abstract class DBS_FormBase {

	const ACTION_NONE = 0;
	const ACTION_SAVE = 1;
	const ACTION_DELETE = 2;
	const ACTION_ADD = 3;
	
	/**
	 * Performs form validation.
	 *
	 * @return [out] true if everything is okay, false otherwise
	 */
	abstract public function validate();
	
	/**
	 * Extracts data from the form into the entity provided.
	 */
	abstract public function extract( $entity );
	
	/**
	 * Take the values from the entity and put them in the form
	 */
	abstract public function inject( $entity );
	
	/**
	 * Obtains what action was called on this form. Note that
	 * ACTION_NONE does not necessarily imply that hasAction is
	 * false.
	 */
	abstract public function getAction();
	
	/** 
	 * This can be used to determine whether the form has been submitted yet,
	 * or this will be the first instance of the form (such as on first page access).
	 *
	 * This is a static since you will likely need to know this before creating
	 * the form object.
	 *
	 * @return [out] true indicates that some action  has been performed with the
	 *		form, false indicates no action has yet been performed.
	 */
	abstract public function hasAction();
}

/**
 * A common base class (abstract) for HTML forms.
 */
abstract class DBS_FormBase_HTMLForm extends DBS_FormBase {

	public $ENTITY = null;	//the class of the entity involved  (Override in derived class)
	
	protected $isNew = false; //<Bool> a new object is being created (set by this class)
	protected $createFrom;	//<Entity> created from this entity (set by this class)
	
	protected $allowAddSave = true;	//can the item be added/saved (Override in derived class)
	protected $allowDelete = true;	//can the item be deleted (Override in derived class)
	
	/** 
	 * Initializes the form from the request parameters. This is called
	 * when a form is submitted.
	 */
	public function initFromRequest() {
		$this->_setup();
		$this->isNew = $this->isRequestNew();
	}
	
	/**
	 * Initiailizes a new form using the provided entity.  This entity
	 * should be marked for retrieval in the request such that initFromRequest
	 * can obtain it.	 
	 * This is called when a form is first created (before first submission)
	 *
	 * @param from [*] if not null loads the form to edit this object, otherwise
	 *		a new object will be created
	 */
	public function initCreate( $from = null ) {
		$this->_setup();
		$this->createFrom = $from;
		$this->isNew = $from === null || $from->isNew();
	}
	
	abstract protected function _setup();
	
	/**
	 * Called from execute to display the form.
	 *
	 * @return [out] returns the HTML rendering of the form
	 */
	abstract public function toHTML();
	
	const T_SUBMITROW = 'submitrow'; //TODO: unique name per form, to distinguish multiple forms
	const T_ACTION_SAVE = 'save';
	const T_ACTION_DELETE = 'delete';
	const T_ACTION_ADD = 'add';
	const T_ACTIONMARKER = '_dbs_actionmarker';	//TODO: unique name per form, to distinguish in hasAction
	const T_MARKNEW = '_dbsfq_new';	//TODO: unique per form
	
	public function getAction() {
		//see note in hasAction about exportValue
		$sr = isset( $_REQUEST[self::T_SUBMITROW] ) ? $_REQUEST[self::T_SUBMITROW] : null;
		if( $sr === null )
			return DBS_FormBase::ACTION_NONE;
		$act = key( $sr );
		switch( $act ) {
			case self::T_ACTION_SAVE:
				return DBS_FormBase::ACTION_SAVE;
			case self::T_ACTION_DELETE:
				return DBS_FormBase::ACTION_DELETE;
			case self::T_ACTION_ADD:
				return DBS_FormBase::ACTION_ADD;
			default:
				return DBS_FormBase::ACTION_NONE;
		}
	}
		
	public function hasAction() {
		//don't use exportValue since it requires the actions to have already been added
		//in the form, and stick this directly in the template
		return array_get_default( self::T_ACTIONMARKER, $_REQUEST, '0' ) == '1';
	}
	
	public function isRequestNew() {
		return array_get_default( self::T_MARKNEW, $_REQUEST, '0' ) == '1';
	}
	
	public function execute() {
		if( !$this->hasAction() ) {
			if( $this->createFrom !== null )
				$this->inject( $this->createFrom );
		}
			
		$showForm = true;
		if( $this->validate() ) {
			if( $this->isNew ) {
				$rule = call_user_func( "{$this->ENTITY}::createWithNothing" );
			} else {
				$rule = call_user_func( "{$this->ENTITY}::withIdentifier", $this->getIdentifier() );
				//$this->extractKeys( $rule );
				$rule->find();
			}
			
			try {
				$this->extract( $rule );
				if( $this->getAction() == DBS_FormBase::ACTION_SAVE ) {
					$rule->save();
					$this->inject( $rule, true );	//capture any logic/new values from entity
					print( "<p class='success'>Saved.</p>" );
				} else if( $this->getAction() == DBS_FormBase::ACTION_ADD ) {
					$rule->add();
					$this->isNew = false;
					$this->inject( $rule, true );	//capture any logic/new values from entity
					print( "<p class='success'>Added.</p>" );
				} else if( $this->getAction() == DBS_FormBase::ACTION_DELETE ) {
					$rule->delete();
					$showForm = false;
					print( "<p class='success'>Deleted.</p>" );
				}
			} catch( DBS_SetFieldException $ex ) {
				//just do something quick and dirty for now, TODO: combine with HTMLQuickForm to report validation errors
				print( "<p class='error'>{$ex->getMessage()}</p>" );
			}
			//TODO: Other exceptions...
		}
		
		if( $showForm )
			echo $this->toHTML();
	}
	
}

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
		return $this->form->validate();
	}
	
	protected $elements = array();
	
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
	 */
	protected function addElement( $type, $field, $label = null, $options = null ) {
		$typeDesc = call_user_func( "{$this->ENTITY}::getTypeDescriptor" );
		
		if( $label === null )
			$label = $typeDesc->getDefaultLabel( $field );
			
		if( $type == 'static' ) {
			$this->form->addElement( 'static', "_ro__dbs_{$field}", $label );
			//add a readable form for JS or checking programs
			$this->form->addElement( 'hidden', "_hro__dbs_${field}" );
			
			$this->elements[] = array( $field, false, "_ro__dbs_{$field}" );
			$this->elements[] = array( $field, false, "_hro__dbs_{$field}" );
		} else if( $type == 'select' ) {
			$selOpts = $options['options'];
			$this->form->addElement( 'select', "_dbs_{$field}", $label, $selOpts );
			$this->elements[] = array( $field, true, "_dbs_{$field}" );
		} else {
			//add max length if there
			$maxLen = $typeDesc->getFieldOption( $field, 'maxLength' );
			if( $maxLen !== null && !array_key_exists( 'maxlength', $options ) )	//don't overwrite an existing value
				$options['maxlength'] = $maxLen;
				
			$this->form->addElement( $type, "_dbs_{$field}", $label, $options );
			$this->elements[] = array( $field, true, "_dbs_{$field}" );
			
			//check numeric types
			if( array_search( $typeDesc->getBaseType( $field ), array( 'Integer', 'Decimal', 'Float' ) ) !== false )
				$this->form->addRule( "_dbs_{$field}", "{$label} must be numeric.", 'numeric', true, 'client' );
		}
	}
	
	protected function addStaticElement( $field, $label = null ) {
		$this->addElement( 'static', $field, $label );
	}
	
	protected function addTypicalElement( $field, $label = null ) {
		$typeDesc = call_user_func( "{$this->ENTITY}::getTypeDescriptor" );
		$baseType = $typeDesc->getBaseType( $field );
		if( array_search( $baseType, array( 'String', 'Integer', 'Decimal', 'Float', 'DateTime', 'Date', 'Time' ) ) !== false )
			$this->addElement( 'text', $field, $label );
		else if( $baseType === 'Text' )
			$this->addElement( 'textarea', $field, $label );
		else if( $baseType === 'Bool' )
			$this->addSelectElement( $field, array( 0 => 'False', 1 => 'True' ), $label );		
		else
			throw new Exception( "Unsupported type: $baseType" );
	}
	
	protected function addSelectElement( $field, $options, $label = null ) {
		assert( 'count($options) > 0' );
		$typeDesc = call_user_func( "{$this->ENTITY}::getTypeDescriptor" );
		$baseType = $typeDesc->getBaseType( $field );
		if( $baseType === 'Entity' ) {
			$customType = $typeDesc->getCustomType($field);
			$titleField = call_user_func( "{$customType}::getTypeDescriptor" )->getOption( 'titleField' );
			if( $titleField === null )
				throw new Exception( "{$customType} does not define a title field for {$baseType}::{$field}" );
			$this->addElement( 'select', $field, $label, array( 'options' => _dbs_form_loadentityselect( $options, 'identifier', $titleField ) ) );
		} else
			$this->addElement( 'select', $field, $label, array( 'options' => $options ) );
		
	}
	
	/** 
	 * NOTE: derived classes must call the parent version of this function!
	 */
	protected function _setup() {
		$this->form = new HTML_QuickForm( get_class($this), 'POST', '', '', array( 'class' => 'dbsform' ) );
		$this->form->addElement( 'hidden', '_key_ident' );
	}
	
	
	public function inject( $entity, $overrideRequest = false ) {
		$values = array();
		
		$typeDesc = call_user_func( "{$this->ENTITY}::getTypeDescriptor" );
		
		foreach( $this->elements as $element ) {
			if( $entity->__has( $element[0] ) ) {
				
				$baseType = $typeDesc->getBaseType( $element[0] );
				$raw = $entity->__get( $element[0] );
				if( $baseType === 'Entity' )
					$raw = $raw->identifier;
				else {
					$func = "_dbs_formin_{$baseType}";
					$raw = $func( $raw );
				}
					
				$values[$element[2]] = $raw;
			}
		}
		
		$values['_key_ident'] = $entity->getIdentifier();
		
		if( $overrideRequest )
			$this->form->setConstants( $values );
		else
			$this->form->setDefaults( $values );
		
	}
	
	protected function getIdentifier( ) {
		return $this->form->exportValue( '_key_ident' );
	}
	
	public function extract( $entity ) {
		$typeDesc = call_user_func( "{$this->ENTITY}::getTypeDescriptor" );
		foreach( $this->elements as $element ) {
			if( !$element[1] )
				continue;
				
			$baseType = $typeDesc->getBaseType( $element[0] );
			$raw = $this->form->exportValue( $element[2] );
			if( $baseType === 'Entity' ) {
				$raw = call_user_func( "{$typeDesc->getCustomType($element[0])}::withIdentifier", $raw );
			} else {
				$func = "_dbs_formout_{$baseType}";
				$raw = $func( $raw );
			}
			
			$entity->__set( $element[0], $raw );
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
		$render->setElementTemplate( "
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
			");
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
	
		$this->form->accept( $render );
		return $render->toHtml();
	}
}

function _dbs_formin_Integer( $value ) { return $value === null ? '' : '' . $value; }
function _dbs_formin_String( $value ) {	return $value === null ? '' : $value; }
function _dbs_formin_Text( $value ) {	return $value === null ? '' : $value; }
function _dbs_formin_Decimal( $value ) { return $value === null ? '' : '' . $value; }
function _dbs_formin_Float( $value ) { return $value === null ? '' : '' . $value; }
function _dbs_formin_Bool( $value ) {	return $value === null ? '' : $value ? '1' : '0'; }
function _dbs_formin_DateTime( $value ) {	return $value === null ? '' : date( 'Y-m-d H:i:s', $value ); }
function _dbs_formin_Date( $value ) {	return $value === null ? '' : date( 'Y-m-d', $value ); }
function _dbs_formin_Time( $value ) {	return $value === null ? '' : _dbs_encode_time($value ); }

function _dbs_formout_Integer( $value ) { return $value === '' ? null : intval( $value ); }
function _dbs_formout_String( $value ) {	return $value; }
function _dbs_formout_Text( $value ) {	return $value; }
function _dbs_formout_Decimal( $value ) { return $value === '' ? null : floatval( $value ); }
function _dbs_formout_Float( $value ) { return $value === '' ? null : floatval( $value ); }
function _dbs_formout_Bool( $value ) {	return $value === '' ? null : '1' === $value; }
function _dbs_formout_DateTime( $value ) { return $value === '' ? null : strtotime( $value ); }
function _dbs_formout_Date( $value ) { return $value === '' ? null : strtotime( $value ); }
function _dbs_formout_Time( $value ) { return $value === '' ? null : _dbs_decode_time( $value ); }

function _dbs_form_loadentityselect( $results, $key, $text ) {
	$ret = array();
	foreach( $results as $result )
		$ret[$result->$key] = $result->$text;
	return $ret;
}

/**
 * Does a  very standard form setup, either editing an entity or creating a
 * new one with defaults.
 *
 * @param formclass [in] which form class to use, implies the entity
 * @param entitykey [in] which findWith function to use (such as "ID") and
 *		also specifies the request parameter used to indicate this parameter, 
 *		if not specified in request then a new item is assumed
 * @param defaultsForNew [in] if the key is not in the request, then these
 *		defaults are set in the form.  Form:
 *			memberName -> value
 *		If value is null the item will not be set (this is for convenience)
 */
function dbs_standard_form( $form, $entitykey, $defaultsForNew = null ) {
	if( !$form->hasAction() ) {
		$key = array_get_default( $entitykey, $_REQUEST, null );	//TODO: unlike the get_request_def this doesn't handle encoding correctly!!!
		$entityname = $form->ENTITY;
		//for PHP 5.3 (and can also replace call_user_func)
		//$entityname = $formclass::ENTITY
		if( $key !== null ) 
			$rule = call_user_func( "$entityname::findWith$entitykey", $key );
		else if( $defaultsForNew !== null ) {
			$rule = call_user_func( "$entityname::createWithNothing" );
			foreach( $defaultsForNew as $member => $value ) {
				if( $value !== null )
					$rule->$member = $value;
			}
		} else
			$rule = null;
			
		$form->initCreate( $rule );
	} else {
		$form->initFromRequest( );
	}
	return $form;
}

?>
