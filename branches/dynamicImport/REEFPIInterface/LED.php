<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">

<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">

<head>
	<meta http-equiv="content-type" content="text/html; charset=utf-8" />
	<meta name="description" content="" />

<meta name="keywords" content="" />

<meta name="author" content="" />

<link rel="stylesheet" type="text/css" href="style.css" media="screen" />


<?php include('includes/header.php'); ?>

<?php include('includes/nav.php'); ?>

<?php include('includes/dbconnect.php'); ?>

<?php
	date_default_timezone_set('Europe/London');
	$result = mysqli_query($con,"select * from (SELECT timeStamp, reading FROM sensorReadings 
				WHERE idsensor = (SELECT idsensor FROM sensor WHERE sensorName = 'tempSensor1') 
				ORDER BY timeStamp DESC LIMIT 100) 
				AS descArray ORDER BY descArray.timeStamp ASC;");
					
	$dataArray = array(array('timeStamp', 'reading'));
	$date = '';
	while($row = mysqli_fetch_array($result)) {
		$timestamp = DateTime::createFromFormat('Y-m-d H:i:s', $row['timeStamp']);
    	$dataArray[] = array($timestamp->format('H:i:s'), (float) $row['reading']);
    	$dateStamp = DateTime::createFromFormat('Y-m-d H:i:s', $row['timeStamp']);
		$date = $dateStamp->format('d:m:Y');
	}
	
?>



<!--Load the AJAX API-->

    <script type="text/javascript" src="https://www.google.com/jsapi"></script>
   	<script type="text/javascript">
   		google.load("jquery", "1.6.1");
      	google.load("visualization", "1", {packages:["corechart"]});
      	google.setOnLoadCallback(drawChart);
      	function drawChart(dataArray) {
        	var data = google.visualization.arrayToDataTable(<?php echo json_encode($dataArray); ?>);
        	var options = {
        		height : 400,
          		title: 'temperature',
          		is3d: true,
          		curveType: 'function',
          		explorer:{ actions: ['dragToZoom', 'rightClickToReset'] , axis: 'horizontal'},
          		vAxis: { title: "temperature", viewWindowMode:'explicit',viewWindow: {max:28.1,min:22.5} },
          		hAxis: { title: <?php echo json_encode($date); ?>, format: 'HH:mm'}
        	};
        var chart = new google.visualization.LineChart(document.getElementById('chart_div'));
        chart.draw(data, options);
      }
    </script>
    
<title>REEFPI Home Page</title>

</head>

	<body>

		<div id="wrapper">



<div id="content">

<p>

LED Page

</p>
<br>
<div id="chart_div"></div>
<br>

<select name="deviceType" id="deviceType" style="width: 200px" >
	<?php
		$sensors = mysqli_query($con, 'select * from sensor') or die (mysql_error());
		while($sensorType = mysqli_fetch_array($sensors))
		{
			echo "<option value=".$sensorType['idsensor']."> ".$sensorType['sensorName']." </option>";
		}
	?>
</select>
				
				
<h3>LED Temperature Reading</h3>
<?php
			$resultReadingLED = mysqli_query($con,"SELECT reading, timeStamp FROM sensorReadings 
					WHERE idsensor = (SELECT idsensor FROM sensor WHERE sensorName = 'tempSensor1') 
					ORDER BY timeStamp DESC 
					limit 1;");

		echo "<table border='1'>
	<tr>
		<th>Date</th>
		<th>Time</th>
		<th>Reading</th>
	</tr>";

			while($rowLED = mysqli_fetch_array($resultReadingLED))
				{
					$format = 'Y-m-d H:i:s';
					$timestamp = DateTime::createFromFormat($format, $rowLED['timeStamp']);					
					echo "<tr>";
					echo "<td>" . $timestamp->format('d:m:Y'). "</td>";
					echo "<td>" . $timestamp->format('H:i:s'). "</td>";
					echo "<td>" . $rowLED['reading'] . "</td>";
					echo "</tr>";
				}
		echo "</table>";
		
	

?>



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
