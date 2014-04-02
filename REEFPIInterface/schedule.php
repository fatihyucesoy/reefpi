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
Current Scheduled Events
</p>

<?php
	$resultControllerTypes = mysqli_query($con, "SELECT * FROM scheduledEvent AS SE inner JOIN device AS D ON SE.iddevice = D.iddevice");

	if($resultControllerTypes){
	echo "<table border='1'>
	<tr>
		<th>Job Name</th>
		<th>Job type</th>
		<th>device</th>
		<th>command</th>
		<th>value</th>
		<th>startDate</th>
		<th>year</th>
		<th>month</th>
		<th>day</th>
		<th>week</th>
		<th>day of week</th>
		<th>hour</th>
		<th>minute</th>
		<th>second</th>
	</tr>";

			while($rowControllerType = mysqli_fetch_array($resultControllerTypes))
				{
					echo "<tr>";
					echo "<td>" . $rowControllerType['jobName'] . "</td>";
					echo "<td>" . $rowControllerType['type'] . "</td>";
					echo "<td>" . $rowControllerType['deviceName'] . "</td>";
					echo "<td>" . $rowControllerType['command'] . "</td>";
					echo "<td>" . $rowControllerType['value'] . "</td>";
					echo "<td>" . $rowControllerType['startDate'] . "</td>";
					echo "<td>" . $rowControllerType['year'] . "</td>";
					echo "<td>" . $rowControllerType['month'] . "</td>";
					echo "<td>" . $rowControllerType['day'] . "</td>";
					echo "<td>" . $rowControllerType['week'] . "</td>";
					echo "<td>" . $rowControllerType['day_of_week'] . "</td>";
					echo "<td>" . $rowControllerType['hour'] . "</td>";
					echo "<td>" . $rowControllerType['minute'] . "</td>";
					echo "<td>" . $rowControllerType['second'] . "</td>";		
					echo "</tr>";
				}
		echo "</table>";
		}
		else
		{
			echo "failed to find any results";
		}
?>

<p>
Add a Scheduled Event
</p>

<?PHP
if(isset($_POST['addSchedule']))
{
	$jobName = ($_POST['jobName'])!="" ? ($_POST["'jobName'"]): 'NULL';
	$type = ($_POST['type'])!="" ? ($_POST["'type'"]): 'NULL';
	$iddevice = ($_POST['iddevice'])!="" ? ($_POST['iddevice']): 'NULL';
	$command = ($_POST['command'])!="" ? ($_POST["'command'"]): 'NULL';
	$value = ($_POST['value'])!="" ? ($_POST['value']): 'NULL';
	$startDate = ($_POST['startDate'])!="" ? ($_POST['startDate']): 'now()';
	$year = (int)($_POST['year'])!="" ? ($_POST['year']): 'NULL';
	$month = ($_POST['month'])!="" ? ($_POST['month']): 'NULL';
	$day = ($_POST['day'])!="" ? ($_POST['day']): 'NULL';
	$week = ($_POST['week'])!="" ? ($_POST['week']): 'NULL';
	$day_of_week = ($_POST['day_of_week'])!="" ? ($_POST['day_of_week']): 'NULL';
	$hour = ($_POST['hour'])!="" ? ($_POST['hour']): 'NULL';
	$minute = ($_POST['minute'])!="" ? ($_POST['minute']): 'NULL';
	$second = ($_POST['second'])!="" ? ($_POST['second']): 'NULL';
	
	$addScheduledEvent = mysqli_query($con, "INSERT INTO scheduledevent 
									(jobName, type, iddevice, command, value, startDate, 
									year, month, day, week, day_of_week, 
									hour, minute, second)VALUES ($jobName, $type, $iddevice, $command, $value, $startDate, 
									$year, $month, $day, $week, $day_of_week, $hour, $minute, $second)") or die(mysqli_error($con));
	$result = ($addScheduledEvent);
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
			<td width="100">Job Name</td>
			<td><input name="jobName" type="text" id="jobName"></td>
		</tr>
		<tr>
			<td width="100">Type</td>
			<td><input name="type" type="text" id="type"></td>
		</tr>
		<tr>
			<td width="100">Device ID</td>
			<td>
				<select name="iddevice" id="iddevice" style="width: 200px" >
   	   				<?php
   	   					$deviceTypes= mysqli_query($con, 'select * from device') or die (mysql_error()); 
       
      					while($deviceType = mysqli_fetch_array($deviceTypes))
      					{
        					echo "<option value=".$deviceType['iddevice']."> ".$deviceType['deviceName']." </option>";
      					}
      				?>
				</select>
			</td>
		</tr>
		<tr>
			<td width="100">Command</td>
			<td><input name="command" type="text" id="command"></td>
		</tr>
		<tr>
			<td width="100">Value</td>
			<td><input name="value" type="text" id="value"></td>
		</tr>
		<tr>
			<td width="100">Start Date</td>
			<td><input name="startDate" type="text" id="startDate"></td>
		</tr>
		<tr>
			<td width="100">Year</td>
			<td><input name="year" type="text" id="year"></td>
		</tr>	
		<tr>
			<td width="100">Month</td>
			<td><input name="month" type="text" id="month"></td>
		</tr>	
		<tr>
			<td width="100">Day</td>
			<td><input name="day" type="text" id="day"></td>
		</tr>
		<tr>
			<td width="100">Week</td>
			<td><input name="week" type="text" id="week"></td>
		</tr>	
		<tr>
			<td width="100">Day of Week</td>
			<td><input name="day_of_week" type="text" id="day_of_week"></td>
		</tr>		
		<tr>
			<td width="100">Hour</td>
			<td><input name="hour" type="text" id="hour"></td>
		</tr>	
		<tr>
			<td width="100">Minute</td>
			<td><input name="minute" type="text" id="minute"></td>
		</tr>	
		<tr>
			<td width="100">Second</td>
			<td><input name="second" type="text" id="second"></td>
		</tr>			
		<tr>
			<td width="100"> </td>
			<td>
				<input name="addSchedule" type="submit" id="addSchedule" value="addSchedule">
			</td>
		</tr>
	</table>
</form>





</div> <!-- end #content -->



<div id="footer">
	<p> <a href="#">REEFPI</a></p>
</div> <!-- end #footer -->

		</div> <!-- End #wrapper -->

	</body>

</html>
