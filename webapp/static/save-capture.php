<?php

$image = $_POST["image"];
$image = explode(";", $image)[1];
$image = explode(",", $image)[1];

$image = base64_encode($image);

echo "File ready";
?>