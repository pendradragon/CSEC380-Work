<?php
session_start();
?>

<!DOCTYPE html>
<html>
<head>
    <title>Login</title>
</head>
<body>
    <h2>Login Page</h2>

    <form action="authenticate.php" method="POST">
        <label>Username:</label><br>
        <input type="text" name="username" required><br><br>

        <label>Password:</label><br>
        <input type="password" name="password" required><br><br>

        <button type="submit">Login</button>
    </form>

    <?php
    if (isset($_GET['error'])) {
        echo "<p style='color:red;'>Invalid login!</p>";
    }
    ?>
</body>
</html>