<?php
require 'config.php';

// Strict access control (prevents privilege escalation)
if (!isset($_SESSION['username']) || $_SESSION['role'] !== "basic") {
    header("Location: login.php");
    exit();
}
?>

<h2>User Dashboard</h2>
<p>Welcome <?php echo htmlspecialchars($_SESSION['username']); ?></p>

<a href="logout.php">Logout</a>