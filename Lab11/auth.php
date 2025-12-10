<?php
session_start();

// Hardcoded accounts
$users = [
    "basicuser" => [
        "password" => "basic123",
        "role" => "basic"
    ],
    "admin" => [
        "password" => "adminpass",
        "role" => "admin"
    ]
];

$username = $_POST['username'] ?? "";
$password = $_POST['password'] ?? "";

if (isset($users[$username]) && $users[$username]['password'] === $password) {
    $_SESSION['role'] = $users[$username]['role'];
    $_SESSION['username'] = $username;

    // Redirect based on role
    if ($_SESSION['role'] === "admin") {
        header("Location: admin.php");
    } else {
        header("Location: basic.php");
    }
    exit();
}

// Failed login
header("Location: login.php?error=1");
exit();
?>
