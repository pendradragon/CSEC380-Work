<?php
// Secure session settings
session_start([
    'cookie_httponly' => true,
    'cookie_secure' => false, // set TRUE if using HTTPS
    'cookie_samesite' => 'Strict'
]);

// Regenerate session ID periodically
if (!isset($_SESSION['initiated'])) {
    session_regenerate_id(true);
    $_SESSION['initiated'] = true;
}

// Simple rate limiting (DoS protection)
if (!isset($_SESSION['attempts'])) {
    $_SESSION['attempts'] = 0;
    $_SESSION['last_attempt'] = time();
}

// CSRF Token generator
function generateCSRFToken() {
    if (empty($_SESSION['csrf_token'])) {
        $_SESSION['csrf_token'] = bin2hex(random_bytes(32));
    }
    return $_SESSION['csrf_token'];
}

// CSRF validation
function validateCSRFToken($token) {
    return hash_equals($_SESSION['csrf_token'], $token);
}

// Secure headers (prevent info disclosure)
header("X-Frame-Options: DENY");
header("X-Content-Type-Options: nosniff");
header("X-XSS-Protection: 1; mode=block");
?>