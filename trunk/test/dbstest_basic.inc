<?php

class DBSTest_Clean extends TestCase {
	function testCleanup() {
		DBSTest::searchAndDelete( DBS_Query::matchAll() );
		DBSStrings::searchAndDelete( DBS_Query::matchAll() );
		DBSTwoKeys::searchAndDelete( DBS_Query::matchAll() );
		DBSName::searchAndDelete( DBS_Query::matchAll() );
		
		# Setup names table
		$names = array( 
			1 => "One",
			2 => "Two",
			3 => "Three"
			);
		foreach( $names as $id => $value ) {
			$q = DBSName::createWithID( $id );
			$q->name = $value;
			$q->add();
		}
	}
}

class DBSTest_Basic extends TestCase {
	function testAddFind() 	{
		$n = DBSTest::createWithNothing();
		$n->name = 'T❀stNäm€' . time();	//include some unicode, latin-1, and latin-15 overlap characters
		$n->date = rand( 1000, 10000 ) * 3600*24;	//TODO: hmm, php has no native Date type
		$n->time = rand( 0, 100000 );
		$n->dateTime = time();
		$n->decimal = rand( 0, 100000 ) / 1000.0;
		$n->float = rand() / getrandmax();
		
		$this->assertFalse( $n->exists() );
		$n->add();
		$this->assertTrue( $n->exists() );
		
		$this->assertTrue( $n->id > 0 );	//lastInsert
		
		$l = DBSTest::findWithName( $n->name );
		//TODO: precision/comparison of 'float'?
		foreach( array( 'id', 'name', 'date', 'time', 'dateTime', 'bool', 'decimal' ) as $comp)
			$this->assertEquals( $n->$comp, $l->$comp, "Compare: $comp" );
		
		//by id
		$l = DBSTest::findWithID( $n->id );
		$this->assertEquals( $n->name, $l->name );
		
		//field based search
		$l = DBSTest::withNothing();
		$l->id = $n->id;
		$l->find();
		$this->assertEquals( $n->name, $l->name );
	}
	
	/**
	 * The duplicate name should fail since the DB has it marked as Unique
	 */
	function testDupName() {
		$name = "Simple:" . time();
		$n = DBSTest::createWithName( $name );
		$n->decimal = 97.5;
		$n->add();
		
		$m = DBSTest::createWithName( $name );
		$m->decimal = 82.75;
		try {
			$m->add();
			$this->assertTrue( false );
		} catch( DBS_DBException $ex ) {
			$this->assertEquals( DBS_DBException::ADD_ALREADY_IN_DB, $ex->getCode() );
		}
	}
	
	function testLink() {
		$n = DBSTest::createWithNothing();
		$n->name = "Link." . time();
		$n->add();
		
		$l = DBSLink::createWithNothing();
		$l->basic = $n;
		$l->add();
		
		$nk = DBSLink::findWithID( $l->id );
		$this->assertEquals( $l->basic->id, $n->id );
		$this->assertEquals( $l->basic->name, $n->name );
	}
	
	function testNameRef() {
		$n = DBSTest::createWithName( "REFTEST" );
		$n->nameRef = DBSName::withID( 2 );
		$n->add();
		
		$q = DBSTest::findWithID( $n->id );
		$this->assertEquals( "Two", $n->nameRef->name );
	}
	
	function testFindCreate() {
		$q = DBSTest::createWithName( 'FindCreate' );
		$q->add();
		
		$f = DBSTest::findOrCreateWithName( $q->name );
		$this->assertEquals( $q->id, $f->id );
		
		$n = DBSTest::findOrCreateWithName( 'FC2' );
		$this->assertFalse( $n->__has( 'id' ) );
	}
	
	function testAttemptID() {
		$q = DBSTest::createWithID( 123 );	//TODO: perhaps this function should not be created for LOAD_ONLY keys?
		try {
			$q->add();
			$this->assertTrue( false );
		} catch( DBS_FieldException $ex ) {	
			$this->assertEquals( DBS_FieldException::SAVE_LOAD_ONLY, $ex->getCode() );
		}
	}
	
