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
Schedule Types
</p>

<?php
	$resultScheduleTypes = mysqli_query($con, "SELECT * FROM scheduleType");

	if($resultScheduleTypes){
	echo "<table border='1'>
	<tr>
		<th>ID</th>
		<th>Schedule Type Name</th>
		<th>Description</th>
	</tr>";

			while($rowScheduleType = mysqli_fetch_array($resultScheduleTypes))
				{
					echo "<tr>";
					echo "<td>" . $rowScheduleType['idscheduleType'] . "</td>";
					echo "<td>" . $rowScheduleType['scheduleTypeName'] . "</td>";
					echo "<td>" . $rowScheduleType['Description'] . "</td>";	
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



<div id="footer">
	<p> <a href="#">REEFPI</a></p>
</div> <!-- end #footer -->

		</div> <!-- End #wrapper -->

	</body>

</html>
