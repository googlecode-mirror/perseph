<?php

class DBSTest_Clean extends TestCase {
	function testCleanup() {
		DBSTest::searchAndDelete( DBS_Query::matchAll() );
		DBSStrings::searchAndDelete( DBS_Query::matchAll() );
		DBSTwoKeys::searchAndDelete( DBS_Query::matchAll() );
		DBSName::searchAndDelete( DBS_Query::matchAll() );
		DBSLinkNames::searchAndDelete( DBS_Query::matchAll() );
		SimpleBasic::searchAndDelete( DBS_Query::matchAll() );
		SimpleName::searchAndDelete( DBS_Query::matchAll() );
		
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
		global $skipCaseTest;
		
		$n = DBSTest::createWithNothing();
		$n->name = 'T❀stNäm€' . time();	//include some unicode, latin-1, and latin-15 overlap characters
		
		# Create a date outside the 32-bit int range (to ensure proper Date support)
		$date = new Date( rand( -10000, 10000 ) );
		$date->setYear( rand( 2500, 5000 ) );
		$date->setHour( 0 );
		$date->setMinute( 0 );
		$date->setSecond( 0 );
		$n->date = $date;
		if( TestLimit::$time24H )
			$n->time = rand( 0, 3600*24 );	//some DB's are limited to 24H
		else
			$n->time = rand( -100000, 100000 );	//be sure to have negatives tested as well
		$n->dateTime = new Date( rand( -1000000000, -10000000 ), DATE_FORMAT_UNIXTIME ); //this time use negative
		$n->decimal = rand( 0, 100000 ) / 1000.0;
		$n->float = rand() / getrandmax();
		$n->memoryOnly = 1234;	//value will just be lost on reload (nothing really to test, perhaps when caching is introduced)
		
		$this->assertFalse( $n->exists() );
		$n->add();
		$this->assertTrue( $n->exists() );
		
		$this->assertTrue( $n->id > 0 );	//lastInsert
		
		if( $skipCaseTest )
			$l = DBSTest::findWithName( $n->name ); //in a mismatched encoding connection the backend can't properly match case
		else
			$l = DBSTest::findWithName( strtoupper($n->name) );	//we expect a case-insensitive match, but the name must match what was in the DB!
		//TODO: precision/comparison of 'float'?
		foreach( array( 'id', 'name', 'time', 'bool', 'decimal' ) as $comp)
			$this->assertEquals( $n->$comp, $l->$comp, "Compare: $comp" );
		foreach( array( 'date', 'dateTime' ) as $comp)
			$this->assertTrue( $n->$comp->equals( $l->$comp ), "Compare: $comp / {$n->$comp->getDate()} == {$l->$comp->getDate()}" );
		
		//by id
		$l = DBSTest::findWithID( $n->id );
		$this->assertEquals( $n->name, $l->name );
		
		//field based search
		$l = DBSTest::withNothing();
		$l->id = $n->id;
		$l->find();
		$this->assertEquals( $n->name, $l->name );
		
		//lenient/strict find
		$l->find();	//expect no exception
		try {
			$l->find( true /*strict*/ );
			$this->assertTrue( false );
		} catch( DBS_LogicException $le ) {
			$this->assertEquals( DBS_LogicException::FIND_NOT_UNKNOWN, $le->getCode() );
		}
	}
	
	function testIdentifier() {
		$n = DBSTest::createWithName( "ByID" );
		$n->float = 516;
		$n->add();
		
		$q = DBSTest::withIdentifier( $n->getIdentifier() );
		$this->assertEquals( 516, $q->float );
		
		//with partial keys
		$l = DBSTest::withID( $n->id );
		$m = DBSTest::withIdentifier( $l->getIdentifier() );
		$m->find();
		$this->assertEquals( 516, $q->float );
		
		$l = DBSTest::withName( $n->name );
		$m = DBSTest::withIdentifier( $l->getIdentifier() );
		$this->assertEquals( 516, $q->float );
		
		//with an explicit null
		$n = DBSTest::createWithNothing();
		$n->float = 879;
		$n->name = null;
		$n->add();
		
		$l = DBSTest::withIdentifier( $n->getIdentifier() );
		$this->assertEquals( 879, $l->float );
	}
	
	function testExplicitIdentifier() {
		$q = DBSIdentEx::createWithName( "Explicit1" );
		$q->value = 435;
		$curID = $q->anyIdentifier;	//capture before we have an ID
		$q->add();
		
		$this->assertEquals( "{$q->id}", $q->identifier );
		
		$a = DBSIdentEx::withIdentifier( $curID );
		$this->assertEquals( 435, $a->value );
		
		$b = DBSIdentEx::withIdentifier( "{$q->id}" );	//explicit form here
		$this->assertEquals( 435, $b->value );
	}
	
