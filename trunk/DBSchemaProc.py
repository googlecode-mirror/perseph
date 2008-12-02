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
import SchemaLexer as SL
import SchemaParser as SP

import DBSchema

##
# Processes the parsed input into a DBSchema and related structures
class Processor:
	def __init__(self):
		self.rawDecls = { SL.ENTITY: [],
			SL.DEFAULT: [],
			SL.MAPPER: [],
			SL.PROVIDER: [],
			SL.CUSTOMTYPE: [],
			SL.LISTING: [],
			SL.SEARCH: [],
			}
			
		self.sc = DBSchema.Root()
	
	def collect( self, root ):
		for i in range( root.getChildCount() ):
			ch = root.getChild( i )
			self.rawDecls[ch.getToken().type].append( ch )
			
	def process( self ):
		self.processDefaults( )
		self.processTypes( )
		self.processProviders( )
		self.processEntities( )
		self.processEntitiesPass2( )
		self.processMappers( )
		self.processListings( )
		self.processSearches( )
		
	def processDefaults( self ):
		for df in self.rawDecls[SL.DEFAULT]:
			self.sc.defaults[df.getChild(0).text] = df.getChild(1).text
			
	def processTypes( self ):
		for ty in self.rawDecls[SL.CUSTOMTYPE]:
			name = extProp( ty, SL.NAME )
			varset = extVarSet( ty )
			checkVarSet( ty, varset, [],[] )
			base = self.getType( ty )
			
			self.sc.types[name] = DBSchema.CustomType( name, base )
		
		#we also need to treat entities as types (they're incomplete definitions now)
		for enNode in self.rawDecls[SL.ENTITY]:
			name = extProp( enNode, SL.NAME )
			if extPropOpt( enNode, SL.MERGE ) == None:
				self.sc.types[name] = DBSchema.Entity_Normal(name)
			else:
				self.sc.types[name] = DBSchema.Entity_Merge(name)
		
	# Providers support the special combination ability such that part of the provider
	# can be specified as incomplete, and later completed.
	def processProviders( self ):
		for prov in self.rawDecls[SL.PROVIDER]:
			name = extProp( prov, SL.NAME )
			varset = extVarSet( prov )
			provider = None
			
			defn = varset['definition'] if 'definition' in varset else 'full'
			if defn == 'full' or defn == 'incomplete':
				if name in self.sc.providers:
					errorOn( prov, "A provider definition already exists: %s" % name )
				provider = DBSchema.Provider()
				self.sc.providers[name] = provider
			elif defn == 'extend':
				if not name in self.sc.providers:
					errorOn( prov, "Provider extends does not exist: %s" % name )
				provider = self.sc.providers[name]
			else:
				errorOn( prov, "Unknown definition type: %s" % defn )
							
			if defn != 'incomplete':
				type = varset["type"]
				impl = None
				if type == "DBSource" or type == 'MDB2':
					if type == 'MDB2':
						impl = DBSchema.Provider_MDB2( )
						checkVarSet( prov, varset, ["type"], ["var","func","tablePrefixVar","textType","definition"] )
						if 'textType' in varset:
							impl.textType = varset['textType']
					else:
						impl = DBSchema.Provider_DBSource( )
						checkVarSet( prov, varset, ["type"], ["var","func","tablePrefixVar","definition"] )
					provider.impl = impl
						
					
					# May use a variable or a function to lookup/return the DB
					if 'var' in varset:
						impl.varName = varset['var']
					else:
						impl.funcName = varset['func']
					
				else:
					errorOn( prov, "Unknown type in provider: %s" % name )
			
				if "tablePrefixVar" in varset:
					provider.impl.tablePrefixVar = varset['tablePrefixVar'];
				
			tableNodes = extTableNodes( prov )
			for tableNode in tableNodes:
				tableName = extProp( tableNode, SL.NAME )
				table = DBSchema.Provider_Table( tableName )
				provider.tables[tableName] = table
				
				for fieldSpec in extNodes( tableNode, SL.FIELD ):
					fieldType = self.getType( fieldSpec )
					fieldName = extProp( fieldSpec, SL.NAME )
					
					field = DBSchema.Provider_Field( fieldName, fieldType )
					table.fields[fieldName] = field
					
					for opt in extOptions( fieldSpec ):
						if opt[0] == 'LAST_INSERT_ID':
							field.lastInsert = True
						else:
							errorOn( fieldSpec, "Unknown option: %s" % opt[0] )
				
			
	##
	# 
	def getType( self, node, allowCol = True ):
		col = extNodeOpt( node, SL.COLTYPE )
		if col == None:
			name = extNode( node, SL.TYPE ).getChild(0).text
			if not name in self.sc.types:
				errorOn( node, "Unrecognized type: %s" % name )
			return self.sc.types[name]
			
		# handle the collection
		if not allowCol:
			errorOn( node, "Collection type not allowed, possibly it is already a collection" )
			
		name = col.getChild(0).text
		if name != 'Array': #TODO: remove harcoding of collection types
			errorOn( col, "Unrecognized collection: %s" % name )
			
		sub = self.getType( col, False )
		return DBSchema.CollectionType( name, sub )
		
	##
	# 
	def processEntities( self ):
		for ent in self.rawDecls[SL.ENTITY]:
			name = extProp( ent, SL.NAME )
			# previously created in processTypes
			entity = self.sc.types[ name ]
			
			varset = extVarSet( ent )
			checkVarSet( ent, varset, [], ['class']	)
			
			if 'class' in varset:
				entity.className = varset['class']
			
			# Fields -------------------------------------------------------------
			fields = extFields( ent )
			for fieldSpec in fields:
				if isinstance( entity, DBSchema.Entity_Merge ):
					errorOn( fieldSpec, "merge entity cannot contain fields" )
					
				fieldType = self.getType( fieldSpec )
				fieldName = extProp( fieldSpec, SL.NAME )
				opts = extOptions( fieldSpec )
				
				field = DBSchema.Entity_Field( fieldName, fieldType )
				for opt in opts:
					if opt[0] == 'RECORD_KEY':
						field.keyType = DBSchema.KEY_TYPE_RECORD
					elif opt[0] == 'ALT_RECORD_KEY':
						field.keyType = DBSchema.KEY_TYPE_ALT
					elif opt[0] == 'DEFAULT':
						field.hasDefault = True
						field.defaultValue = opt[1]
						#TODO: only handle NULL if a raw string, not quoted
						if field.defaultValue == 'NULL':
							field.defaultValue = None
					elif opt[0] == 'TITLE':
						if entity.titleField != None:
							errorOn( fieldSpec, "entity has duplicate TITLE" )
						entity.titleField = field
					elif opt[0] == 'MAXLEN':
						field.maxLen = int( opt[1] )
					elif opt[0] == 'ALLOW_NULL':
						field.allowNull = True;
					elif opt[0] == 'LABEL':
						field.label = opt[1]
					elif opt[0] == 'DESC':
						field.desc = opt[1]
					elif opt[0] == 'IDENTIFIER':
						if entity.identifierField != None:
							errorOn( fieldSpce, "entity has duplicate IDENTIFIER, only one supported" )
						entity.identifierField = field
					else:
						errorOn( fieldSpec, "unrecognized option: %s " % opt )
					
				# Default label to the field name
				if field.label == None:
					field.label = field.name
				
				entity.fields[fieldName] = field
			
			# Auto Identifier field ---------------------------------------------
			# This is *NOT* guaranteed, if the user needs a guaranteed Identifier they should use IDENTIFIER!
			if isinstance( entity, DBSchema.Entity_Normal ) and entity.identifierField == None:
				entity.identifierField = entity.getSingleKey()	# will be None if none, so okay to assign like this
				
			# Aliases -----------------------------------------------------------
			aliases = extAliases( ent )
			for alias in aliases:
				if isinstance( entity, DBSchema.Entity_Merge ):
					errorOn( ent, "merge entity cannot contain aliases" )
					
				nameA, nameB = alias
				fieldA = nameA in entity.fields
				fieldB = nameB in entity.fields
				if fieldA == fieldB:
					errorOn( ent, "%s, %s, one must be field, one not" % (nameA, nameB ) )
					
				if fieldA:
					entity.aliases[nameB] = nameA
				else:
					entity.aliases[nameA] = nameB
					
			# Finalize -----------------------------------------------------------
			self.sc.entities[name] = entity
			
 	##
	# We do a second pass since the searches need to refer to other entities, and they won't be
	# fully defined in the first pass
	def processEntitiesPass2( self ):
		for ent in self.rawDecls[SL.ENTITY]:
			entity = self.sc.entities[extProp( ent, SL.NAME )]
		
			# Searches --------------------------------------------------------
			for searchNode in extSearches( ent ):
				if isinstance( entity, DBSchema.Entity_Merge ):
					errorOn( searchNode, "merge entity cannot contain searches" )
					
				search = DBSchema.Search( entity )
				self.extractSearch( search, searchNode )
				entity.searches[search.name] = search
				
			# Merge ------------------------------------------------------------
			merges = extMerges( ent )
			for merge in merges:
				if isinstance( entity, DBSchema.Entity_Normal ):
					errorOn( merge, "normal entity cannot contain merges" )
					
				toMergeName = extProp( merge, SL.NAME )
				opts = extOptions( merge )
				
				if not toMergeName in self.sc.entities:
					errorOn( merge, "merge entity %s not defined" % toMergeName )
				toMerge = self.sc.entities[toMergeName]
				if not isinstance( toMerge, DBSchema.Entity_Normal ):
					errorOn( merge, "merge entity %s must be a normal entity" % toMergeName )
					
			# Link ---------------------------------------------------------------
			links = extLinks( ent )
			for link in links:
				if isinstance( entity, DBSchema.Entity_Normal ):
					errorOn( merge, "normal entity cannot contain merges" )
					
				op = link.getChild(0)
				if op.type != SL.MAPTORIGHTOP:
					errorOn( op, "unexpect op type" )
					
				fieldFrom = op.getChild(0)
				fieldTo = op.getChild(1)
				
				eml = DBSchema.Entity_Merge_Link()
				eml.fromEnt = self.getEntity( fieldFrom, fieldFrom.getChild(0).text )
				eml.fromField = self.getEntityField( fieldFrom, eml.fromEnt, fieldFrom.getChild(1).text )
				
				eml.toEnt = self.getEntity( fieldTo, fieldTo.getChild(0).text )
				eml.toField = self.getEntityField( fieldTo, eml.toEnt, fieldTo.getChild(1).text )
				
				# TODO: sort and do root->lead ordering here!
				
				entity.links.append( eml )
				
				
	def getEntity( self, refNode, name ):
		if not name in self.sc.entities:
			errorOn( refNode, "reference to undefined entity %s" % name )
		return self.sc.entities[name]
		
	def getEntityField( self, refNode, entity, field ):
		if not field in entity.fields:
			errorOn( refNode, "reference to undefined field %s::%s" % (entity.name, field ) )
		return entity.fields[field]
			
	def processMappers( self ):
		for mapperNode in self.rawDecls[SL.MAPPER]:
			name = extProp( mapperNode, SL.NAME )
			varset = extVarSet( mapperNode )
			checkVarSet( mapperNode, varset, ['provider' ], [] )
			
			if not varset['provider'] in self.sc.providers:
				errorOn( mapperNode, "invalid provider %s" % varset['provider'] )
				
			mapper = DBSchema.Mapper( self.sc.providers[varset['provider']] )
			mapper.entity = self.getEntity( mapperNode, name )
			self.sc.mappers[name] = mapper
			
			fieldsNode = extNode( mapperNode, SL.FIELDS )
			for i in range( fieldsNode.getChildCount() ):
				node = fieldsNode.getChild(i)
				if node.type == SL.USING:
					using = node.getChild(0).text
					#temporary table set until we support multiple tables
					if mapper.table != "":
						errorOn( node, "Duplicate table spec, multi-tables not supported" )
					if not using in mapper.provider.tables:
						errorOn( node, "Table does not exist in provider: %s" % using )
						
					mapper.table = mapper.provider.tables[using];
					
					for j in range(1,node.getChildCount() ):
						expr = node.getChild(j)
						mapField = DBSchema.Mapper_Field()
						mapper.fields.append( mapField )
						
						if expr.type == SL.MAPOPEXPR:
							op = expr.getChild(0)
							left = self.getMapperFieldExpr( expr.getChild(1) )
							right = self.getMapperFieldExpr( expr.getChild(2) )
							if left['db'] == right['db']:
								errorOn( expr, "requires one database and one entity field" )
								
							( db, ent ) = ( left, right ) if left['db'] else ( right, left )
							if ent['func'] != None:
								mapField.ent_convert = ent['func'];	
							elif db['func'] != None:
								mapField.db_convert = db['func']
								
							#TODO: check that fields exist
							mapField.db_field = mapper.table.fields[db['name']]
							mapField.ent_field = mapper.entity.fields[ent['name']]
							
							if ent['subfield'] != None:
								mapField.ent_field_field = mapField.ent_field.fieldType.fields[ent['subfield']]
							
							# handle non-bi-directional persistence
							if op.type != SL.MAPEQUALOP:
								if op.type == SL.MAPTORIGHTOP:
									isToEnt = left['db']
								elif op.type == SL.MAPTOLEFTOP:
									isToEnt = right['db']
								else:
									errorOn( op, "Unrecognized operator %s" % SP.tokenNames[ op.type ] )
									
								if isToEnt:
									mapField.persist = DBSchema.PERSIST_TYPE_LOAD
								else:
									mapField.persist = DBSchema.PERSIST_TYPE_SAVE
							
						else:
							errorOn( expr, "Unsupported expression " + expr )
							
				else:
					errorOn( node, "Expecting only using now" )
	
	# NOTE: supports only a single function parameter now
	def getMapperFieldExpr( self, node ):
		res = {}
		res['subfield'] = None
		res['func'] = None
		
		if node.type == SL.FUNCTION:
			func = DBSchema.Function()
			func.name = node.getChild(0).text 
			func.returnType = self.getType( node )
			res['func'] = func
			node = node.getChild(2)
			
		if node.type == SL.DBFIELDNAME:
			res['db'] = True
			res['name'] = node.getChild(0).text
			return res
		
		if node.type == SL.ENTSUBFIELD:
			res['db'] = False
			res['name'] = node.getChild(0).text
			res['subfield'] = node.getChild(1).text
			return res
			
		if node.type != SL.ENTFIELDNAME:
			errorOn( node, "expecting an entity field, perhaps only db fields specified" )
			
		res['db'] = False
		res['name'] = node.getChild(0).text
		return res
		
			
	def processListings( self ):
		for listNode in self.rawDecls[SL.LISTING]:
			name = extProp( listNode, SL.NAME )
			varset = extVarSet( listNode )
			checkVarSet( listNode, varset, ['entity'], [] )
			
			listing = DBSchema.Listing( name )
			self.sc.listings[name] = listing
			
			#TODO: duplicate code from processForm
			if not varset['entity'] in self.sc.entities:
				errorOn( listNode, "refers to non-extant entity: %s" % varset['entity'] )
			listing.entity = self.sc.entities[varset['entity']]
			
			# collect fields to display
			fieldsNode = extNode( listNode, SL.FIELDS )
			for i in range( fieldsNode.getChildCount() ):
				node = fieldsNode.getChild(i)
				label = extPropOpt( node, SL.LABEL )
				
				field = DBSchema.Listing_Field()
				listing.fields.append( field )
				field.label = label
				
				# Support only a single parameter for now
				funcNode = extNodeOpt( node, SL.FUNCTION )
				if funcNode != None:
					field.convertFunc = funcNode.getChild(0).text	
					refNode = extNodeOpt( funcNode, SL.REF )
					if refNode != None:
						entfield = '@' + refNode.getChild(0).text
					else:
						entfield = extProp( funcNode, SL.NAME )
				else:
					entfield = extProp( node, SL.NAME )
				
				# Set the field used
				if  entfield == '@SELF':
					field.entField = None
				else:
					if not entfield in listing.entity.fields:
						errorOn( node, "refers to non-entity field %s" % entfield )
					field.entField = listing.entity.fields[entfield]
				
				# Assign a default label
				if field.label == None:
					field.label = field.entField.label
			
			
	def processSearches( self ):
		for searchNode in self.rawDecls[SL.SEARCH]:
			search = DBSchema.Search( None )
			self.extractSearch( search, searchNode )
			self.sc.searches[search.name] = search
			
	def extractSearch( self, search, searchNode ):
		search.name = extProp( searchNode, SL.NAME )
		search.entity = self.getType( searchNode )
		
		filterNode = extNodeOpt( searchNode, SL.FILTER )
		if filterNode != None:
			search.filter = self.extractSearchFilter( search, filterNode.getChild(0) )
			
		sortNode = extNodeOpt( searchNode, SL.SORT )
		if sortNode != None:	
			search.sort = self.extractSearchSort( search, sortNode )
		
	def extractSearchSort( self, search, node ):
		sort = DBSchema.Search_Sort()
		
		# extract direction
		dir = node.getChild(0).text
		if dir == 'ASC':
			sort.dir = 'ASC'
		elif dir == 'DESC':
			sort.dir = 'DESC'
		else:
			errorOn( node, "Unrecognized sort ordering %s" % dir )
			
		# extract fields
		for i in range( 1, node.getChildCount() ):
			col = node.getChild(i)
			if not col.text in search.entity.fields:
				errorOn( col, "No such field in entity, %s" % col.text )
				
			sort.fields.append( search.entity.fields[col.text] )
		
		return sort
		
	opMap = {
		SL.OPEQUALS: '=',
		SL.OPLESSTHAN: '<',
		SL.OPGREATERTHAN: '>',
		SL.AND: 'AND',
		SL.OR: 'OR',
		};
	def extractSearchFilter( self, search, node ):
		
		if node.type in ( SL.OR, SL.AND ):
			expr = DBSchema.Search_FilterGroupOp()
			expr.op = self.opMap[node.type]
				
			# NOTE: the left-right ordering must be maintained (in grammar also) to ensure correct
			# placehold counting
			for i in range( 0, node.getChildCount() ):
				sub = self.extractSearchFilter( search, node.getChild(i) )
				expr.exprs.append( sub )
			return expr
		
		if node.type in ( SL.OPEQUALS, SL.OPLESSTHAN, SL.OPGREATERTHAN ):
			expr = DBSchema.Search_FilterFieldOp()
			expr.op = self.opMap[node.type]
			
		if node.type == SL.OPPATTERNMATCH:
			expr = DBSchema.Search_FilterFieldPattern()
			
		if node.type in ( SL.OPEQUALS, SL.OPLESSTHAN, SL.OPGREATERTHAN, SL.OPPATTERNMATCH ):
			left = node.getChild(0)
			if not left.text in search.entity.fields:
				errorOn( left, "No such field in entity, %s" % left.text )
			expr.field = search.entity.fields[left.text]
				
			right = node.getChild(1)
			if right.type == SL.PLACEHOLDER:
				expr.placeholder = search.placeholderCount
				search.placeholderCount += 1
			elif right.type == SL.REF:
				fname = right.getChild(0).text
				if search.container == None:
					errorOn( right, "Cannot refer to container field when not in a container (Entity)" )
					
				if fname == 'SELF':
					expr.containerRef = search.container
				else:
					if not fname in search.container.fields:
						errorOn( right, "No such field in container entity, %s" % fname )
					expr.containerRef = search.container.fields[fname]
			else:
				expr.const = right.text
			return expr
			
		errorOn( node, "Unrecognized search expression" )
	
