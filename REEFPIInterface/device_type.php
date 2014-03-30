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
Device Types
</p>
<?php
			$resultDeviceTypes = mysqli_query($con, "SELECT * FROM deviceType");

		echo "<table border='1'>
	<tr>
		<th>Device type</th>
		<th>Bus Type</th>
	</tr>";

			while($rowDeviceType = mysqli_fetch_array($resultDeviceTypes))
				{
					echo "<tr>";
					echo "<td>" . $rowDeviceType['deviceTypeName'] . "</td>";
					echo "<td>" . $rowDeviceType['busType'] . "</td>";
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
