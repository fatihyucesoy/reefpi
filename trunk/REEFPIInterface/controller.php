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
Controller
</p>

<?php
			$resultAvailableController = mysqli_query($con, "SELECT * FROM controller 
				INNER JOIN controllerType ON controller.idcontrollerType = controllerType.idcontrollerType");

		echo "<table border='1'>
	<tr>
		<th>Name</th>
		<th>Type</th>
		<th>Description</th>
	</tr>";

			while($rowAvailableController = mysqli_fetch_array($resultAvailableController))
				{
					echo "<tr>";
					echo "<td>" . $rowAvailableController['controllerName'] . "</td>";
					echo "<td>" . $rowAvailableController['controllerTypeName'] . "</td>";
					echo "<td>" . $rowAvailableController['controllerDescription'] . "</td>";
					echo "</tr>";
				}
		echo "</table>"
?>

</div> <!-- end #content -->

<div id="sidebar">

<?php include('includes/sidebar.php'); ?>

</div> <!-- end #sidebar -->

<div id="footer">
	<p><a href="#">REEFPI</a></p>
</div> <!-- end #footer -->

		</div> <!-- End #wrapper -->

	</body>

</html>