	function testReload() {
		$n = DBSTest::createWithName( 'ReloadMe' );
		$n->float = 123;
		$n->add();
		
		$same = DBSTest::findWithName( 'ReloadMe' );
		$same->float = 415;
		$same->save();
		
		$this->assertEquals( 123, $n->float );
		$n->reload();
		$this->assertEquals( 415, $n->float );
		
		//test some tricky scenarios (failed in practice)
		$n = NullKey::createWithNothing( );
		$n->decimal = 10;
		$n->add();
		$n->reload();
		
		$n = NullKey2::createWithNothing( );
		$n->decimal = 11;
		$n->add();
		$n->reload();
		
		//test lenient reload
		$lenient = DBSTest::withName( 'ReloadMe' );
		try {
			$lenient->reload( true /*strict*/ );
			$this->assertTrue( false );
		} catch( DBS_LogicException $le ) {
			$this->assertEquals( DBS_LogicException::RELOAD_NOT_EXTANT, $le->getCode() );
		}
		$lenient->reload();
	}
	
	function testReloadDirty() {
		$n = DBSTest::createWithName( 'ReloadDirty' );
		$n->float = 123;
		$n->add();
		
		$n->float = 412;
		try {
			$n->reload();
			$this->fail();
		} catch( DBS_FieldException $ex ) {
			$this->assertEquals( 'float', $ex->field );
			$this->assertEquals( DBS_FieldException::LOAD_DIRTY, $ex->getCode() );
		}
	}
	
