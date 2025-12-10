<?php
session_start();
if (!isset($_SESSION['role']) || $_SESSION['role'] !== "basic") {
    header("Location: login.php");
    exit();
}
?>
<!DOCTYPE html>
<html>
<head>
    <title>Basic User Page</title>
</head>
<body>
    <h2>Welcome, Basic User!</h2>
    <p>You are logged in as: <?php echo $_SESSION['username']; ?></p>

    <p>This is the basic user page.</p>

    <a href="logout.php">Log Out</a>
</body>
</html>
