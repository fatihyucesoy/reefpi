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
Create Controller
</p>

<?PHP
if(isset($_POST['addDevices']))
{
	$Name = ($_POST['Name']);
	$idcontrollerType = ($_POST['controllerType']);
	$description = ($_POST['description']);
	$addDevice = mysqli_query($con, "INSERT INTO controller ". "(Name, description, idcontrollerType)". "VALUES ('$Name', '$description', $idcontrollerType)");
	$result = ($addDevice);
}
?>

<form method="post" action="<?php $_PHP_SELF ?>">
	<table width="400" border="0" cellspacing="1" cellpadding="2">
		<tr>
			<td width="100">Name</td>
			<td><input name="Name" type="text" id="Name"></td>
		</tr>
		<tr>
			<td width="100">Controller Type ID</td>
			<td>
				<select name="controllerType" id="controllerType" style="width: 200px" >
   	   				<?php
   	   					$controllerTypes= mysqli_query($con, 'select * from controllerType') or die (mysql_error()); 
       
      					while($controllerType = mysqli_fetch_array($controllerTypes))
      					{
        					echo "<option value=".$conrollerType['idcontrollerType']."> ".$controllerType['name']." </option>";
      					}
      				?>
				</select>
			</td>
		</tr>
		<tr>
			<td width="100">Description</td>
			<td><input name="description" type="text" id="description"></td>
		</tr>
		<tr>
			<td width="100"> </td>
			<td>
				<input name="addDevices" type="submit" id="addDevices" value="addDevices">
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
