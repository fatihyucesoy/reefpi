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
	$result = mysqli_query($con,"SELECT timeStamp, reading FROM sensorReadings 
					WHERE idsensor = (SELECT idsensor FROM sensor WHERE sensorName = 'tempSensor1') 
					ORDER BY timeStamp DESC LIMIT 10;");
					
	$dataArray = array(array('timeStamp', 'reading'));
	
	while($row = mysqli_fetch_array($result)) {
    	$dataArray[] = array($row['timeStamp'], (int) $row['reading']);
	}
	
	
	echo count($dataArray);
?>
<!--Load the AJAX API-->

        <script type="text/javascript" src="https://www.google.com/jsapi"></script>
   		<script type="text/javascript">
      	google.load("visualization", "1", {packages:["corechart"]});
      	google.setOnLoadCallback(drawChart);
      	function drawChart() {
        var data = google.visualization.arrayToDataTable(<?php echo json_encode($dataArray); ?>);

        var options = {
        	height : 400,
          	title: 'temp 1 temperature',
          	is3d: true,
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
<h3>LED Temperature Reading</h3>
<?php
			$resultReadingLED = mysqli_query($con,"SELECT reading FROM sensorReadings 
					WHERE idsensor = (SELECT idsensor FROM sensor WHERE sensorName = 'tempSensor1') 
					ORDER BY timeStamp DESC 
					limit 1;");

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
