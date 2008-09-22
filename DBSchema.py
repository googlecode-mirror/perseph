# ***** BEGIN LICENSE BLOCK *****
# Version: GPL 3.0
# This file is part of Persephone.
#
# Persephone is free software: you can redistribute it and/or modify it under the 
# terms of the GNU General Public License as published by the Free Software
# Foundation, version 3 of the License.
#
# Persephone is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Persephone.  If not, see <http://www.gnu.org/licenses/>.
# 
# Contributors:
#		edA-qa mort-ora-y <edA-qa@disemia.com>
# ***** END LICENSE BLOCK *****

class Type:
	def __init__(self, name):
		self.name = name	#<String>
		
	def getRootType(self):
		return self
	
	def baseType(self):
		return True
		
class CustomType( Type ):
	
	def __init__( self, name, base ):
		Type.__init__( self, name )
		self.base = base	#//<DBSchema_Type>
	
	def getRootType( self ):
		return self.base
	
	def baseType( self ):
		return False

# A collection type is like in Java, or a standard collection in C++, it has
# an outer type (the primary type) and an inner type (what is being collected)
class CollectionType( Type ):
	def __init__(self,name,of):
		Type.__init__( self, name )
		self.of = of	#<DBSchema_Type> what it contains
		
		
# Root for an in memory Schema
class Root:
	def __init__(self):
		self.types = {
			"String": Type( "String" ),
			"Integer": Type( "Integer" ),
			"DateTime": Type( "DateTime" ),
			"Date": Type( "Date" ),
			"Time": Type( "Time" ),
			"Decimal": Type( "Decimal" ),
			"Float": Type( "Float" ),
			"Bool": Type( "Bool" ),
			"Text": Type( "Text" ),
			"Object": Type( "Object" ),
			}
		self.defaults = {}
		self.providers = {}
		self.entities = {}
		self.mappers = {}
		self.forms = {}
		self.listings = {}
		self.searches = {}
		
		
class Provider:
	def __init__(self):
		self.tables = {}#Name:Provider_Table

class Provider_DBSource (Provider):
	def __init__(self):
		Provider.__init__( self )
		self.varName = None #variable name in PHP which is this source
		self.tablePrefixVar = None	#prefix variable for all tables
		self.funcName = None;	#funcion in PHP which obtains the DBSource
		
		
class Provider_Table:
	def __init__( self, name ):
		self.name = name
		self.fields = {} #name:DBScheam_Provider_Field
		
class Provider_Field:
	def __init__( self, name, fieldType ):
		self.name = name
		self.fieldType = fieldType #<String> DB layer type
		self.lastInsert = False #<Boolean> this field is "available" after an insert
		
		
KEY_TYPE_NONE = 0
KEY_TYPE_RECORD = 1
KEY_TYPE_ALT = 2		

class Entity_Field:
	
	def __init__(self, name, fieldType ):
		self.name = name
		self.fieldType = fieldType
		self.keyType = KEY_TYPE_NONE
		self.hasDefault = False #<Boolean>
		self.defaultValue = None
		self.title = False #<String> the logical title of the entity
		self.maxLen = None #Null<Integer>if non-null indicates the maximum logical length to the entity
		self.allowNull = False #<Boolean> does the field allow a null assignment
		self.label = None #<String> logical label of the field, defaults to name
		self.desc = None #<String> description, no default
	
class Entity(Type):
	def __init__(self,name):
		Type.__init__(self,name)
		self.fields = {}	#String: Entity_Field
		self.aliases = {}#AliasString:InternalString
		self.className = None #Null<String> if not null specifies the instance classname to use instead of "name"
	
	##
	# Obtains the sets of keys which can identify this record for loading/saving
	def getRecordKeyFields( self ):
		ret = []
		for field in self.fields.itervalues():
			if field.keyType != KEY_TYPE_NONE:
				ret.append( field )
		return ret
	
	##
	# Obtains a set of all keys/composites which can identify the identity.
	def getKeySet( self ):
		ret = []
		comp = []
		for field in self.fields.itervalues():
			if field.keyType == KEY_TYPE_RECORD:
				comp.append( field )
			elif field.keyType == KEY_TYPE_ALT:
				ret.append( [ field ] )
			
		if len(comp) > 0:
			ret.append( comp )
			
		return ret
	
	##
	# Obtains the field marked as title in this entity
	# @return [out] title field, or None
	def getTitle( self ):
		for field in self.fields.itervalues():
			if field.title:
				return field
		return None
	
	
