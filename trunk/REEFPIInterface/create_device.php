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
Create Device
</p>

<?PHP
if(isset($_POST['addDevices']))
{
	$Name = ($_POST['Name']);
	$iddeviceType = ($_POST['deviceType']);
	$address = ($_POST['address']);
	$status = ($_POST['status']);
	$addDevice = mysqli_query($con, "INSERT INTO devices ". "(Name, iddeviceType, address, status)". "VALUES ('$Name', '$iddeviceType', '$address', $status)");
	$result = ($addDevice);
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
			<td width="100">Name</td>
			<td><input name="Name" type="text" id="Name"></td>
		</tr>
		<tr>
			<td width="100">Device Type ID</td>
			<td>
				<select name="deviceType" id="deviceType" style="width: 200px" >
   	   				<?php
   	   					$deviceTypes= mysqli_query($con, 'select * from deviceType') or die (mysql_error()); 
       
      					while($deviceType = mysqli_fetch_array($deviceTypes))
      					{
        					echo "<option value=".$deviceType['iddeviceType']."> ".$deviceType['deviceName']." </option>";
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
			<td width="100">Status</td>
			<td><input name="status" type="text" id="status"></td>
		</tr>		
		<tr>
			<td width="100"> </td>
			<td>
				<input name="addDevices" type="submit" id="addDevices" value="Add Device">
			</td>
		</tr>
	</table>
</form>


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
