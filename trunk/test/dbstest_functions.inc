<?php

class DBSTest_Functions extends TestCase {
	function testExport() {
		$n = DBSTest::createWithNothing();
		$n->id = 12345;	//force this for our tests
		$n->name = 'T❀stNäm€' . time();	//include some unicode, latin-1, and latin-15 overlap characters
		
		# Create a date outside the 32-bit int range (to ensure proper Date support)
		$date = new DateTime();
		$date->setDate( rand( 2500, 5000 ), rand( 1, 12 ), rand( 1, 28 ) );
		$date->setTime( rand( 0, 24 ), rand( 0, 60 ), rand( 0, 60 ) );
		$n->date = $date;
		if( TestLimit::$time24H )
			$n->time = rand( 0, 3600*24 );	//some DB's are limited to 24H
		else
			$n->time = rand( -100000, 100000 );	//be sure to have negatives tested as well
		$dateTime = new DateTime();
		$dateTime->setDate( rand( 1, 1000 ), rand( 1, 12 ), rand( 1, 28 ) );
		$n->dateTime = $dateTime;
		$n->decimal = rand( 0, 100000 ) / 1000.0;
		$n->float = rand() / getrandmax();
		$n->memoryOnly = 1234;	//value will just be lost on reload (nothing really to test, perhaps when caching is introduced)
		
		$export = export_entity( $n );
		
		$this->assertEquals( $n->name, $export['Name'] );
		$this->assertEquals( $n->float, $export['Float'] );
		
		$import = import_entity( 'DBSTest', $export );
		$this->assertEquals( $n->name, $import->name );
		$this->assertEquals( $n->float, $import->float );
		$this->assertNull( $n->nameRef );
		$this->assertEquals( $n->dateTime->format( DateTime::ISO8601 ), $import->dateTime->format( DateTime::ISO8601 ) );
		$this->assertEquals( $n->memoryOnly, $import->memoryOnly );
		$this->assertEquals( $n->id, $import->id );
		
		//try one with linking
		$to = DBSLink::withNothing();
		$to->basic = $n;
		
		$export = export_entity( $to );
		$this->assertEquals( $n->identifier, $export['Basic'] );
		
		$import = import_entity( 'DBSLink', $export );
		$this->assertEquals( $to->basic->id, $import->basic->id );
		$this->assertEquals( $to->basic->name, $import->basic->name );	//we know our ID includes the name
		$this->assertFalse( $import->basic->__has( 'memoryOnly' ) );	//not part of ID (no default)
		
		$export = export_entity( $to, 1 );
		$this->assertEquals( $n->name, $export['Basic']['Name'] );
		
		$import = import_entity( 'DBSLink', $export );
		$this->assertEquals( $to->basic->id, $import->basic->id );
		$this->assertEquals( $to->basic->name, $import->basic->name );
		$this->assertEquals( $to->basic->float, $import->basic->float );
	}
}

?>
