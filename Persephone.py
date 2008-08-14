import sys

if len( sys.argv ) != 3:
	print "Syntax: input.schema output/dir/base_\n"
	sys.exit( 1 )
	
infile = sys.argv[1]
outbase = sys.argv[2]

sys.path.append('antlr/runtime/Python')
import antlr3
	
###########################################
# Parsing
import SchemaLexer as SL
from SchemaParser import SchemaParser
from DBSchemaProc import Processor
from DBSchemaPHP import PHPEmitter

char_stream = antlr3.ANTLRInputStream( open( infile, 'r' ) )

lexer = SL.SchemaLexer(char_stream)
tokens = antlr3.CommonTokenStream(lexer)
parser = SchemaParser(tokens)
root = parser.schema()

def showTree( node, prefix ):
	if node.isNil():
		print "null"
	else:
		tok = node.getToken()
		print prefix , tok.getType() , ":" , tok.getText()
		
	for ci in range( node.getChildCount() ):
		showTree( node.getChild( ci ), prefix + "  " )

#showTree( root.tree, "" )
		
######################################
# Main
proc = Processor()
proc.process( root.tree )

#print root.tree.toStringTree()
emit = PHPEmitter( proc.sc )
emit.emit( outbase );
