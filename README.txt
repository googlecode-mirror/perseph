[Description]

	Persephone is a data abstraction mechanism. Its purpose is to remove all the tedious parts of working with databases and lets you focus on real code. Standard searching, loading, and saving of data to/from databases is handled automatically -- along with protection for data types and incorrect operations. Beyond persistence Persephone can also generate HTML listings and Forms for your data.
	
	Unlike ActiveRecord style systems, Persephone assumes you have a lot of existing code and/or and existing database and have no ability, nor desire, to completely replace it. Thus Persephone operates in a miminally invasive manner, by being very clear about what it is doing, and operating happily alongside alternate solutions. There are no method assumptions, no prescriptive behaviours, and basically nothing that will make curse the solution.
	
	Currently Persephone supports PHP code generation.  Other targets are possible, the source schema language is not PHP specific.
	

[Install]

	-- Requirements --

	You will need these programs / packages installed:
		gnu make
		php 5.2 or higher
		
		Pear:
		MDB2 (technically optional)
		
	???

		
[Test]

To run the tests you need to have persephone's php_support in the php include path:

# ln -s /opt/persephone/php_support /usr/share/php/persephone

assuming persephone is installed in /opt/persephone.

You will need to have MySQL installed to test the Persephone setup.

    This will also require PHP to be installed, but we assume you have that as it is the only supported target so far with Persephone.

MySQL Setup

In the test/test_db.sql is the SQL you will need to create the test database. Note that the first part of actual database creation has been commented out for safety reasons. You will need to run that, or similar commands at least once before the remainder of the setup.

A typical setup sequence:

$> mysql

mysql> DROP DATABASE if exists dbs_test;
Query OK, 0 rows affected (0.06 sec)

mysql> CREATE DATABASE `dbs_test` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
Query OK, 1 row affected (0.00 sec)

mysql> GRANT ALL PRIVILEGES ON dbs_test.* to 'DBSTestUser'@'localhost' IDENTIFIED BY 'password';
Query OK, 0 rows affected (0.00 sec)

Note that the password really is password, that is expected by the test scripts.
PHP Setup

Then source the rest of the commands, the path below will be wherever you installed Persephone.

mysql> source /opt/persephone/test/test_db.sql

Before continuing with the test you will also need to configure the code for use in PHP. Refer to Setup PHP Environment and Paths→.

If you run make test now at least have of the test should work. The "Running as MySQLSource" half will work, but you might get a failure under "Running as MDB2DBSource".
MDB2 Setup

If you wish to use MDB2 and not the native DBSource wrappers you will need to install MDB2 and the MySQLI module (and any other DB modules you intend on using).

Sample commands:

pear install --alldeps pear/MDB2 pear/Log MDB_QueryTool HTML_QuickForm
pear install MDB2#mysql

    HTML_QuickForm also shown since it is used for Form generation

Apache Setup

In order to have the TestPlan↗ test suite run you will also need to install the PHP pages. The /opt/persephone/test folder is expected to be configured as http://persephone.local.
Add persephone.local to the 127.0.0.1 line in /etc/hosts.
The test/apache.vhost file is a usable configuration for Apache as a virtual host. Refer to the notes in the file on how to configure it correctly.

If you have some other setup you can easily point the test to a new location by altering the test/test.properties file.

You will need testplan installed: http://testplan.brainbrain.net/Entry:26/Download_and_Install
