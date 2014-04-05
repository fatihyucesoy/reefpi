<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">

<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">

<head>

<meta http-equiv="content-type" content="text/html; charset=utf-8" />

<meta name="description" content="" />

<meta name="keywords" content="" />

<meta name="author" content="" />

<link rel="stylesheet" type="text/css" href="style.css" media="screen" />

<title>ReefPi Define Sensor Actions</title>

</head>

	<body>

		<div id="wrapper">

<?php include('includes/header.php'); ?>

<?php include('includes/nav.php'); ?>

<?php include('includes/dbconnect.php'); ?>


<div id="content">


<p>
Defined Sensor Actions
</p>
<?php
	$resultSensorTypes = mysqli_query($con, "SELECT * FROM sensorAction AS SA
												INNER JOIN sensor AS S ON SA.idsensor = S.idsensor
												INNER JOIN device AS D ON SA.iddevice = D.iddevice
												INNER JOIN deviceCommand AS DC ON SA.iddeviceCommand = DC.iddeviceCommand");

	echo "<table border='1'>
	<tr>
		<th>Sensor Name</th>
		<th>device</th>
		<th>command</th>
		<th>type</th>
		<th>condition</th>
		<th>value</th>
		<th>units</th>
	</tr>";

	while($rowSensorType = mysqli_fetch_array($resultSensorTypes))
	{
		echo "<tr>";
		echo "<td>" . $rowSensorType['sensorName'] . "</td>";
		echo "<td>" . $rowSensorType['deviceName'] . "</td>";
		echo "<td>" . $rowSensorType['deviceCommand'] . "</td>";
		echo "<td>" . $rowSensorType['type'] . "</td>";
		echo "<td>" . $rowSensorType['relation'] . "</td>";
		echo "<td>" . $rowSensorType['value'] . "</td>";
		echo "<td>" . $rowSensorType['units'] . "</td>";
		echo "</tr>";
	}
	echo "</table>"
?>
<p>
Add a Sensor Action
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

if(isset($_POST['addSensorAction']))
{
	$idsensor 			= ($_POST['idsensor']);
	$type 				= ($_POST['type']);
	$relation 			= ($_POST['relation']);
	$value 				= ($_POST['value']);	
	$iddevice 			= ($_POST['iddevice']);
	$iddeviceCommand 	= ($_POST['iddeviceCommand']);
	$query				="INSERT INTO sensorAction 
							(idsensor, value, idsensorActionRelation, idsensorActionType, iddevice, iddeviceCommand)	
							VALUES 
							($idsensor, '$value', '$relation', '$type', $iddevice, $iddeviceCommand)";
	$addSensorAction 	= mysqli_query($con, $query);
	$result = ($addSensorAction);
		if(!$result)
		{
			echo "Sorry, cannot submit your request";
			die(mysqli_error($con));
		}
		else
		{
			redirect($_SERVER['PHP_SELF']);
		}
	
	unset($_POST['addSensorAction']);
}
?>

<form method="post" action="<?php $_PHP_SELF ?>">
	<table width="400" border="0" cellspacing="1" cellpadding="2">
		<tr>
			<td width="200">Sensor</td>
			<td>
				<select name="idsensor" id="idsensor" style="width: 200px" >
   	   				<?php
   	   					$sensors= mysqli_query($con, 'SELECT * FROM sensor') or die (mysql_error());    
      					while($sensor = mysqli_fetch_array($sensors))
      					{
        					echo "<option value=".$sensor['idsensor']."> ".$sensor['sensorName']." </option>";
      					}
      				?>
				</select>
			</td>
		</tr>
		<tr>
			<td width="200">Type</td>
			<td>
				<select name="type" id="type" style="width: 200px" >
   	   				<?php
   	   					$sensors= mysqli_query($con, 'SELECT * FROM sensorActionType') or die (mysql_error());    
      					while($sensor = mysqli_fetch_array($sensors))
      					{
        					echo "<option value=".$sensor['idsensorActionType']."> ".$sensor['sensorActionType']." </option>";
      					}
      				?>
				</select>
			</td>
		</tr>
		<tr>
			<td width="200">Relation</td>
			<td><input name="relation" type="text" id="relation"></td>
		</tr>
		<tr>
			<td width="200">value</td>
			<td><input name="value" type="text" id="value"></td>
		</tr>
		<tr>
			<td width="200">device</td>
			<td>
				<select name="iddevice" id="iddevice" style="width: 200px" >
   	   				<?php
   	   					$sensors= mysqli_query($con, 'SELECT * FROM device') or die (mysql_error());    
      					while($sensor = mysqli_fetch_array($sensors))
      					{
        					echo "<option value=".$sensor['iddevice']."> ".$sensor['deviceName']." </option>";
      					}
      				?>
				</select>
			</td>
		</tr>
		<tr>
			<td width="200">command</td>
			<td>
				<select name="iddeviceCommand" id="iddeviceCommand" style="width: 200px" >
   	   				<?php
   	   					$sensors= mysqli_query($con, 'SELECT * FROM deviceCommand') or die (mysql_error());    
      					while($sensor = mysqli_fetch_array($sensors))
      					{
        					echo "<option value=".$sensor['iddeviceCommand']."> ".$sensor['deviceCommand']." </option>";
      					}
      				?>
				</select>
			</td>
		</tr>
		<tr>
			<td width="100"> </td>
			<td>
				<input name="addSensorAction" type="submit" id="addSensorAction" value="addSensorAction">
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
