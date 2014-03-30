<?php
            $mysqlserver="127.0.0.1";
            $mysqlusername="root";
            $mysqlpassword="";
            $dbname = 'reefpi_rpi_schema';
            $con=mysqli_connect("$mysqlserver", "$mysqlusername", "$mysqlpassword","$dbname");

						if (mysqli_connect_errno())
	{
		echo "Failed to connect to MySQL: " . mysqli_connect_error();
	}
?>