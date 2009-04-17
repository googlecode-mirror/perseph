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
			"Entity": Type( "Entity" ),
			}
		self.defaults = {}
		self.providers = {}
		self.entities = {}
		self.mappers = {}
		self.listings = {}
		self.searches = {}
		
		
class Provider:
	def __init__(self):
		self.tables = {}#Name:Provider_Table
		self.impl = None	#Provider_Impl
		self.dbType = 'generic'	# The type of the DB in the backend

class Provider_Impl:
	def __init__(self):
		self.varName = None #variable name in PHP which is this source
		self.tablePrefixVar = None	#prefix variable for all tables
		self.funcName = None;	#funcion in PHP which obtains the DBSource
		
class Provider_DBSource(Provider_Impl):
	def __init__(self):
		Provider_Impl.__init__( self )
		
class Provider_MDB2(Provider_Impl):
	def __init__(self):
		Provider_Impl.__init__( self )
		self.textType = 'text'	#which MDB2 type (or custom type) to use for text/string fields
		
		
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

# The Entity_Field instance may be used more than use if merges are being used
class Entity_Field:
	
	def __init__(self, name, fieldType ):
		self.name = name
		self.fieldType = fieldType
		self.keyType = KEY_TYPE_NONE
		self.hasDefault = False #<Boolean>
		self.defaultValue = None
		self.maxLen = None #Null<Integer>if non-null indicates the maximum logical length to the entity
		self.allowNull = False #<Boolean> does the field allow a null assignment
		self.label = None #<String> logical label of the field, defaults to name
		self.desc = None #<String> description, no default
	
class Entity(Type):
	def __init__(self,name):
		Type.__init__(self,name)
		self.className = None #Null<String> if not null specifies the instance classname to use instead of "name"
		self.titleField = None	#<Entity_Field> logical title of the entity
		self.aliases = {}#AliasString:InternalString
		self.fields = {}	#String: Entity_Field
		self.identifierField = None	#<Entity_Field> the unique identifier of the item, if one exists
			
	def getRootType(self):
		return Type("Entity")
	
	def baseType(self):
		return False
	
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
	# We decide ordering of key names here, and we use alphabetic for now (this
	# applies to the component keys of RECORD_KEY type)
	def getKeySet( self ):
		ret = []
		comp = []
		for field in self.fields.itervalues():
			if field.keyType == KEY_TYPE_RECORD:
				comp.append( field )
			elif field.keyType == KEY_TYPE_ALT:
				ret.append( [ field ] )
			
		if len(comp) > 0:
			comp.sort(key=lambda x:x.name)
			ret.append( comp )
			
		return ret
	
	##
	# returns None or
	#		the key field if the entity has only a single defining key
	# NOTE: A return on non-None here also implies that identifierField
	# is set (not during processing of course, but by the time of output
	# generation)
	def getSingleKey( self ):
		set = self.getRecordKeyFields()
		if len( set ) != 1:
			return None
		return set[0]
	
	##
	# Obtains the field marked as title in this entity
	# @return [out] title field, or None
	def getTitle( self ):
		return self.titleField


class Entity_Normal(Entity):
	def __init__(self,name):
		Entity.__init__(self,name)
		self.searches = {} #Name: Search
	
	
class Entity_Merge(Entity):
	def __init__(self,name):
		Entity.__init__(self,name)
		self.merges = {}	# Name: Entity_Normal
		self.links = []	# Array<Entity_Merge_Link> list of grouped items
		self.keyMerges = {} # <Name: Entity_Normal> merges which serve as entry points
		
	def linksWithEntity( self, entity ):
		ret = []
		for linkSet in self.links:
			for link in linkSet:
				if link.entity == entity:
					ret.append( ( linkSet, link ) ) # return set and the matching link
					break
		return ret
	
class Entity_Merge_Link:
	def __init__(self):
		self.entity = None	# <Entity>
		self.field = None	# <Entity_Field>
		
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

		self.ent_const = None	 #<Value> constant value to populate into DB field
		
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
	def __init__(self, container ):
		self.name = None;
		self.sort = None	# <Search_Sort>
		self.filter = None	# <Search_FilterExpr>
		self.limit = None	# <Search_None>
		self.entity = None	# <Entity> which is produced by the search
		self.container = container # <Entity> may be null (in which this search resides)
		self.static = True # <Bool> Has no references to enclosing container entity
		
		self.placeholderCount = 0	# Total count of placeholders
		
class Search_FilterExpr:
	def __init__(self):
		pass
	
class Search_FilterField(Search_FilterExpr):
	def __init__(self):
		self.field = None	# <Entity_Field> the field to be matched
		
		self.const = None	# If a constant, then the string form of it here
		self.placeholder = None	# An integer (the paramter position) of a placeholder is used (not a constant)
		self.containerRef = None # <Entity_Field> of container, or <Entity> for the entity itself

class Search_FilterFieldOp(Search_FilterField):
	def __init__(self):
		Search_FilterField.__init__(self)
		self.op = None	# String form of OP

class Search_FilterFieldPattern(Search_FilterField):
	def __init__(self):
		Search_FilterField.__init__(self)

class Search_FilterGroupOp(Search_FilterExpr):
	def __init__(self):
			Search_FilterExpr.__init__(self)
			self.exprs = []	#Array<Search_FilterExpr> at least 2 in length
			self.op = None	#String, OR or AND
			
class Search_Sort:
	def __init__(self):
		self.dir = None	#<String> one of ASC or DESC
		self.fields = [] #list<Entity_Field> of columns to sort by (in order of precedence)
