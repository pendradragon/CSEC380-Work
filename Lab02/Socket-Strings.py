#!/usr/bin/env python3
"""
Fetch a WordPress login page (/wp-login.php) using raw sockets and simple HTTP request strings.
Supports both http and https URLs.
"""

import socket
import ssl
from urllib.parse import urlparse

def fetch(url, timeout=10, preview_len=500):
    parsed = urlparse(url)
    scheme = parsed.scheme or "http"
    host = parsed.hostname
    port = parsed.port
    path = parsed.path or "/"
    if parsed.query:
        path += "?" + parsed.query

    if scheme not in ("http", "https"):
        raise ValueError("Only http and https schemes are supported")

    if port is None:
        port = 443 if scheme == "https" else 80

    # Build a minimal HTTP/1.1 GET request string
    request_lines = [
        f"GET {path} HTTP/1.1",
        f"Host: {host}",
        "User-Agent: simple-socket-client/1.0",
        "Accept: */*",
        "Connection: close",  # close after response so we can read until EOF
        "",
        "",
    ]
    request_data = "\r\n".join(request_lines).encode("utf-8")

    # Create TCP connection
    with socket.create_connection((host, port), timeout=timeout) as sock:
        # Wrap with TLS if https
        if scheme == "https":
            context = ssl.create_default_context()
            # For simple demonstration we use default verification. If you want to skip verification:
            # context.check_hostname = False; context.verify_mode = ssl.CERT_NONE  # NOT recommended
            sock = context.wrap_socket(sock, server_hostname=host)

        # Send request
        sock.sendall(request_data)

        # Receive response until socket closes
        chunks = []
        while True:
            try:
                chunk = sock.recv(4096)
            except socket.timeout:
                break
            if not chunk:
                break
            chunks.append(chunk)

    raw_response = b"".join(chunks)
    # Split headers and body for nicer preview
    try:
        header_bytes, body_bytes = raw_response.split(b"\r\n\r\n", 1)
    except ValueError:
        header_bytes = raw_response
        body_bytes = b""

    headers = header_bytes.decode("iso-8859-1", errors="replace")
    body = body_bytes.decode("utf-8", errors="replace")

    return headers, body

if __name__ == "__main__":
    url = "http://192.168.196.171/wp-login.php"  # the VM IP that is hosting the WordPress site

    try:
        headers, body = fetch(url, timeout=10)
        print("=== Response headers ===")
        print(headers)
        print("\n=== Body preview ===")
        print(body[:500])  # preview of the body
    except Exception as e:
        print("Error:", e)
