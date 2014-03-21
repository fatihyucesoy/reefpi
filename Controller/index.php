<html>
<header>
<title>ReefPi</title>
</header>
<body>
<?php
            $mysqlserver="localhost";
            $mysqlusername="root";
            $mysqlpassword="root";
            $dbname = 'reefpi_rpi_schema';			
            $con=mysqli_connect("$mysqlserver", "$mysqlusername", "$mysqlpassword", "$dbname");
			
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
</body>
</html>