####################################
# Extractor utilities
def errorOn( node, msg ):
	loc = "%d:%d:" %  (node.getLine(), node.getCharPositionInLine())
	raise Exception, loc + msg

##
# Checks for the correctness of the variables in a variable set
# @param node [in] reference for errors
# @param varset [in] which variable set to check
# @param req [in] list of required items
# @param opt [in] list of optional items
def checkVarSet( node, varset, req, opt ):
	for r in req:
		if not r in varset:
			errorOn( node, "Missing required variable: %s" % (r) )
	
	for k in varset.iterkeys():
		if not ( k in req or k in opt ):
			errorOn( node, "Extraneous variable: %s" % (k) )

##
# Obtains the node with the given token, or None if not found.
# A duplicate note will raise an exception
def extNodeOpt( node, token ):
	found = None
	for i in range( node.getChildCount() ):
		ch = node.getChild( i )
		if ch.type == token :
			if found != None:
				errorOn( ch, "Duplicate definition " + token )
			found = ch
	return found
	
##
# Obtains the node with the given token. Checks that only a single
# node of this type exists
def extNode( node, token ):
	found = extNodeOpt( node, token )
	if found == None:
		errorOn( node, "Missing definition " + SP.tokenNames[token] )
	return found

## 
# Obtains the TOKEN based property from the tree.
def extProp( node, token ):
	return extNode( node, token ).getChild(0).text

