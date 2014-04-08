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
Available Device Types
</p>
<?php
			$resultDeviceTypes = mysqli_query($con, "SELECT * FROM deviceType");

		echo "<table border='1'>
	<tr>
		<th>Device type</th>
		<th>Bus Type</th>
	</tr>";

			while($rowDeviceType = mysqli_fetch_array($resultDeviceTypes))
				{
					echo "<tr>";
					echo "<td>" . $rowDeviceType['deviceTypeName'] . "</td>";
					echo "<td>" . $rowDeviceType['busType'] . "</td>";
					echo "</tr>";
				}
		echo "</table>";

echo "<p>";
echo "Add a Device Type";
echo "</p>";

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

if(isset($_POST['addDeviceType']))
{
	$deviceName = ($_POST['deviceTypeName']);
	$busType = ($_POST['busType']);
	$addDeviceType = mysqli_query($con, "INSERT INTO devicetype ". "(deviceTypeName, busType)". "VALUES ('$deviceName', '$busType')");
	$result = ($addDeviceType);
	if(!$result)
	{
		echo "Sorry, cannot submit your request";
	}
	else
	{
		redirect($_SERVER['PHP_SELF']);
	}
}
?>
<p></p>

<form method="post" action="<?php $_PHP_SELF ?>">
	<table width="400" border="0" cellspacing="1" cellpadding="2">
		<tr>
			<td width="100">Device Type Name</td>
			<td><input name="deviceTypeName" type="text" id="name"></td>
		</tr>
		<tr>
			<td width="100">Bus Type</td>
			<td><input name="busType" type="text" id="type"></td>
		</tr>
		<tr>
			<td width="100"> </td>
			<td>
				<input name="addDeviceType" type="submit" id="addDeviceType" value="Add Device Type">
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
