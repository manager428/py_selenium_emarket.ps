<?php
/* upload one file */
$upload_dir = './storage/media';
$name = basename($_FILES["myfile"]["name"]);
$userid = $_REQUEST["method"];
echo"\n    {$userid}";
$target_file = "$upload_dir/$name";
if ($_FILES["myfile"]["size"] > 90000000) { // limit size of 10KB
    echo 'error: your file is too large.';
    exit();
}
$path = 'media/'.$name;
$create = date("Y-m-d h-i-s");

$servername = "server name";
$username = "username";
$password = "db_pass";
$dbname = "db_name";

$conn = new mysqli($servername, $username, $password, $dbname);
$sql = "INSERT INTO files (`user_id`, `filename`, `disk`, `path`, `extension`, `mime`, `created_at`, `updated_at`) VALUES (1, '$name', 'public_storage', '$path', 'jpg', 'image/jpeg', '$create', '$create')";
if (mysqli_query($conn, $sql)) {
    echo "New record created successfully";
  } else {
    echo "Error: " . $sql . "<br>" . mysqli_error($conn);
  }
  
$sqlgetdata = "SELECT id, `filename` FROM files WHERE `filename`='$name'";
$result = $conn->query($sqlgetdata);
$imageid = 0;
$slash = "\\";
$entity_type_name = "Modules\\\Product\\\Entities\\\Product";
if ($result->num_rows > 0) {
// output data of each row
while($row = $result->fetch_assoc()) {
    $imageid = $row["id"];
}
} else {
echo "0 results";
}
echo"\n {$entity_type_name}";
$sqlentry_file = "INSERT INTO entity_files (`file_id`, `entity_type`, `entity_id`, `zone`, `created_at`, `updated_at`) VALUES ('$imageid', '$entity_type_name', '$userid', 'base_image', '$create', '$create')";
echo"\n filename : {$sqlentry_file}";
if (mysqli_query($conn, $sqlentry_file)) {
    echo "New record created successfully";
  } else {
    echo "Error: " . $sql . "<br>" . mysqli_error($conn);
  }

$conn->close();

if (!move_uploaded_file($_FILES["myfile"]["tmp_name"], $target_file))
    echo 'error: '.$_FILES["myfile"]["error"].' see /var/log/apache2/error.log for permission reason';
else {
    if (isset($_POST['data'])) print_r($_POST['data']);
    echo "\n filename : {$userid}";
}
?>
