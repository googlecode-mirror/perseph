<?php

//these functions make up for a lack of two fundamental conversions forgotten in PHP 5.2 and added in PHP 5.3
//they are obvisouly undefined if the date can't be expressed as a 32-bit int

function datetime_from_timestamp( $timestamp ) {
	return new DateTime( date( DATE_ISO8601, $timestamp ) );
}

function timestamp_from_datetime( DateTime $dt ) {
	return strtotime( $dt->format( DATE_ISO8601 ) );
}

?>