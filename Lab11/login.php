<?php
session_start();

// If already logged in, redirect
if (isset($_SESSION['role'])) {
    if ($_SESSION['role'] === 'admin') {
        header("Location: admin.php");
        exit();
    } else {
        header("Location: basic.php");
        exit();
    }
}
?>
<!DOCTYPE html>
<html>
<head>
    <title>Login</title>
</head>
<body>
    <h2>Login Page</h2>
    <?php 
        if (isset($_GET['error'])) {
            echo "<p style='color:red'>Invalid username or password</p>";
        }
    ?>
    <form action="authenticate.php" method="POST">
        <label>Username:</label><br>
        <input type="text" name="username" required><br><br>

        <label>Password:</label><br>
        <input type="password" name="password" required><br><br>

        <button type="submit">Log In</button>
    </form>
</body>
</html>
