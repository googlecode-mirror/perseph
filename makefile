all: config parser

CLEANS=SchemaParser.py SchemaLexer.py Schema.tokens $(wildcard *.pyc) Schema__.g \
	configure aclocal.m4
CLEANDIRS=$(GENDIR)  autom4te.cache package
clean:
	rm -f $(CLEANS)
	rm -fr $(CLEANDIRS)
	
TESTDIR=test
GENDIR=test/gen
	
$(GENDIR):
	mkdir -p $(GENDIR)
	
.PHONY: test phptest webtest
test: phptest webtest
	
MYSQLURL=mysqli://DBSTestUser:password@localhost/dbs_test
PGSQLURL=pgsql://DBSTestUser:password@localhost/dbs_test

phptest: test-build
	php $(TESTDIR)/alltests.php --mdburl $(MYSQLURL)
	php $(TESTDIR)/alltests.php --mdburl $(MYSQLURL) --nomysql --usedbcharset

phptest-pgsql: test-build $(TESTDIR)/pgsql.schema.inc
	php $(TESTDIR)/alltests.php --mdburl $(PGSQLURL) --nomysql --usedbcharset

nodbphptest: test-build
	php $(TESTDIR)/alltests.php --nodb
	
webtest: test-build
	cd $(TESTDIR) && testplan web_sanity.test +test.properties Debug.Web=/tmp/persephone-web.txt

test-build: parser $(GENDIR)/schema.inc $(GENDIR)/mdb2_schema.inc
	
# include . so that any changes will cause it to regenerate the file
$(GENDIR)/schema.inc: $(TESTDIR)/gen.test.schema $(TESTDIR)/test.schema . | $(GENDIR)
	python Persephone.py $(TESTDIR)/gen.test.schema $(TESTDIR)/source.schema $(TESTDIR)/test.schema $(GENDIR)/

genschema: $(GENDIR)/schema.inc

$(TESTDIR)/pgsql.schema.inc: $(TESTDIR)/gen.pgsql.test.schema . | $(GENDIR)
	python Persephone.py $(TESTDIR)/gen.pgsql.test.schema $(TESTDIR)/source.schema $(TESTDIR)/test.schema $(GENDIR)/pgsql.
	
$(TESTDIR)/gen.test.schema: . | $(GENDIR)
	php dump_provider.php DBTest $(MYSQLURL) > $(TESTDIR)/gen.test.schema
$(TESTDIR)/gen.pgsql.test.schema: . | $(GENDIR)
	php dump_provider.php DBTest $(PGSQLURL) > $(TESTDIR)/gen.pgsql.test.schema
	
$(GENDIR)/mdb2_schema.inc: $(TESTDIR)/test_mdb2.schema . | $(GENDIR)
	python Persephone.py $(TESTDIR)/test_mdb2.schema $(GENDIR)/mdb2_
	
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
	
PACKAGEDIR=package
PACKAGEFILES=$(wildcard *.py) php_support docs LICENSE.txt README.txt
.PHONY: package
package: clean all
	rm -fr $(PACKAGEDIR)
	mkdir $(PACKAGEDIR)
	cp -R $(PACKAGEFILES) $(PACKAGEDIR)
	# Special ANTLR copy
	mkdir -p $(PACKAGEDIR)/antlr/runtime
	cp -R antlr/runtime/Python $(PACKAGEDIR)/antlr/runtime
	
REVISION=$(shell svn info | sed -rne "s/Revision: ([0-9]+)/\1/p" )
svn-package: package
	mv package persephone-$(REVISION)
	tar cjf persephone-$(REVISION).tar.bz2 persephone-$(REVISION)
	
	