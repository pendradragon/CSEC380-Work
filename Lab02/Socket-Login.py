#!/usr/bin/env python3
import socket
import ssl
from urllib.parse import urlparse, urlencode, urljoin
import time
import sys

# ====== CONFIGURE ======
SITE = "http://192.168.196.171/wp-admin"            # IP of the WordPress database
USERNAME = "wp_user"              # So original
PASSWORD = "Password"              # Password security is my passion!!
TIMEOUT = 10                            # socket timeout in seconds
MAX_REDIRECTS = 5
PREVIEW_LEN = 600
# =======================

def parse_status_and_headers(raw_bytes):
    """Return (status_code:int, headers:list_of_tuples, body_bytes)"""
    # Split header and body at first CRLFCRLF
    sep = b"\r\n\r\n"
    if sep in raw_bytes:
        header_block, body = raw_bytes.split(sep, 1)
    else:
        header_block = raw_bytes
        body = b""
    header_lines = header_block.split(b"\r\n")
    status_line = header_lines[0].decode("iso-8859-1", errors="replace")
    # Parse status code from e.g. HTTP/1.1 302 Found
    try:
        parts = status_line.split()
        status_code = int(parts[1])
    except Exception:
        status_code = 0
    headers = []
    for line in header_lines[1:]:
        try:
            k, v = line.decode("iso-8859-1", errors="replace").split(":", 1)
            headers.append((k.strip(), v.strip()))
        except ValueError:
            # malformed header line, skip
            continue
    return status_code, headers, body

def headers_to_dict_multivalue(headers):
    """Convert list of (k,v) -> dict of k -> [v,...] (case-insensitive keys)"""
    d = {}
    for k, v in headers:
        lk = k.lower()
        d.setdefault(lk, []).append(v)
    return d

def build_cookie_header(cookie_jar):
    """cookie_jar: dict name->value -> return 'Cookie' header value"""
    return "; ".join(f"{k}={v}" for k, v in cookie_jar.items())

def set_cookies_from_set_cookie_headers(cookie_jar, set_cookie_values):
    """
    set_cookie_values: list of Set-Cookie header strings.
    Very simple parser: extracts name=value before first ';'
    """
    for sc in set_cookie_values:
        parts = sc.split(";")
        if parts:
            nv = parts[0].strip()
            if "=" in nv:
                name, val = nv.split("=", 1)
                cookie_jar[name] = val

def send_raw_request(host, port, use_tls, request_bytes, timeout=10):
    """Open socket, send request_bytes, read until close, return raw response bytes."""
    with socket.create_connection((host, port), timeout=timeout) as sock:
        if use_tls:
            context = ssl.create_default_context()
            sock = context.wrap_socket(sock, server_hostname=host)
        sock.sendall(request_bytes)
        chunks = []
        while True:
            try:
                chunk = sock.recv(4096)
            except socket.timeout:
                break
            if not chunk:
                break
            chunks.append(chunk)
    return b"".join(chunks)

def http_exchange(url, method="GET", headers=None, body_bytes=b"", timeout=10):
    """
    Perform one HTTP request over raw socket. Returns (status_code, headers_list, body_bytes).
    headers: dict for request; body_bytes is bytes.
    """
    parsed = urlparse(url)
    scheme = parsed.scheme or "http"
    host = parsed.hostname
    port = parsed.port or (443 if scheme == "https" else 80)
    path = parsed.path or "/"
    if parsed.query:
        path += "?" + parsed.query
    use_tls = scheme == "https"

    req_lines = [f"{method} {path} HTTP/1.1",
                 f"Host: {host}"]
    # Add custom headers
    if headers:
        for k, v in headers.items():
            req_lines.append(f"{k}: {v}")
    # Add Content-Length for methods with body
    if method in ("POST", "PUT", "PATCH"):
        req_lines.append(f"Content-Length: {len(body_bytes)}")
    # Close connection after response (makes reading simpler)
    req_lines.append("Connection: close")
    req_lines.append("")  # blank line before body
    req_head = "\r\n".join(req_lines).encode("utf-8") + b"\r\n"
    request_packet = req_head + body_bytes

    raw_resp = send_raw_request(host, port, use_tls, request_packet, timeout=timeout)
    status_code, headers_list, body = parse_status_and_headers(raw_resp)
    return status_code, headers_list, body

