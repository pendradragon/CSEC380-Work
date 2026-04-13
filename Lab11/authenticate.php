<?php
session_start();

// Hardcoded users
$users = [
    "user" => ["password" => "user123", "role" => "basic"],
    "admin" => ["password" => "admin123", "role" => "admin"]
];

$username = $_POST['username'];
$password = $_POST['password'];

if (isset($users[$username]) && $users[$username]['password'] === $password) {
    
    $_SESSION['username'] = $username;
    $_SESSION['role'] = $users[$username]['role'];

    // Redirect based on role
    if ($_SESSION['role'] === "admin") {
        header("Location: admin.php");
    } else {
        header("Location: dashboard.php");
    }
    exit();
} else {
    header("Location: login.php?error=1");
    exit();
}