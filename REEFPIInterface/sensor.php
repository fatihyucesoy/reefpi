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
			$resultControllerTypes = mysqli_query($con, 'SELECT * FROM sensors AS S INNER JOIN devices AS D ON S.device = D.iddevices INNER JOIN sensorType AS ST ON S.idsensorType = ST.idsensorType');

		echo "<table border='1'>
	<tr>
		<th>SName</th>
		<th>Type</th>
		<th>address</th>
		<th>sample period</th>
		<th>Device</th>
		<th>state</th>
		<th>lower limit</th>
		<th>Upper Limit</th>
	</tr>";

			while($rowControllerType = mysqli_fetch_array($resultControllerTypes))
				{
					echo "<tr>";
					echo "<td>" . $rowControllerType['sensorId'] . "</td>";
					echo "<td>" . $rowControllerType['sensorName'] . "</td>";
					echo "<td>" . $rowControllerType['address'] . "</td>";
					echo "<td>" . $rowControllerType['period'] . "</td>";
					echo "<td>" . $rowControllerType['Name'] . "</td>";
					echo "<td>" . $rowControllerType['state'] . "</td>";
					echo "<td>" . $rowControllerType['lowerLimit'] . "</td>";
					echo "<td>" . $rowControllerType['upperLimit'] . "</td>";
					
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
