all: config parser

CLEANS=SchemaParser.py SchemaLexer.py Schema.tokens $(wildcard *.pyc) Schema__.g \
	configure aclocal.m4
CLEANDIRS=$(GENDIR)  autom4te.cache
clean:
	rm -f $(CLEANS)
	rm -fr $(CLEANDIRS)
	
TESTDIR=test
GENDIR=test/gen
	
$(GENDIR):
	mkdir $(GENDIR)
	
.PHONY: test
test: test-build
	php $(TESTDIR)/alltests.php
	
test-build: $(GENDIR)/schema.inc
	
# include . so that any changes will cause it to regenerate the file
$(GENDIR)/schema.inc: $(TESTDIR)/test.schema . | $(GENDIR)
	python Persephone.py $(TESTDIR)/test.schema $(GENDIR)/
	
Persephone.py: | parser

parser: SchemaParser.py

ANTLRJARS=$(wildcard antlr/lib/*.jar)
ANTLRCP:=`for i in $(ANTLRJARS); do echo -n $$i:; done`
SchemaParser.py: Schema.g
	java -cp $(ANTLRCP) org.antlr.Tool Schema.g

##
# Configure doesn't do much for us beyond checking the environment
config: configure 
	./configure
	
configure: aclocal.m4 configure.ac
	autoconf
	
aclocal.m4: configure.ac
	aclocal -I autoconf/
	