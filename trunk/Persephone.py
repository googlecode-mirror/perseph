#!/usr/bin/python
import sys, os

if len( sys.argv ) < 3:
	print "Syntax: input.schema [input2.schema] output/dir/base_\n"
	sys.exit( 1 )
	
infiles = sys.argv[1:len(sys.argv)-1]
outbase = sys.argv[len(sys.argv)-1]

# import antlr (relative to ourself)
ourpath = os.path.abspath( os.path.dirname( sys.argv[0] ) )
sys.path.append('%s/antlr/runtime/Python' % ourpath)
import antlr3
	
###########################################
# Parsing
import SchemaLexer as SL
from SchemaParser import SchemaParser
from DBSchemaProc import Processor
from DBSchemaPHP import PHPEmitter

def showTree( node, prefix ):
	if node.isNil():
		print "null"
	else:
		tok = node.getToken()
		print prefix , tok.getType() , ":" , tok.getText()
		
	for ci in range( node.getChildCount() ):
		showTree( node.getChild( ci ), prefix + "  " )
		
# Use a common processor for all files
proc = Processor()
for infile in infiles:
	print "Processing " + infile + "...\n"
	char_stream = antlr3.ANTLRInputStream( open( infile, 'r' ) )

	lexer = SL.SchemaLexer(char_stream)
	tokens = antlr3.CommonTokenStream(lexer)
	parser = SchemaParser(tokens)
	root = parser.schema()

	#showTree( root.tree, "" )
	proc.collect( root.tree )


# Process the data
proc.process( )

##
# Emit now
#print root.tree.toStringTree()
emit = PHPEmitter( proc.sc )
emit.emit( outbase );