	function testBadFlow() {
		$q = DBSTest::createWithName('saveforadd');
		try {	
			$q->save();
			$this->assertTrue( false );
		} catch( DBS_LogicException $ex ) {
			$this->assertEquals( DBS_LogicException::ONLY_SAVE_EXTANT, $ex->getCode() );
		}
		
		$q->add();
		$q->float = 123.3;
		try {
			$q->add();
		} catch( DBS_LogicException $ex ) {
			$this->assertEquals( DBS_LogicException::ONLY_ADD_NEW, $ex->getCode() );
		}
		
		$q->save();
	}
	
	function testDirtySave() {
		$q = DBSTest::createWithName( 'dirty' );
		$q->decimal = 10.5;
		$q->float = 128;
		$q->add();
		
		$q->decimal = 20.25;
		$q->float = 456;
		$q->__markClean( 'float' );
		$q->save();
		
		$l = DBSTest::findWithName( 'dirty' );
		$this->assertEquals( 20.25, $l->decimal );
		$this->assertEquals( 128, $l->float );
	}
	
	function testDelete() {
		$q = DBSTest::createWithName( 'deleteme' );
		$q->add();
		
		//we only need one ALT_RECORD_KEY to delete
		$d = DBSTest::withName( $q->name );
		$d->delete();
		
		try {
			$l = DBSTest::findWithName( $q->name );
			$this->assertTrue( false );
		} catch( Exception $ex ) {
			$this->assertTrue( true );
		}
	}
	
	function testSearch() {
		for( $i = 1; $i <= 10; $i++ ) {
			$q = DBSTest::createWithName( "Search:$i" );
			$q->decimal = $i;
			$q->add();
		}
		
		$count = 0;
		$found = DBSTest::search( 
			DBS_Query::matchAndGroup( 
				DBS_Query::match( 'decimal', '5', '>' ) ,
				DBS_Query::matchStringPattern( 'name', 'Search:*' )
				)
			);
		foreach( $found as $l ) {
			$this->assertTrue( $l->decimal > 5 );
			$count++;
		}
		$this->assertEquals( 5, $count );
		
		//sorted
		$ordered = DBSTest::search( 
			DBS_Query::matchStringPattern( 'name', 'Search:*' ),
			DBS_Query::sort( 'decimal', DBS_Query::SORT_ASC )
			)->loadAll();
		for( $i = 1; $i <= 10; $i++ )
			$this->assertEquals( $i, $ordered[$i-1]->decimal );
			
		//keyed (use Scheme search)
		$ordered = KeySortSearch::search()->loadAll( 'decimal' );
		for( $i = 1; $i <= 10; $i++ )
			$this->assertEquals( $i, $ordered[$i]->decimal );
			
		//test delete
		DBSTest::searchAndDelete( DBS_Query::matchStringPattern( 'name', 'Search:*' ) );
		$this->assertEquals( 0, count( DBSTest::search( DBS_Query::matchStringPattern( 'name', 'Search:*' ) )->loadAll() ) );
	}
	
	function testDefault() {
		$q = DBSTest::createWithNothing();
		$this->assertEquals( 123.5, $q->float );
		
		$q = DBSTest::createWithName( "SaveDefault" );
		$q->add();
		
		$n = DBSTest::findWithName( "SaveDefault" );
		$this->assertEquals( 123.5, $n->float );
	}
	
	function testTypeRestrictions() {
		$q = DBSTest::createWithNothing();
		try {
			$q->float = "abs";	//expecting exception
			$this->assertTrue( false );
		} catch( DBS_SetFieldException $e ) {
			$this->assertEquals( DBS_SetFieldException::TYPE_NUMERIC, $e->getType() );
			$this->assertEquals( 'float', $e->field );
		}
		
		try {
			$q->decimal = null;
			$this->assertTrue( false );
		} catch( DBS_SetFieldException $e ) {
			$this->assertEquals( DBS_SetFieldException::TYPE_NULL, $e->getType() );
			$this->assertEquals( 'decimal', $e->field );
		}
		
		$q->dateTime = null;
		$this->assertEquals( null, $q->dateTime );
	}
	
	function testMaxLen() {
		$q = DBSTest::createWithNothing();
		$q->name = "01234567890123456789012345678901234567890123456789"; //50 chars
		try {
			$q->name = "01234567890123456789012345678901234567890123456789!"; //51 chars
			$this->assertTrue( false );
		} catch( DBS_SetFieldException $e ) {
			$this->assertEquals( DBS_SetFieldException::TYPE_LEN, $e->getType() );
			$this->assertEquals( 'name', $e->field );
		}
		$this->assertEquals( "01234567890123456789012345678901234567890123456789", $q->name );
		
	}
	