class Mapper:
	def __init__( self, provider ):
		self.provider = provider
		self.entity = None
	
		self.table = ""	#Will need to support multiple tables, this is just to get back to where we were before
		self.fields = [] #<Mapper_Field>

	def getDBFieldForEntityField( self, ef ):
		for locfield in self.fields:
			if locfield.ent_field.name == ef.name:
				return locfield
		raise Exception, "No DBField for the entity %s" % ef.name

PERSIST_TYPE_NONE = 0
PERSIST_TYPE_LOAD = 0x1
PERSIST_TYPE_SAVE = 0x2
PERSIST_TYPE_LOADSAVE = PERSIST_TYPE_LOAD | PERSIST_TYPE_SAVE

class Mapper_Field:
	def __init__(self):
		self.db_convert = None #<Function>
		self.db_field = None #<Provider_Field>
		self.db_table = None #<Provider_Table> (Not yet supported)
	
		self.ent_convert = None #<Function>
		self.ent_field = None #<DBSchema_Entity_Field>
		self.ent_field_field = None #<DBSchema_Entity_Field> name of field in the entity field, may be null (no sub-field in use)

		self.persist = PERSIST_TYPE_LOADSAVE #<Boolean> how this field is persisted in backing stores
	
	def isPersistSave( self ):
		return self.persist & PERSIST_TYPE_SAVE == PERSIST_TYPE_SAVE
	
	def isPersistLoad( self ):
		return self.persist & PERSIST_TYPE_LOAD == PERSIST_TYPE_LOAD
	
	def isLoadOnly( self ):
		return self.persist == PERSIST_TYPE_LOAD;

class Function:
	def __init__(self):
		self.name = None	#<String>
		self.returnType = None #<Type>


class Form:
	
	def __init__(self,name):
		self.name = name #//<String>
		self.entity = None #	//<DBSchema_Entity>
		self.allowDelete = False #	//<Bool>
		self.fields = [] # //list<DBSchema_Form_Field>


class Form_Field:
	
	def __init__(self, field ):
		self.name = field.name
		self.hidden = False
		self.readonly = False
		self.label = field.label #<String>
	

class Listing:
	
	def __init__(self, name ):
		self.name = name	#	//<String>
		self.entity = None #	//<DBSchema_Entity>
		self.fields = [] #	//Array<DBSchema_Listing_Field>


class Listing_Field:
	
	def __init__(self ):
		self.entField = None # //<DBSchema_Entity_Field> or null for the entity itself
		self.label = "" #	//<String> 
		self.convertFunc = None #	//<FunctionName>


class Search:
	def __init__(self, name, entity ):
		self.name = name;
		self.sort = None	# <Search_Sort>
		self.filter = None	# <Search_FilterExpr>
		self.limit = None	# <Search_None>
		self.entity = entity	# <Entity>
		
class Search_FilterExpr:
	def __init__(self):
		pass
	
	def countPlaceholders( self ):
		return 0
	
class Search_FilterField(Search_FilterExpr):
	def __init__(self):
		self.field = None	# <Entity_Field>
		self.const = None	# If a constant, then the string form of it here
		self.placeholder = False	# True if a placeholder is used (not a constant)
	
	def countPlaceholders( self ):
		return 1 if self.placeholder else 0

class Search_FilterFieldOp(Search_FilterField):
	def __init__(self):
		Search_FilterField.__init__(self)
		self.op = None	# String form of OP

class Search_FilterFieldPattern(Search_FilterField):
	def __init__(self):
		Search_FilterField.__init__(self)
