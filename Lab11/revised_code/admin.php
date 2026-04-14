<?php
require 'config.php';

// Strict access control (prevents privilege escalation)
if (!isset($_SESSION['username']) || $_SESSION['role'] !== "admin") {
    header("Location: login.php");
    exit();
}
?>

<h2>Admin Panel</h2>
<p>Welcome <?php echo htmlspecialchars($_SESSION['username']); ?></p>

<p>Admin-only content here.</p>

<a href="logout.php">Logout</a>