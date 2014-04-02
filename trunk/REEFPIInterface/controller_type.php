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
<p>
Create Controller Types
</p>

<?PHP
if(isset($_POST['addDeviceType']))
{
	$controllerTypeName = ($_POST['controllerTypeName']);
	$description = ($_POST['controllerTypeDescription']);
	$addDeviceType = mysqli_query($con, "INSERT INTO controllertype ". "(controllerTypeName, controllerTypeDescription)". "VALUES ('$controllerTypeName', '$description')");
		$result = ($addDeviceType);
		if(!$result)
		echo "Sorry, cannot submit your request";
	else
		{
		header("Location: ".$_SERVER['REQUEST_URI']); //which will just reload the page
		}
}
?>

<form method="post" action="<?php $_PHP_SELF ?>">
	<table width="400" border="0" cellspacing="1" cellpadding="2">
		<tr>
			<td width="100">Controller Type Name</td>
			<td><input name="controllerTypeName" type="text" id="name"></td>
		</tr>
		<tr>
			<td width="100">Description</td>
			<td><input name="controllerTypeDescription" type="text" id="type"></td>
		</tr>
		<tr>
			<td width="100"> </td>
			<td>
				<input name="addDeviceType" type="submit" id="addDeviceType" value="Add Controller Type">
			</td>
		</tr>
	</table>
</form>

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
