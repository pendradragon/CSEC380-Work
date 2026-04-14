<?php
require 'config.php';

// Rate limiting (DoS protection)
if ($_SESSION['attempts'] > 5 && (time() - $_SESSION['last_attempt']) < 60) {
    die("Too many attempts. Try again later.");
}

// Validate CSRF token (tampering protection)
if (!validateCSRFToken($_POST['csrf_token'])) {
    die("Invalid request.");
}

// Hardcoded users (now hashed passwords)
$users = [
    "user" => [
        "password" => password_hash("user123", PASSWORD_DEFAULT),
        "role" => "basic"
    ],
    "admin" => [
        "password" => password_hash("admin123", PASSWORD_DEFAULT),
        "role" => "admin"
    ]
];

// Input validation (tampering prevention)
$username = filter_input(INPUT_POST, 'username', FILTER_SANITIZE_STRING);
$password = $_POST['password'];

if (isset($users[$username]) && password_verify($password, $users[$username]['password'])) {

    // Reset attempts
    $_SESSION['attempts'] = 0;

    // Prevent session fixation (spoofing protection)
    session_regenerate_id(true);

    $_SESSION['username'] = $username;
    $_SESSION['role'] = $users[$username]['role'];

    // Strict role-based redirect (prevent escalation)
    if ($_SESSION['role'] === "admin") {
        header("Location: admin.php");
    } else {
        header("Location: dashboard.php");
    }
    exit();

} else {
    $_SESSION['attempts']++;
    $_SESSION['last_attempt'] = time();

    header("Location: login.php?error=1");
    exit();
}