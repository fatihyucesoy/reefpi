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
Available Schedule Types
</p>

<?php
	$resultScheduleTypes = mysqli_query($con, "SELECT * FROM scheduleType");

	if($resultScheduleTypes){
	echo "<table border='1'>
	<tr>
		<th>ID</th>
		<th>Schedule Type Name</th>
		<th>Description</th>
	</tr>";

			while($rowScheduleType = mysqli_fetch_array($resultScheduleTypes))
				{
					echo "<tr>";
					echo "<td>" . $rowScheduleType['idscheduleType'] . "</td>";
					echo "<td>" . $rowScheduleType['scheduleTypeName'] . "</td>";
					echo "<td>" . $rowScheduleType['scheduleTypeDescription'] . "</td>";	
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
Add a Schedule Type
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

if(isset($_POST['addScheduleTypes']))
{
	$scheduleTypeName = ($_POST['scheduleTypeName']);
	$description = ($_POST['description']);
		$addScheduleType = mysqli_query($con, "INSERT INTO scheduletype (scheduleTypeName, scheduleTypeDescription) VALUES ('$scheduleTypeName', '$description')");
		$result = ($addScheduleType);
		if(!$result)
		{
			echo "Sorry, cannot submit your request:";
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
			<td width="100">Schedule Type Name</td>
			<td><input name="scheduleTypeName" type="text" id="scheduleTypeName"></td>
		</tr>
		<tr>
			<td width="100">Description</td>
			<td><input name="description" type="text" id="description"></td>
		</tr>
		<tr>
			<td width="100"> </td>
			<td>
				<input name="addScheduleTypes" type="submit" id="addScheduleTypes" value="Add Schedule Type">
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
