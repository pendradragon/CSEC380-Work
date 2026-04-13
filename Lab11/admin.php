<?php
session_start();

if (!isset($_SESSION['username']) || $_SESSION['role'] !== "admin") {
    header("Location: login.php");
    exit();
}
?>

<!DOCTYPE html>
<html>
<head>
    <title>Admin Panel</title>
</head>
<body>
    <h2>Admin Panel</h2>
    <p>Welcome, <?php echo $_SESSION['username']; ?>!</p>

    <p>This is the admin-only page.</p>

    <a href="logout.php">Logout</a>
</body>
</html>