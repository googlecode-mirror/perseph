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
require_once dirname(__FILE__).'/entity_base.inc';

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
	 *
	 * @param enity [out] into where should the values be extract (may not be null)
	 */
	abstract public function extract( $entity );
	
	/**
	 * Take the values from the entity and put them in the form. 
	 *
	 * @param entity [in] from where to take the values, null may be
	 *		used to say from nowhere (in which case only defaults and special
	 *		settings will be injected)
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
	
	public function isNewEntity() {
		return $this->isNew;
	}
	
	/**
	 * Adds a name=value pair to the form so that on submission the server will
	 * get it back.
	 *
	 * NOTE: Must be called before an "init" request
	 * NOTE: Derived classes must use the values collected here
	 */
	public function addPrivate( $name, $value ) {
		$this->privateValues[$name] = $value;
	}
	protected $privateValues = array();
	
	/**
	 * Sets field values for entities when new entities are being created.
	 * Note that fields set in the form will override these.  For example, if
	 * you specifc a text field for "Name" with a default, the first display
	 * of the form will use that default, but on submission it will used whatever
	 * the user entered.
	 *
	 * However, if the field is of type "static" then the value will *NOT* be
	 * submitted and the new default will be used again. So you need to
	 * specify the same set of defaults each time the form is created.
	 * (Not submitting read-only fields is a security feature to prevent the
	 * user from overwriting them.  In future versions we could support
	 * encrypting the defaults.)
	 */
	public function setDefaultsForNew( $defaults ) {
		$this->defaultsForNew = $defaults;
	}
	protected $defaultsForNew = array();
	
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
		return _pers_array_get_default( self::T_ACTIONMARKER, $_REQUEST, '0' ) == '1';
	}
	
	public function isRequestNew() {
		return _pers_array_get_default( self::T_MARKNEW, $_REQUEST, '0' ) == '1';
	}
	
	public function execute() {
		if( !$this->hasAction() ) {
			$this->inject( $this->createFrom );
		}
			
		$showForm = true;
		//in Delete we don't need to validate
		if( $this->getAction() == DBS_FormBase::ACTION_DELETE || $this->validate() ) {
			//obtain the entity we are working with
			if( $this->isNew ) {
				$entity = call_user_func( "{$this->ENTITY}::createWithNothing" );
			} else {
				$entity = call_user_func( "{$this->ENTITY}::withIdentifier", $this->getIdentifier() );
				$entity->find();
			}
			
			try {
				if( $this->getAction() == DBS_FormBase::ACTION_SAVE ) {
					$this->extract( $entity );
					$entity->save();
					$this->inject( $entity, true );	//capture any logic/new values from entity
				} else if( $this->getAction() == DBS_FormBase::ACTION_ADD ) {
					$this->extract( $entity );
					$entity->add();
					$this->isNew = false;
					$this->inject( $entity, true );	//capture any logic/new values from entity
				} else if( $this->getAction() == DBS_FormBase::ACTION_DELETE ) {
					//don't extract in this case
					$entity->delete();
				}
				
				$showForm = $this->actionSuccess( $this->getAction(), $entity );
				
			} catch( DBS_SetFieldException $ex ) {
				//just do something quick and dirty for now, TODO: combine with HTMLQuickForm to report validation errors
				print( "<p class='error'>{$ex->getMessage()}</p>" );
			}
			//TODO: Other exceptions...
		}
		
		if( $showForm )
			echo $this->toHTML();
	}
	
	/**
	 * Called when an action is successfully performed with the form.  This can be overridden
	 * to provide different output, or control form display.
	 *
	 * @param action [in] which action DBS_FormBase::ACTION_
	 * @param entity [in] the entity which was operated on
	 * @return [out] true if the form should be display again, false if to not display the form
	 *
	 * NOTE: Delete should normally return "false", otherwise the resulting form may
	 *	be unusuable on the deleted entity.
	 */
	/*virtual*/ public function actionSuccess( $action, $entity ) {
		if( $action == DBS_FormBase::ACTION_SAVE ) {
			print( "<p class='success'>Saved.</p>" );
			return true;
			
		} else if( $action == DBS_FormBase::ACTION_ADD ) {
			print( "<p class='success'>Added.</p>" );
			return true;
			
		} else if( $action == DBS_FormBase::ACTION_DELETE ) {
			print( "<p class='success'>Deleted.</p>" );
			return false;
			
		} else if( $action == DBS_FormBase::ACTION_NONE ) {
			return true;
			
		} else {
			assert( "Invalid action to actionSuccess: $action" );
		}
	}
}

class DBS_FormConvertException extends DBS_Exception {
	const INVALID_INPUT_STRING = 1;
	
