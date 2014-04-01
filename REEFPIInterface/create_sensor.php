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

<?PHP
if(isset($_POST['addSensor']))
{
	$sensorName = ($_POST['sensorName']);
	$sensorType = (int)($_POST['sensorTypes']);
	$address = ($_POST['address']);
	$units = ($_POST['units']);
	$period = (int)($_POST['period']);
	echo $sensorName;
	$addDevice = mysqli_query($con, "INSERT INTO sensor (sensorName, idsensorType, address, units, period) 
									VALUES ('$sensorName', '$sensorType', '$address', '$units', '$period')
									")or die(mysqli_error($con));
	$result = ($addDevice);
}
?>

<form method="post" action="<?php $_PHP_SELF ?>">
	<table width="400" border="0" cellspacing="1" cellpadding="2">
		<tr>
			<td width="100">Sensor Name</td>
			<td><input name="sensorName" type="text" id="sensorName"></td>
		</tr>
		<tr>
			<td width="100">Sensor Type ID</td>
			<td>
				<select name="sensorTypes" id="sensorTypes" style="width: 200px" >
   	   				<?php
   	   					$idsensorTypes= mysqli_query($con, 'select * from sensorType') or die (mysql_error()); 
       
      					while($sensorsType = mysqli_fetch_array($idsensorTypes))
      					{
        					echo "<option value=".$sensorsType['idsensorType']."> ".$sensorsType['sensorTypeName']." </option>";
      					}
      				?>
				</select>
			</td>
		</tr>
		<tr>
			<td width="100">Address</td>
			<td><input name="address" type="text" id="address"></td>
		</tr>
		<tr>
			<td width="100">Units</td>
			<td><input name="units" type="text" id="units"></td>
		</tr>
		<tr>
			<td width="100">Period</td>
			<td><input name="period" type="text" id="period"></td>
		</tr>		
		<tr>
			<td width="100"> </td>
			<td>
				<input name="addSensor" type="submit" id="addSensor" value="Add Sensor">
			</td>
		</tr>
	</table>
</form>


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