def perform_wp_login(base_url, username, password, timeout=10, max_redirects=5):
    """
    Attempts to login to WordPress using raw sockets.
    Returns (final_status_code, final_headers, final_body, cookies)
    """
    cookie_jar = {}  # simple dict of name->value

    # Step 1: GET the login page to collect any initial cookies (e.g., wordpress_test_cookie)
    login_url = urljoin(base_url, "/wp-login.php")
    default_headers = {
        "User-Agent": "simple-socket-client/1.0",
        "Accept": "*/*",
    }
    status, headers_list, body = http_exchange(login_url, "GET", headers=default_headers, body_bytes=b"", timeout=timeout)
    headers_map = headers_to_dict_multivalue(headers_list)
    if "set-cookie" in headers_map:
        set_cookies_from_set_cookie_headers(cookie_jar, headers_map["set-cookie"])

    # Optionally: parse hidden fields from the body (nonce, redirect_to) if needed.
    # For simplicity we will send redirect_to to /wp-admin/ by default.
    redirect_to = urljoin(base_url, "/wp-admin/")

    # Build POST body
    form = {
        "log": username,
        "pwd": password,
        "rememberme": "forever",
        "wp-submit": "Log In",
        "redirect_to": redirect_to,
    }
    body_bytes = urlencode(form).encode("utf-8")

    # Build headers including cookies we collected
    post_headers = default_headers.copy()
    post_headers["Content-Type"] = "application/x-www-form-urlencoded"
    if cookie_jar:
        post_headers["Cookie"] = build_cookie_header(cookie_jar)

    # Step 2: POST credentials
    status, headers_list, body = http_exchange(login_url, "POST", headers=post_headers, body_bytes=body_bytes, timeout=timeout)
    headers_map = headers_to_dict_multivalue(headers_list)
    # Capture Set-Cookie from POST response
    if "set-cookie" in headers_map:
        set_cookies_from_set_cookie_headers(cookie_jar, headers_map["set-cookie"])

    # Handle redirects (Location header). Follow up to max_redirects.
    redirects = 0
    current_status = status
    current_headers = headers_map
    current_body = body
    current_location = None

    while redirects < max_redirects and current_status in (301, 302, 303, 307, 308):
        loc_list = current_headers.get("location", [])
        if not loc_list:
            break
        loc = loc_list[0]
        # build absolute URL if relative
        next_url = urljoin(login_url, loc)
        # prepare headers for follow-up GET: include cookies
        follow_headers = default_headers.copy()
        if cookie_jar:
            follow_headers["Cookie"] = build_cookie_header(cookie_jar)
        status, headers_list, body = http_exchange(next_url, "GET", headers=follow_headers, body_bytes=b"", timeout=timeout)
        headers_map = headers_to_dict_multivalue(headers_list)
        if "set-cookie" in headers_map:
            set_cookies_from_set_cookie_headers(cookie_jar, headers_map["set-cookie"])
        current_status = status
        current_headers = headers_map
        current_body = body
        current_location = next_url
        redirects += 1
        # small polite delay to avoid hammering
        time.sleep(0.1)

    return current_status, current_headers, current_body, cookie_jar, current_location

def main():
    if SITE.startswith("http://") or SITE.startswith("https://"):
        base = SITE
    else:
        base = "https://" + SITE  # default to https if not provided
    print(f"Attempting login to {base} as user '{USERNAME}' (educational/test only)...")
    try:
        status, headers, body, cookies, final_location = perform_wp_login(base, USERNAME, PASSWORD, timeout=TIMEOUT, max_redirects=MAX_REDIRECTS)
    except Exception as e:
        print("Error during login attempt:", e)
        sys.exit(1)

    print("\n--- Result ---")
    print(f"Final status code: {status}")
    if final_location:
        print(f"Final location followed: {final_location}")
    print(f"Cookies received: {cookies}")
    # Heuristic: successful WP login often results in redirect to /wp-admin/ with a Set-Cookie
    # Check if cookies contain 'wordpress_logged_in'
    logged_in = any(name.startswith("wordpress_logged_in") for name in cookies.keys())
    if logged_in:
        print("Login appears to have succeeded (wordpress_logged_in cookie present).")
    else:
        print("Login may have failed (no wordpress_logged_in cookie found).")

    print("\n--- Body preview (first {} chars) ---".format(PREVIEW_LEN))
    try:
        snippet = body.decode("utf-8", errors="replace")[:PREVIEW_LEN]
    except Exception:
        snippet = str(body)[:PREVIEW_LEN]
    print(snippet)

if __name__ == "__main__":
    main()