	static private $codeToMsg = array(
		self::INVALID_INPUT_STRING => 'The input format is invalid.',
		);
	public function __construct( $code ) {
		parent::__construct( self::$codeToMsg[$code], $code );
	}
}

function _dbs_formin_Integer( $value ) { return $value === null ? '' : '' . $value; }
function _dbs_formin_String( $value ) {	return $value === null ? '' : $value; }
function _dbs_formin_Text( $value ) {	return $value === null ? '' : $value; }
function _dbs_formin_Decimal( $value ) { return $value === null ? '' : '' . $value; }
function _dbs_formin_Float( $value ) { return $value === null ? '' : '' . $value; }
function _dbs_formin_Bool( $value ) {	return $value === null ? '' : $value ? '1' : '0'; }
function _dbs_formin_DateTime( $value ) {	return $value === null ? '' : $value->getDate( DATE_FORMAT_ISO ); }
function _dbs_formin_Date( $value ) { return $value === null ? '' : $value->format( '%Y-%m-%d' ); }
function _dbs_formin_Time( $value ) {	return $value === null ? '' : _dbs_encode_time($value ); }

function _dbs_formout_Integer( $value ) { 
	if( $value === null || $value === "" )
		return null;
		
	if( !is_numeric( $value ) )
		throw new DBS_FormConvertException( DBS_FormConvertException::INVALID_INPUT_STRING );
		
	//ensure no extra nonsense is used... (truly an integer)
	if( intval( $value ) != floatval( $value ) )
		throw new DBS_FormConvertException( DBS_FormConvertException::INVALID_INPUT_STRING );
		
	return intval( $value ); 
}

function _dbs_formout_String( $value ) {	
	return $value; 
}

function _dbs_formout_Text( $value ) {	
	return $value; 
}

function _dbs_formout_Decimal( $value ) { 
	if( $value === null || $value === "" )
		return null;
		
	if( !is_numeric( $value ) )
		throw new DBS_FormConvertException( DBS_FormConvertException::INVALID_INPUT_STRING );
		
	return floatval( $value ); 
}

function _dbs_formout_Float( $value ) { 
	if( $value === null || $value === "" )
		return null;
		
	if( !is_numeric( $value ) )
		throw new DBS_FormConvertException( DBS_FormConvertException::INVALID_INPUT_STRING );
	
	return floatval( $value ); 
}

function _dbs_formout_Bool( $value ) {	
	if( $value === null || $value === "" )
		return null;
		
	if( $value === '1' )
		return true;
	else if( $value === '0' )
		return false;
	else
		throw new DBS_FormConvertException( DBS_FormConvertException::INVALID_INPUT_STRING );
}

function _dbs_formout_DateTime( $value ) { 
	if( $value === '' )
		return null;
	//http://pear.php.net/bugs/bug.php?id=15631 (check format first, setDate doesn't indicate failure)
	if( !preg_match('/^(\d{4})-?(\d{2})-?(\d{2})([T\s]?(\d{2}):?(\d{2}):?(\d{2})(\.\d+)?(Z|[\+\-]\d{2}:?\d{2})?)?$/i', $value ) )
		throw new DBS_FormConvertException( DBS_FormConvertException::INVALID_INPUT_STRING );
	
	$ret = new Date();
	$ret->setDate( $value ); //default accepts a lot of formats
	return $ret;
}
function _dbs_formout_Date( $value ) { 
	$ret = _dbs_formout_DateTime( $value ); 
	//TODO: requires Date >= 1.5 (still alpha release)
	//if( $ret !== null )
	//	$ret->trunc( DATE_PRECISION_DAY );
	return $ret;
}
function _dbs_formout_Time( $value ) { 
	if( $value === '' )
		return null;
		
	$ret = _dbs_decode_time( $value ); 
	if( $ret === null )
		throw new DBS_FormConvertException( DBS_FormConvertException::INVALID_INPUT_STRING );
	return $ret;
}

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
 */
function dbs_standard_form( $form, $entitykey ) {
	if( !$form->hasAction() ) {
		$key = _pers_array_get_default( $entitykey, $_REQUEST, null );	//TODO: unlike the get_request_def this doesn't handle encoding correctly!!!
		$entityname = $form->ENTITY;
		//for PHP 5.3 (and can also replace call_user_func)
		//$entityname = $formclass::ENTITY
		if( $key !== null ) 
			$rule = call_user_func( "$entityname::findWith$entitykey", $key );
		else
			$rule = null;
			
		$form->initCreate( $rule );
	} else {
		$form->initFromRequest( );
	}
	return $form;
}

?>
