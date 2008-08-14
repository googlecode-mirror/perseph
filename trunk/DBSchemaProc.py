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
			SL.FORM: [],
			}
			
		self.sc = DBSchema.Root()
	
	def process( self, root ):
		for i in range( root.getChildCount() ):
			ch = root.getChild( i )
			self.rawDecls[ch.getToken().type].append( ch )
			
		self.processDefaults( )
		self.processTypes( )
		self.processProviders( )
		self.processEntities( )
		self.processMappers( )
		self.processForms( )
		self.processListings( )
		
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
			self.sc.types[name] = DBSchema.Entity(name)
		
	def processProviders( self ):
		for prov in self.rawDecls[SL.PROVIDER]:
			name = extProp( prov, SL.NAME )
			varset = extVarSet( prov )
			type = varset["type"]
			provider = None
			if type == "DBSource":
				checkVarSet( prov, varset, ["type","var"], [] )
				self.sc.providers[name] = provider = DBSchema.Provider_DBSource( varset["var"] )
			else:
				errorOn( prov, "Unknown type in provider: %s" % name )
			
			tableNodes = extTableNodes( prov )
			for tableNode in tableNodes:
				tableName = extProp( tableNode, SL.NAME )
				table = DBSchema.Provider_Table( tableName )
				provider.tables[tableName] = table
				
				for fieldSpec in extAllField( tableNode ):
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
			varset = extVarSet( ent )
			checkVarSet( ent, varset, [], ['class']	)
			
			# previously created in processTypes
			entity = self.sc.types[ name ]
			
			if 'class' in varset:
				entity.className = varset['class']
			
			# Fields -------------------------------------------------------------
			fields = extFields( ent )
			for fieldSpec in fields:
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
					elif opt[0] == 'LOAD_ONLY':
						field.loadOnly = True
					elif opt[0] == 'TITLE':
						field.title = True
					elif opt[0] == 'MAXLEN':
						field.maxLen = int( opt[1] )
					elif opt[0] == 'ALLOW_NULL':
						field.allowNull = True;
					elif opt[0] == 'LABEL':
						field.label = opt[1]
					elif opt[0] == 'DESC':
						field.desc = opt[1]
					else:
						errorOn( fieldSpec, "unrecognized option: %s " % opt )
					
				# Default label to the field name
				if field.label == None:
					field.label = field.name
				
				entity.fields[fieldName] = field
			
			# Aliases -----------------------------------------------------------
			aliases = extAliases( ent )
			for alias in aliases:
				nameA, nameB = alias
				fieldA = nameA in entity.fields
				fieldB = nameB in entity.fields
				if fieldA == fieldB:
					errorOn( ent, "%s, %s, one must be field, one not" % (nameA, nameB ) )
					
				if fieldA:
					entity.aliases[nameB] = nameA
				else:
					entity.aliases[nameA] = nameB
					
			self.sc.entities[name] = entity
			
			
	def processMappers( self ):
		for mapperNode in self.rawDecls[SL.MAPPER]:
			name = extProp( mapperNode, SL.NAME )
			varset = extVarSet( mapperNode )
			checkVarSet( mapperNode, varset, ['provider' ], [] )
			
			if not varset['provider'] in self.sc.providers:
				errorOn( mapperNode, "invalid provider %s" % varset['provider'] )
			if not name in self.sc.entities:
				errorOn( mapperNode, "does not match an entity %s" % name )
				
			mapper = DBSchema.Mapper( self.sc.providers[varset['provider']] )
			mapper.entity = self.sc.entities[name]
			self.sc.mappers[name] = mapper
			
			fieldsNode = extNode( mapperNode, SL.FIELDS )
			for i in range( fieldsNode.getChildCount() ):
				node = fieldsNode.getChild(i)
				if node.type == SL.USING:
					using = node.getChild(0).text
					#temporary table set until we support multiple tables
					if mapper.table != "":
						errorOn( node, "Duplicate table spec, multi-tables not supported" )
					mapper.table = mapper.provider.tables[using];
					
					for j in range(1,node.getChildCount() ):
						expr = node.getChild(j)
						mapField = DBSchema.Mapper_Field()
						mapper.fields.append( mapField )
						
						if expr.type == SL.MAPEQUALEXPR:
							left = self.getMapperFieldExpr( expr.getChild(0) )
							right = self.getMapperFieldExpr( expr.getChild(1) )
							if left['db'] == right['db']:
								errorOn( expr, "requires one database and one entity field" )
								
							( db, ent ) = ( left, right ) if left['db'] else ( right, left )
							if ent['func'] != None:
								errorOn( expr, "functions not supported on entity side, use inverse on DB side" )
								
							if db['func'] != None:
								mapField.db_convert_func = db['func']
								mapField.db_convert_type = db['func_type']
								
							#TODO: check that fields exist
							mapField.db_field = mapper.table.fields[db['name']]
							mapField.ent_field = mapper.entity.fields[ent['name']]
							
							if ent['subfield'] != None:
								mapField.ent_field_field = mapField.ent_field.fieldType.fields[ent['subfield']]
							
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
			res['func'] = node.getChild(0).text
			res['func_type'] = self.getType( node )
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
		
	def processForms( self ):
		for formNode in self.rawDecls[SL.FORM]:
			name = extProp( formNode, SL.NAME )
			varset = extVarSet( formNode )
			checkVarSet( formNode, varset, [ 'entity' ], [ 'allowDelete', 'addFields' ] )
			
			form = DBSchema.Form( name )
			self.sc.forms[name] = form
			form.allowDelete = asBool( formNode, varset.get( 'allowDelete', 'false' ) )
			
			addFields = varset.get( 'addFields', 'none' ).lower()
			if not addFields in [ 'all', 'none' ]:
				errorOn( formNode, 'addFields must be one of [all,none]' )
				
			if not varset['entity'] in self.sc.entities:
				errorOn( formNode, "refers to non-extant entity: %s" % varset['entity'] )
			form.entity = self.sc.entities[varset['entity']]
				
			# Special fields are handled now, otherwise defaults are taken for all fields
			coveredFields = {}
			fieldsNode = extNode( formNode, SL.FIELDS )
			for i in range( fieldsNode.getChildCount() ):
				node = fieldsNode.getChild(i)
				
				name = extProp( node, SL.NAME )
				if not name in form.entity.fields:
					errorOn( node, "field not in entity %s" % name )
				ff = DBSchema.Form_Field( form.entity.fields[name] )
				coveredFields[name] = True
				form.fields.append( ff )
				
				# Collect options
				opts = extOptions( node )
				for opt in opts:
					if opt[0] == 'HIDDEN':
						ff.hidden = True
					elif opt[0] == 'READ_ONLY':
						ff.readonly = True
					else:
						errorOn( node, "unrecognized option %s" % opt[0] )
			
			#fill in all default fields (by default, all entity fields are included)
			if addFields == 'all':
				for field in form.entity.fields.itervalues():
					if not field.name in coveredFields:
						coveredFields[field.name] = True
						form.fields.append( DBSchema.Form_Field( field ) )
			
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

def extTableNodes( node ):
	ret = []
	for i in range( node.getChildCount() ):
		if node.getChild(i).type == SL.TABLE:
			ret.append( node.getChild( i ) )
	return ret
			
	
def extFields( node ):
	for i in range( node.getChildCount() ):
		ch = node.getChild( i )
		if ch.type == SL.FIELDS:
			return extAllField( ch )
			
	errorOn( node, "Missing fields in entity" )
	
def extAllField( node ):
	all = []
	for j in range( node.getChildCount() ):
		field = node.getChild(j)
		if field.type != SL.FIELD:
			continue
		all.append( field )
		
	return all
	
def extAliases( node ):
	aliases = extNodeOpt( node, SL.ALIASES )
	if( aliases != None ):
		all = []
		for j in range( aliases.getChildCount() ):
			alias = aliases.getChild(j)
			if alias.type != SL.ALIAS:
				errorOn( alias, "Expecting ALIAS" )
			all.append( [alias.getChild(0).text,alias.getChild(1).text] )
				
			return all
	return []
			
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
