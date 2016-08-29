<?php
ECHO "Hello World!<br>";
echo "Hello World!<br>";
EcHo "Hello World!<br>";
?>

<?php
// This is the argument passed into php after the file name
$argv[1];
$servername = "206.221.178.138";
$username = "andybaay_general";
$password = "ineedglycans";
$database = "andybaay_glycomeDB";

$db = mysqli_connect($servername, $username, $password, $database)
 or die('Error connecting to MySQL server.');

$query = "SELECT * FROM structure WHERE structure_id = 2300";
mysqli_query($db, $query) or die('Error querying database.');

$result = mysqli_query($db, $query);
$row = mysqli_fetch_array($result);
echo $argv[1];
var_dump($row);
?>

<?php
ECHO "We tried!<br>";
?>