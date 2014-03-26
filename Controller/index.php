<html>
<header>
<title>ReefPi</title>
</header>
<body>
<?php
            $mysqlserver="127.0.0.1";
            $mysqlusername="root";
            $mysqlpassword="root";
            $dbname = 'reefpi_rpi_schema';
            $con=mysqli_connect("$mysqlserver", "$mysqlusername", "$mysqlpassword","$dbname");

						if (mysqli_connect_errno())
	{
		echo "Failed to connect to MySQL: " . mysqli_connect_error();
	}
?>
<h3>LED Temperature Reading</h3>
<?php
			$resultReadingLED = mysqli_query($con,"SELECT * FROM sensorreadings
				WHERE sensorId=(SELECT idsensors from sensors
					WHERE sensorID = 'tempSensor1')
						ORDER BY timeStamp DESC limit 1");

		echo "<table border='1'>
	<tr>
		<th>Reading</th>
	</tr>";

			while($rowLED = mysqli_fetch_array($resultReadingLED))
				{
					echo "<tr>";
					echo "<td>" . $rowLED['reading'] . "</td>";
					echo "</tr>";
				}
		echo "</table>";

?>
<h3>List of used devices</h3>
<?php
			$resultUsedDevices = mysqli_query($con, "SELECT * FROM devices WHERE status=1");

		echo "<table border='1'>
	<tr>
		<th>Device Name</th>
		<th>Address</th>
		<th>Status</th>
	</tr>";

			while($rowDevice = mysqli_fetch_array($resultUsedDevices))
				{
					echo "<tr>";
					echo "<td>" . $rowDevice['Name'] . "</td>";
					echo "<td>" . $rowDevice['address'] . "</td>";
					echo "<td>" . $rowDevice['status'] . "</td>";
					echo "</tr>";
				}
		echo "</table>"
?>
<h3>List of available devices</h3>
<?php
			$resultAvailableDevices = mysqli_query($con, "SELECT * FROM devices");

		echo "<table border='1'>
	<tr>
		<th>Device Name</th>
		<th>Address</th>
		<th>Status</th>
	</tr>";

			while($rowAvailableDevice = mysqli_fetch_array($resultAvailableDevices))
				{
					echo "<tr>";
					echo "<td>" . $rowAvailableDevice['Name'] . "</td>";
					echo "<td>" . $rowAvailableDevice['address'] . "</td>";
					echo "<td>" . $rowAvailableDevice['status'] . "</td>";
					echo "</tr>";
				}
		echo "</table>"
?>
<h3>List of controllers</h3>
<?php
			$resultAvailableController = mysqli_query($con, "SELECT * FROM controller");

		echo "<table border='1'>
	<tr>
		<th>Controller Name</th>
		<th>Description</th>
	</tr>";

			while($rowAvailableController = mysqli_fetch_array($resultAvailableController))
				{
					echo "<tr>";
					echo "<td>" . $rowAvailableController['Name'] . "</td>";
					echo "<td>" . $rowAvailableController['description'] . "</td>";
					echo "</tr>";
				}
		echo "</table>"
?>
<?PHP
if(isset($_POST['add']))
{
$db_found = mysql_select_db($con);

$deviceName = ($_POST['deviceName']);
$busType = ($_POST['busType']);

if ($db_found) {

$SQL = "INSERT INTO devicetype ".
"(deviceName, busType)". 
"VALUES ('$deviceName', '$busType')";
	
	$result = mysql_query($SQL);

print "The device has been added to the database";
mysql_close( $db_handle );

}
else {

print "Sorry, the Database cannot be Found";
mysql_close( $db_handle );

}
}
else
{
?>
<p></p>
<h3>Adding a Device Type</h3>
<form method="post" action="<?php $_PHP_SELF ?>">
<table width="400" border="0" cellspacing="1" cellpadding="2">
<tr>
<td width="100">Device Name</td>
<td><input name="deviceName" type="text" id="name"></td>
</tr>
<tr>
<td width="100">Bus Type</td>
<td><input name="busType" type="text" id="type"></td>
</tr>
<tr>
<td width="100"> </td>
<td>
<input name="add" type="submit" id="add" value="Add Device">
</td>
</tr>
</table>
</form>
<?php
}
?>
</body>
</html>