	function testFindFail() {
		try {
			$n = DBSTest::findWithName( "NeverInDB" );
			$this->fail();
		} catch( DBS_DBException $ex ) {
			$this->assertEquals( DBS_DBException::NOT_IN_DB, $ex->getCode() );
		}
		
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
	
	function testSaveOnly() {
		$n = DBSTest::createWithName( "SaveOnly:" . time() );
		$n->otherDecimal = 150;
		$n->add();
		
		$l = DBSTest::findWithName( $n->name );
		$this->assertEquals( 150, $l->decimal );
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
	
	function testNullAccess() {
		$n = DBSTest::createWithName( "NullGet" );
		$this->assertEquals( null, $n->nameRef );
		try {
			$q = $n->dateTime;
			$this->fail();
		} catch( DBS_FieldException $ex ) {
			$this->assertEquals( DBS_FieldException::UNAVAILABLE, $ex->getCode() );
		}
	}
	
	function testNullSaveLoad() {
		$n = DBSTest::createWithName( "NullAdd" );
		$n->nullStr = null;
		$this->assertNull( $n->nullStr );
		$n->add();
		 
		 $l = DBSTest::findWithID( $n->id );
		 $this->assertNull( $l->nullStr );
	
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
		$this->assertTrue( $q->__isDirty( 'float' ) );
		$q->add();
		$this->assertFalse( $q->__isDirty( 'float' ) );
		
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
		$d->delete();	//TODO: syntax error in postgres, yet it deletes anyways?
		
		try {
			$l = DBSTest::findWithName( $q->name );
			$this->assertTrue( false );
		} catch( DBS_DBException $ex ) {
			$this->assertEquals( DBS_DBException::NOT_IN_DB, $ex->getCode() );
		}
	}
	
	function testSearch() {
		//unsure an unusual DB order to guarantee sorting is actually doing something
		$nums = range( 1, 10 );
		shuffle( $nums );
		for( $i = 0; $i < 10; $i++ ) {
			$val = $nums[$i];	
			$q = DBSTest::createWithName( "Search:$val" );
			$q->decimal = $val;
			$q->bool = true;
			$q->float = 25;
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
			
		//multi-field sort
		$ordered = DBSTest::search( 
			DBS_Query::matchStringPattern( 'name', 'Search:*' ),
			DBS_Query::sort( 
				array( 'float' , 'decimal' ), 	//float will be effectively ignored as they are all equal
				array( DBS_Query::SORT_DESC, DBS_Query::SORT_ASC )
				)
			)->loadAll();
		for( $i = 1; $i <= 10; $i++ )
			$this->assertEquals( $i, $ordered[$i-1]->decimal );
			
		//non-keyed sort, though direct value load
		$ordered = SortSearch::search()->loadAll( null, 'decimal' );
		for( $i = 1; $i <= 10; $i++ )
			$this->assertEquals( $i, $ordered[$i-1] );
		
		//keyed (use Scheme search)
		$ordered = KeySortSearch::search()->loadAll( 'decimal' );
		for( $i = 1; $i <= 10; $i++ )
			$this->assertEquals( $i, $ordered[$i]->decimal );
			
		//multi-sort (on Name after decimal)
		$nums = range( 1, 10 );
		shuffle( $nums );
		for( $i = 0; $i < 10; $i++ ) {
			$val = $nums[$i];	
			$q = DBSTest::createWithName( "Search:Z$val" );
			$q->decimal = $val;
			$q->bool = false;
			$q->add();
		}
		
		$ordered = MultiSortSearch::search()->loadAll();
		for( $i = 1; $i <= 10; $i++ ) {
			$this->assertEquals( $i, $ordered[2*($i-1)]->decimal );
			$this->assertTrue( $ordered[2*($i-1)]->bool );
			$this->assertEquals( $i, $ordered[2*($i-1)+1]->decimal );
			$this->assertFalse( $ordered[2*($i-1)+1]->bool );
		}
		
		$many = ManyField::search( true, 25, false, 7 )->loadAll();
		$this->assertEquals( 11, count( $many ) );
		
		
		//test delete
		DBSTest::searchAndDelete( DBS_Query::matchStringPattern( 'name', 'Search:*' ) );
		$this->assertEquals( 0, count( DBSTest::search( DBS_Query::matchStringPattern( 'name', 'Search:*' ) )->loadAll() ) );
		
		//empty in
		$this->assertEquals( 0, count( DBSTest::search( DBS_Query::matchIn( 'name', array() ) )->loadAll() ) );
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
			$this->fail();
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
			$this->fail();
		} catch( DBS_FieldException $e ) {
			$this->assertEquals( DBS_FieldException::SAVE_LOAD_ONLY, $e->getCode() );
			$this->assertEquals( 'id', $e->field );
		}
		
		//also test via searching, since it uses an alternate load mechanism
		$allq = DBSTest::search( DBS_Query::match( 'name', 'Yet Newer' ) )->loadAll();
		$q = $allq[0];
		$q->name = 'Again Newer';
		$q->decimal = 12345;
		$q->save();
		
		$n = DBSTest::findWithID( $id );
		$this->assertEquals( 'Again Newer', $n->name );
		
		//okay, check case of attempting to save a value from incomplete search
		$allq = DBSTest::search( DBS_Query::match( 'decimal', 12345 ), DBS_Query::fieldLimit( 'decimal' ) )->loadAll();
		$q = $allq[0];
		$q->decimal = 12;
		try {
			$q->save();
			$this->fail();
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
			$n = DBSTwoKeys::createWithName_Num( $d[1], $d[0] );
			$n->value = $d[2];
			$n->add();
		}
		
		$this->assertEquals( "ABC", DBSTwoKeys::findWithName_Num( "A",1 )->value );
		$this->assertEquals( "DCB", DBSTwoKeys::findWithName_Num( "B", 2  )->value );
		
		//finding by just one part of a key is forbidden
		$j = DBSTwoKeys::withNothing();
		$j->num = 2;
		try {
		 	$j->find();
		 	$this->fail();
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
	
	function testFailOnBrokenKey() {
		$bk = BrokenKey::createWithNothing();
		$bk->name = "Some Name" . time();
		$bk->add();
		$this->assertTrue( $bk->id > 0 );
		
		$nbk = BrokenKey::createWithNothing();
		$nbk->name = $bk->name;
		try {
			$nbk->add();
			$this->fail();
		} catch( DBS_DBException $ex ) {
			$this->assertEquals( DBS_DBException::SAVE_FAILED, $ex->getCode() );
		}
	}
	
	function testNullKey() {
		$q = NullKey::createWithNothing();
		$q->decimal = 10;
		$q->add();
		$this->assertTrue( $q->id > 0 );
		
		$q->decimal++;
		$q->save();
		
		$this->assertEquals( 11, $q->decimal );
		
		$q->name = "nullkey" . time();
		$q->save();
		
		//test when we set an explicit default of null (to match on null values in keys)
		$q = NullKey2::createWithNothing();
		$q->decimal = 10;
		$q->add();
		$q->decimal++;
		$q->save();
	}
	
	function testFindNullKey() {
		try {
			//this exercises an unusual case with Default values in a load key
			$q = NullKey2::findWithID( 0 );	//doesn't exist
			$this->fail();
		} catch( DBS_DBException $ex ) {
			$this->assertEquals( DBS_DBException::NOT_IN_DB, $ex->getCode() );
		}
	}
	
	function testNonSaves() {
		$q = NullKey::createWithNothing();
		try {
			$q->add();
			$this->fail();
		} catch( DBS_DBException $ex ) {
			$this->assertEquals( DBS_DBException::SAVE_ZERO_FIELDS, $ex->getCode() );
		}
		
		//in this case some defaults exist, thus add will work
		$q = DBSTest::createWithNothing();
		$q->add();
		//though save must fail
		try {
			$q->save();
			$this->fail();
		} catch( DBS_DBException $ex ) {
			$this->assertEquals( DBS_DBException::SAVE_ZERO_FIELDS, $ex->getCode() );
		}
	}
	
	function testLinkNames() {
		$a = DBSName::createWithID( 1001 );
		$a->name = 'One';
		$a->add();
		
		$b = DBSName::createWithID( 1002 );
		$b->name = 'Two';
		$b->add();
		
		$q = DBSLinkNames::createWithNothing();
		$q->left = $a;
		$q->right = $b;
		$q->value = 123;
		$q->add();
		
		$l = DBSLinkNames::withIdentifier( $q->getIdentifier() );
		$l->find();
		$this->assertEquals( 123, $l->value );
	}
	
	function testInclTwoKeys() {
		$master = DBSTest::createWithName( "Linking Test" );
		$master->decimal = 2;
		$master->add();
		
		for( $i = 0; $i < 5; $i ++ ) {
			$o = BasicTwoKeys::createWithNothing();
			$o->master = $master;
			$o->value = "$i";
			$o->add();
		}
		
		//the outer search should return the same results
		$i = 0;
		foreach( InclBasicTwoKeys::search( $master ) as $o ) {
			$this->assertEquals( "$i", $o->value );
			$i++;
		}
		$this->assertEquals( 5, $i );
		
		$i = 0;
		foreach( $master->twoKeys() as $o ) {
			$this->assertEquals( "$i", $o->value );
			$i++;
		}
		$this->assertEquals( 5, $i );
		
		//to show that placeholders still work
		$f = $master->twoKeysValue( 3 )->loadAll();
		$this->assertEquals( 1, count( $f ) );
		$this->assertEquals( 3, $f[0]->value );
		
		//test references to other members (Decimal = 2 match to Value)
		$f = $master->twoKeysMatching()->loadAll();
		$this->assertEquals( 1, count( $f ) );
		$this->assertEquals( 2, $f[0]->value );
	}
	
	function testMerge() {
		//simple in memory ops
		$s = SimpleMerge::withNothing();
		$s->decimal = 10;
		$this->assertEquals( 10, $s->decimal );
		$s->name = "hello";
		$this->assertEquals( "hello", $s->name );
		
		//simple add
		$s = SimpleMerge::createWithNothing();
		$s->name = "meme";
		$s->add();
		
		//and then a save
		$s->decimal = 57;
		$s->save();
		
		//now try to load it
		$l = SimpleMerge::findWithNameID( $s->nameID );
		$this->assertEquals( 57, $l->decimal );
		$this->assertEquals( "meme", $l->name );
		
		//load by name...
		$l = SimpleMerge::findWithName( "meme" );
		$this->assertEquals( 57, $l->decimal );
		
		//lazy load by id
		$l = SimpleMerge::withNameID( $s->nameID );
		$this->assertEquals( "meme", $l->name );
		$this->assertEquals( 57, $l->decimal );
		
		//lazy load by name (this will test the backloading)
		$l = SimpleMerge::withName( "meme" );
		$this->assertEquals( 57, $l->decimal );	//very importnat to test this before looking up the NameID!
		
		
		# TODO: multi-level loading A requires B which requires C
		# TODO: multi-named values
	}
	
	function testBadTypes() {
		try {
			DBSTest::findWithName( new Date( 123 ) );
			$this->assertTrue( false );
		} catch( DBS_SetFieldException $e ) {
			$this->assertEquals( DBS_SetFieldException::TYPE_STRING, $e->getType() );
		}
		
		try {
			DBSTest::search( DBS_Query::match( 'decimal', 'badtype' ) );
			$this->assertTrue( false );
		} catch( DBS_SetFieldException $e ) {
			$this->assertEquals( DBS_SetFieldException::TYPE_NUMERIC, $e->getType() );
		}
	}
	
}
?>