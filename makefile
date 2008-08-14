all: parser

CLEANS=SchemaParser.py SchemaLexer.py Schema.tokens $(wildcard *.pyc) Schema__.g
CLEANDIRS=$(GENDIR)
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
