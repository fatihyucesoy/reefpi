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
Scheduler
</p>

<?php
	$resultControllerTypes = mysqli_query($con, "SELECT * FROM scheduledEvent AS SE inner JOIN device AS D ON SE.iddevice = D.iddevice");

	if($resultControllerTypes){
	echo "<table border='1'>
	<tr>
		<th>Job Name</th>
		<th>Job type</th>
		<th>device</th>
		<th>state</th>
		<th>value</th>
		<th>startDate</th>
		<th>year</th>
		<th>month</th>
		<th>day</th>
		<th>week</th>
		<th>day of week</th>
		<th>hour</th>
		<th>minute</th>
		<th>second</th>
	</tr>";

			while($rowControllerType = mysqli_fetch_array($resultControllerTypes))
				{
					echo "<tr>";
					echo "<td>" . $rowControllerType['jobName'] . "</td>";
					echo "<td>" . $rowControllerType['type'] . "</td>";
					echo "<td>" . $rowControllerType['deviceName'] . "</td>";
					echo "<td>" . $rowControllerType['state'] . "</td>";
					echo "<td>" . $rowControllerType['value'] . "</td>";
					echo "<td>" . $rowControllerType['startDate'] . "</td>";
					echo "<td>" . $rowControllerType['year'] . "</td>";
					echo "<td>" . $rowControllerType['month'] . "</td>";
					echo "<td>" . $rowControllerType['day'] . "</td>";
					echo "<td>" . $rowControllerType['week'] . "</td>";
					echo "<td>" . $rowControllerType['day_of_week'] . "</td>";
					echo "<td>" . $rowControllerType['hour'] . "</td>";
					echo "<td>" . $rowControllerType['minute'] . "</td>";
					echo "<td>" . $rowControllerType['second'] . "</td>";		
					echo "</tr>";
				}
		echo "</table>";
		}
		else
		{
			echo "failed to find any results";
		}
?>







</div> <!-- end #content -->

<div id="sidebar">

<?php include('includes/sidebar.php'); ?>

</div> <!-- end #sidebar -->

<div id="footer">
	<p> <a href="#">REEFPI</a></p>
</div> <!-- end #footer -->

		</div> <!-- End #wrapper -->

	</body>

</html>
