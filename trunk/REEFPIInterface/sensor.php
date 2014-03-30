<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">

<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">

<head>

<meta http-equiv="content-type" content="text/html; charset=utf-8" />

<meta name="description" content="" />

<meta name="keywords" content="" />

<meta name="author" content="" />

<link rel="stylesheet" type="text/css" href="style.css" media="screen" />

<title>REEFPI Home Page</title>

</head>

	<body>

		<div id="wrapper">

<?php include('includes/header.php'); ?>

<?php include('includes/nav.php'); ?>

<?php include('includes/dbconnect.php'); ?>

<div id="content">


<p>
Sensors
</p>
<?php
			$resultControllerTypes = mysqli_query($con, 'SELECT * FROM sensor INNER JOIN sensorType ON sensor.idsensorType = sensorType.idsensorType;');

		echo "<table border='1'>
	<tr>
		<th>ID Sensor</th>
		<th>Sensor Name</th>
		<th>Sensor Type Name</th>
		<th>Address</th>
		<th>Units</th>
		<th>Period</th>
	</tr>";

			while($rowControllerType = mysqli_fetch_array($resultControllerTypes))
				{
					echo "<tr>";
					echo "<td>" . $rowControllerType['Idsensor'] . "</td>";
					echo "<td>" . $rowControllerType['sensorName'] . "</td>";
					echo "<td>" . $rowControllerType['sensorTypeName'] . "</td>";
					echo "<td>" . $rowControllerType['address'] . "</td>";
					echo "<td>" . $rowControllerType['units'] . "</td>";
					echo "<td>" . $rowControllerType['period'] . "</td>";

					
					echo "</tr>";
				}
		echo "</table>"
?>


</div> <!-- end #content -->

<div id="sidebar">

<?php include('includes/sidebar.php'); ?>

</div> <!-- end #sidebar -->

<div id="footer">
	<p>Copyright &copy Bigguy 2014 <a href="#">REEFPI</a></p>
</div> <!-- end #footer -->

		</div> <!-- End #wrapper -->

	</body>

</html>
