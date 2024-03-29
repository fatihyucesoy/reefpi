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
Available Controllers
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
<p>
Add a Controller
</p>
<?PHP
function redirect($url) {
    if(!headers_sent()) {
        //If headers not sent yet... then do php redirect
        header('Location: '.$url);
        exit;
    } else {
        //If headers are sent... do javascript redirect... if javascript disabled, do html redirect.
        echo '<script type="text/javascript">';
        echo 'window.location.href="'.$url.'";';
        echo '</script>';
        echo '<noscript>';
        echo '<meta http-equiv="refresh" content="0;url='.$url.'" />';
        echo '</noscript>';
        exit;
    }
}

if(isset($_POST['addDevices']))
{
	$Name = ($_POST['Name']);
	$idcontrollerType = ($_POST['controllerType']);
	$description = ($_POST['description']);
	$addDevice = mysqli_query($con, "INSERT INTO controller ". "(controllerName, controllerdescription, idcontrollerType)". "VALUES ('$Name', '$description', $idcontrollerType)");
	$result = ($addDevice);
	if(!$result)
	{
		echo ("Sorry, cannot submit your request: ". mysqli_error($con));
	}
	else
	{
		redirect($_SERVER['PHP_SELF']);
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
			<td width="100">Controller Type ID</td>
			<td>
				<select name="controllerType" id="controllerType" style="width: 200px" >
   	   				<?php
   	   					$controllerTypes= mysqli_query($con, 'select * from controllerType') or die (mysql_error()); 
       
      					while($controllerType = mysqli_fetch_array($controllerTypes))
      					{
        					echo "<option value=".$controllerType['idcontrollerType']."> ".$controllerType['controllerTypeName']." </option>";
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
	<p><a href="#">REEFPI</a></p>
</div> <!-- end #footer -->

		</div> <!-- End #wrapper -->

	</body>

</html>
