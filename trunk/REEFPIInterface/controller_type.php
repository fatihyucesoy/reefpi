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
Controller Types
</p>

<h3>List of controllers</h3>
<?php
			$resultControllerTypes = mysqli_query($con, "SELECT * FROM controllerType");

		echo "<table border='1'>
	<tr>
		<th>Name</th>
		<th>Description</th>
	</tr>";

			while($rowControllerType = mysqli_fetch_array($resultControllerTypes))
				{
					echo "<tr>";
					echo "<td>" . $rowControllerType['controllerTypeName'] . "</td>";
					echo "<td>" . $rowControllerType['controllerTypeDescription'] . "</td>";
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
