<?php
session_start();

if (!isset($_SESSION['username']) || $_SESSION['role'] !== "basic") {
    header("Location: login.php");
    exit();
}
?>

<!DOCTYPE html>
<html>
<head>
    <title>User Dashboard</title>
</head>
<body>
    <h2>Welcome, <?php echo $_SESSION['username']; ?>!</h2>
    <p>This is the basic user page.</p>

    <a href="logout.php">Logout</a>
</body>
</html>