def extPropOpt( node, token ):
	ret = extNodeOpt( node, token )
	if ret == None:
		return ret
	return ret.getChild(0).text

def extNodes( node, token ):
	ret = []
	if node == None:
		return ret
	for i in range( node.getChildCount() ):
		if node.getChild(i).type == token:
			ret.append( node.getChild( i ) )
	return ret
	
def extTableNodes( node ):
	return extNodes( node, SL.TABLE )
	
def extFields( node ):
	return extNodes( extNodeOpt( node, SL.FIELDS ), SL.FIELD )

def extMerges( node ):
	return extNodes( extNodeOpt( node, SL.MERGE ), SL.FIELD )
	
def extSearches( node ):
	return extNodes( node, SL.SEARCH )

def extLinks( node ):
	return extNodes( node, SL.LINK )

def extAliases( node ):
	aliases = extNodeOpt( node, SL.ALIASES )
	all = []
	if( aliases != None ):
		for alias in extNodes( aliases, SL.ALIAS ):
			all.append( [alias.getChild(0).text,alias.getChild(1).text] )
	return all
			
def extOptions( node ):
	ret = []
	for i in range( node.getChildCount() ):
		ch = node.getChild( i )
		if ch.getType() != SL.OPTION:
			continue
		values = []
		for j in range( ch.getChildCount() ):
			values.append( ch.getChild(j).text )
		ret.append( values )
	return ret
		
##
# Extracts are VARSET items in the node
# @return [out] dict of name: text
def extVarSet( node ):
	varset = {}
	for i in range( node.getChildCount() ):
		ch = node.getChild(i);
		if ch.type == SL.VARSET:
			varset[ch.getChild(0).text] = ch.getChild(1).text
	return varset

def asBool( node, str ):
	str = str.lower()
	if str == 'true':
		return True
	if str == 'false':
		return False
	errorOn( node, "expecting true or false" )
