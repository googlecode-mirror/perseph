grammar Schema;

options
{
	output=AST;
	language=Python;
	ASTLabelType=CommonTree;	//JAVA/Python Specific?
}

tokens
{
	VARSET;
	OPTION;
	DBFIELDNAME;
	ENTFIELDNAME;
	ENTSUBFIELD;
	NAME;
	MAPEQUALEXPR;
	ALIAS;
	FIELD;
	TYPE;
	TABLENAME;
	LABEL;
	FUNCTION;
	REF;
	COLTYPE;
	OPEQUALS;
	OPLESSTHAN;
	OPGREATERTHAN;
	PLACEHOLDER;
	OPPATTERNMATCH;
}

schema 	
	:	 declaration*;

declaration 	
	:	defaultExpr | providerBlock | entityBlock | mapperBlock | formBlock | listingBlock | customtypeBlock | searchBlock;

defaultExpr	//prefer "default" but Java target doesn't correct the name!	
	:	DEFAULT rawVarSet -> ^(DEFAULT rawVarSet);

varSet 
	:	rawVarSet -> ^(VARSET rawVarSet);
	
rawVarSet
	:	id string ENDEXPR!;

option
	:	id paramBlock? -> ^(OPTION id paramBlock?);
	
paramBlock
	:	'('! param ( ','! param )* ')'!;
	
param
	:	NUMBER|string;

// $<CustomType

customtypeBlock
	:	CUSTOMTYPE id typeDef OPENBLOCK customtypeExpr* CLOSEBLOCK -> ^(CUSTOMTYPE ^(NAME id) typeDef customtypeExpr*);
	
customtypeExpr
	:	varSet;
	
// $>
	
// $<Provider

providerBlock 	
	:	PROVIDER id OPENBLOCK providerExpr* CLOSEBLOCK -> ^(PROVIDER ^(NAME id) providerExpr*);
	
providerExpr 
	:	( providerTableSet | varSet );

providerTableSet
	:	TABLE id OPENBLOCK providerTableExpr* CLOSEBLOCK -> ^(TABLE ^(NAME id) providerTableExpr*);
	
providerTableExpr
	:	id typeDef option* ENDEXPR -> ^(FIELD ^(NAME id) typeDef option*);
	
// $>

	
// $<Entity

entityBlock
	:	ENTITY id OPENBLOCK entityExpr* CLOSEBLOCK -> ^(ENTITY ^(NAME id) entityExpr*);
	
entityExpr
	:	entityFields|entityAliases|varSet;
	
entityFields
	:	FIELDS OPENBLOCK entityFieldExpr* CLOSEBLOCK -> ^(FIELDS entityFieldExpr*);

entityFieldExpr
	:	id typeDef option* ENDEXPR -> ^(FIELD ^(NAME id) typeDef option*) ;
	
entityAliases
	:	ALIASES OPENBLOCK entityAliasExpr* CLOSEBLOCK -> ^(ALIASES entityAliasExpr*);
	
entityAliasExpr
	:	id '=' id ENDEXPR -> ^(ALIAS id id );

// $>
	
// $<Mapper

mapperBlock
	:	MAPPER id OPENBLOCK mapperExpr* CLOSEBLOCK -> ^(MAPPER  ^(NAME id) mapperExpr*);
	
mapperExpr
	:	mapperFields|varSet;
	
mapperFields
	:	FIELDS OPENBLOCK mapperField* CLOSEBLOCK -> ^(FIELDS mapperField*);
	
mapperField
	:	mapperFieldExpr '=' mapperFieldExpr ENDEXPR -> ^(MAPEQUALEXPR mapperFieldExpr mapperFieldExpr)
	|	mapperUsing
	;
	
mapperUsing
	:	USING id OPENBLOCK mapperField* CLOSEBLOCK -> ^(USING id mapperField*);
	
mapperFieldExpr
	:	'@' id -> ^(DBFIELDNAME id)
	|	id -> ^(ENTFIELDNAME id)
	|	id '.' id -> ^(ENTSUBFIELD id id)
	|	id typeDef  '(' mapperFieldExpr ')' -> ^(FUNCTION id typeDef mapperFieldExpr)
	;

// $>
	
// $<Form

