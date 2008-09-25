<?php

/**
 * The purpose of this test is just to ensure that using the MDB2 source directly
 * works. Only the most basic tests are required since MDB2 is actually wrapped,
 * and that is tested in the main tests.
 */
class DBSTest_DirectMDB2 extends TestCase {
	function testSomething()	{
		$q = MDBSTest::createWithName( "Hello" . time() );
		$q->add();
		
		$l = MDBSTest::findWithID( $q->id );
		$this->assertEquals( $q->name, $l->name );
	}
}

?>
