<?php
session_start();
if (!isset($_SESSION['role']) || $_SESSION['role'] !== "admin") {
    header("Location: login.php");
    exit();
}
?>
<!DOCTYPE html>
<html>
<head>
    <title>Admin Page</title>
</head>
<body>
    <h2>Admin Control Panel</h2>
    <p>Welcome, <?php echo $_SESSION['username']; ?>.</p>

    <p>This page is restricted to administrators only.</p>

    <a href="logout.php">Log Out</a>
</body>
</html>