formBlock 
	:	FORM id OPENBLOCK formExpr* CLOSEBLOCK -> ^(FORM  ^(NAME id) formExpr*);
	
formExpr
	:	formFields | varSet;
	
formFields
	:	FIELDS OPENBLOCK formField* CLOSEBLOCK -> ^(FIELDS formField*);
	
formField
	:	id option* ENDEXPR -> ^(FIELD ^(NAME id) option*) ;

// $>

// $<Listing

listingBlock 
	:	LISTING id OPENBLOCK listingExpr* CLOSEBLOCK -> ^(LISTING  ^(NAME id) listingExpr*);
	
listingExpr
	:	listingFields | varSet;
	
listingFields
	:	FIELDS OPENBLOCK listingField* CLOSEBLOCK -> ^(FIELDS listingField*);
	
listingField
	:	listingFunc string ENDEXPR -> ^(FIELD listingFunc ^(LABEL string)) 
	|	listingFunc ENDEXPR -> ^(FIELD listingFunc) ;

listingFunc
	:	id '(' idOrRef ')' -> ^(FUNCTION id idOrRef)
	|	id -> ^(NAME id);
	
idOrRef 
	:	id -> ^(NAME id)
	|	'@' id -> ^(REF id);
// $>

//$<Search

searchBlock
	:	SEARCH id typeDef OPENBLOCK searchExpr* CLOSEBLOCK -> ^(SEARCH ^(NAME id) typeDef searchExpr*);
	
searchExpr
	:	searchFilterExpr | searchSortExpr;
	
searchFilterExpr
	:	FILTER sfeExpr ENDEXPR -> ^(FILTER sfeExpr);
	
searchSortExpr
	:	SORT id order=(ASC|DESC) ENDEXPR -> ^(SORT id {$order});
	
sfeExpr 
	:	id sfeOP sfeRef -> ^(sfeOP id sfeRef);
	
sfeRef
	:	id -> ^(FIELD id)
	|	'?' -> PLACEHOLDER
	|	STRING
	|	NUMBER
	;

sfeOP
	: '=' -> OPEQUALS
	| '<' -> OPLESSTHAN
	| '>' -> OPGREATERTHAN
	| '~=' -> OPPATTERNMATCH
	;
//$>

string	
	:	
	id
	| STRING
	;
	
id	
	:	
	PROVIDER
	| MAPPER
	| TABLE
	| FIELDS
	| DEFAULT
	| ALIASES
	| ENTITY
	| USING
	| RAWID
	| FORM
	| LISTING
	| CUSTOMTYPE
	| FILTER
	| SEARCH
	| SORT
	| ASC
	| DESC
	;

typeDef	
	:	'<' id '>' -> ^(TYPE id)
	|	'<' id typeDef '>' -> ^(COLTYPE id typeDef);

	
// $<Keywords

//These work like tokens, but they don't need to be in the token section? Why?
PROVIDER	:	'provider';
FIELDS	:	'fields';
DEFAULT	:	'default';
TABLE	:	'table'	;
ENTITY	:	'entity'	;
MAPPER	:	'mapper'	;
ALIASES	:	'aliases';
USING	:	'using';
FORM	:	'form';
LISTING	:	'listing';
CUSTOMTYPE	:	'type';
FILTER	:	'filter';
SEARCH	:	'search';
SORT		:	'sort';
ASC	:	'ASC';
DESC	:	'DESC';

// $>

RAWID	:	(UN_LETTER|'_')(UN_LETTER|UN_DIGIT|'_'|'-')*;
NUMBER	:	(UN_DIGIT|'.')+;
COMMENT	:	'/*'  .* '*/' { $channel = HIDDEN; };
ENDEXPR	:	';';
OPENBLOCK	:		'{';
CLOSEBLOCK	:	'}';
STRING	:	
	'"'! ~'"'+ '"'! { self.setText(self.getText()[1:-1]);} 	//PYTHON:
	;
	
//put last so it has no precedence (will not interfere with strings then)
WHITESPACE 	: ( '\t' | ' ' | '\r' | '\n'| '\u000C' )+  { $channel = HIDDEN; };

// $<Unicode Classes

//TODO: Proper unicode character classes
fragment UN_LETTER 
	:	 ('a'..'z'|'A'..'Z');
fragment UN_DIGIT
	:	('0'..'9');

// $>