	function testAliases() {
		$q = DBSTest::createWithNothing();
		$q->decimal = 14;
		$this->assertEquals( 14, $q->aNumber );
		$q->aNumber = 17;
		$this->assertEquals( 17, $q->decimal );
	}
	
	/**
	 * The system should allow changing of keys, which is a special case since it needs
	 * to retain the keys used to load/find the object in order to change those keys.
	 */
	function testAlterKey() {
		$q = DBSTest::createWithName( "Change Me" );
		$q->add();
		$id = $q->id;
		
		$q->name = "New Name";
		$q->save();
		
		$n = DBSTest::findWithID( $id );
		$this->assertEquals( "New Name", $n->name );
		
		//do it again, since after save the keys have changed
		$q->name = "Yet Newer";
		$q->save();
		
		$n = DBSTest::findWithID( $id );
		$this->assertEquals( "Yet Newer", $n->name );
		
		
		//though still disallow changing load-only fields
		$q->id = 45;
		try {
			$q->save();
			$this->assertTrue( false );
		} catch( DBS_FieldException $e ) {
			$this->assertEquals( DBS_FieldException::SAVE_LOAD_ONLY, $e->getCode() );
			$this->assertEquals( 'id', $e->field );
		}
		
		//also test via searching, since it uses an alternate load mechanism
		$allq = DBSTest::search( DBS_Query::match( 'name', 'Yet Newer' ) )->loadAll();
		$q =& $allq[0];
		$q->name = 'Again Newer';
		$q->decimal = 12345;
		$q->save();
		
		$n = DBSTest::findWithID( $id );
		$this->assertEquals( 'Again Newer', $n->name );
		
		//okay, check case of attempting to save a value from incomplete search
		$allq = DBSTest::search( DBS_Query::match( 'decimal', 12345 ), DBS_Query::fieldLimit( 'decimal' ) )->loadAll();
		$q =& $allq[0];
		$q->decimal = 12;
		try {
			$q->save();
			$this->assertTrue( false );
		} catch( DBS_LogicException $e ) {
			$this->assertEquals( DBS_LogicException::SAVE_INCOMPLETE_LOAD, $e->getCode() );
		}
	}
	
	function testTwoKeys() {
		$data = array(
			array( 1, "A", "ABC" ),
			array( 1, "B", "BCD" ),
			array( 2, "B", "DCB" ),
			);
		foreach( $data as $d ) {
			$n = DBSTwoKeys::createWithNum_Name( $d[0], $d[1] );
			$n->value = $d[2];
			$n->add();
		}
		
		$this->assertEquals( "ABC", DBSTwoKeys::findWithNum_Name( 1, "A" )->value );
		$this->assertEquals( "DCB", DBSTwoKeys::findWithNum_Name( 2, "B" )->value );
		
		//finding by just one part of a key is forbidden
		$j = DBSTwoKeys::withNothing();
		$j->num = 2;
		try {
		 	$j->find();
		 	$this->assertTrue( false );
		} catch( DBS_FieldException $e ) {
		}
		
		//searching however is just fine
		//...
	}
	
	function testConvertFunc() {
		//createing with logical name is still possible
		$q = DBSStrings::createWithNothing();
		//complete reassignment is the easiest way to do this... (TODO: tech note about arrays in PHP)
		$q->labels = array( "happy", "go", "lucky" );
		$q->add();
		
		//though using the derived name is likely preferred in your app
		$n = DerivedStrings::findWithMyID( $q->myID );
		$this->assertEquals( 3, count( $n->labels ) );
		for( $i = 0; $i < count( $q->labels ); $i++ )
			$this->assertEquals( $q->labels[$i], $n->labels[$i] );
			
		//check the types, we're expecting the DerivedStrings class
		$this->assertTrue( $n instanceof DerivedStrings );
		$this->assertTrue( $q instanceof DerivedStrings );
		$this->assertTrue( $q->contains( "go" ) );
		
		//test search with converted id...
		$res = MyDBSStrings::search( $q->myID )->loadAll();
		$this->assertEquals( 1, count( $res ) );
		$this->assertEquals( $q->myID, $res[0]->myID );
	}
}

?>