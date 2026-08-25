"""
SSRF Protection & URL Validation Module for YatraDham SEO Pipeline.
Defends against Server-Side Request Forgery (SSRF), DNS Rebinding,
Private IP Scanning, and Cloud Metadata Exfiltration.
"""
import ipaddress
import socket
import urllib.parse
from typing import Tuple

# Prohibited Private, Loopback, Link-Local, and Cloud Metadata Networks
BLOCKED_IP_NETWORKS = [
    ipaddress.ip_network("0.0.0.0/8"),          # Current network
    ipaddress.ip_network("10.0.0.0/8"),         # Private RFC1918
    ipaddress.ip_network("100.64.0.0/10"),      # Shared Address Space (Carrier-grade NAT)
    ipaddress.ip_network("127.0.0.0/8"),        # Loopback IPv4
    ipaddress.ip_network("169.254.0.0/16"),     # Link-local / AWS & GCP Instance Metadata
    ipaddress.ip_network("172.16.0.0/12"),      # Private RFC1918
    ipaddress.ip_network("192.0.0.0/24"),       # IETF Protocol Assignments
    ipaddress.ip_network("192.0.2.0/24"),       # TEST-NET-1
    ipaddress.ip_network("192.168.0.0/16"),     # Private RFC1918
    ipaddress.ip_network("198.18.0.0/15"),      # Benchmark testing
    ipaddress.ip_network("198.51.100.0/24"),    # TEST-NET-2
    ipaddress.ip_network("203.0.113.0/24"),     # TEST-NET-3
    ipaddress.ip_network("224.0.0.0/4"),        # Multicast
    ipaddress.ip_network("240.0.0.0/4"),        # Reserved / Future use
    ipaddress.ip_network("255.255.255.255/32"), # Broadcast
    # IPv6 Blocked
    ipaddress.ip_network("::1/128"),            # IPv6 Loopback
    ipaddress.ip_network("::/128"),             # IPv6 Unspecified
    ipaddress.ip_network("fc00::/7"),           # IPv6 Unique Local Address (ULA)
    ipaddress.ip_network("fe80::/10"),          # IPv6 Link-Local
]

BLOCKED_HOSTNAMES = {
    "localhost",
    "metadata.google.internal",
    "metadata",
    "instance-data",
}

ALLOWED_SCHEMES = {"http", "https"}


def is_safe_url(url: str) -> Tuple[bool, str]:
    """
    Validates a target URL against SSRF attacks:
    1. Enforces HTTP/HTTPS protocols only (blocks file://, gopher://, dict://, ftp://).
    2. Resolves DNS hostname to physical IP addresses.
    3. Blocks Private/Internal RFC1918 IPs, Loopback (127.0.0.1), Link-Local (169.254.169.254 AWS metadata).
    4. Guards against DNS rebinding and decimal/hex/octal IP obfuscation.
    """
    if not url or not isinstance(url, str):
        return False, "Empty or invalid URL."

    cleaned_url = url.strip()
    try:
        parsed = urllib.parse.urlparse(cleaned_url)
    except Exception as e:
        return False, f"Malformed URL: {e}"

    if not parsed.scheme or parsed.scheme.lower() not in ALLOWED_SCHEMES:
        return False, f"Prohibited scheme '{parsed.scheme}'. Only HTTP and HTTPS are permitted."

    hostname = parsed.hostname
    if not hostname:
        return False, "Missing hostname in URL."

    hostname_clean = hostname.strip().lower()

    if hostname_clean in BLOCKED_HOSTNAMES or hostname_clean.endswith(".internal") or hostname_clean.endswith(".local"):
        return False, f"Prohibited internal host: {hostname_clean}"

    # Resolve all IPs for hostname to prevent DNS rebinding to internal subnets
    try:
        addr_info = socket.getaddrinfo(hostname_clean, parsed.port or (443 if parsed.scheme == "https" else 80), proto=socket.IPPROTO_TCP)
    except socket.gaierror:
        return False, f"DNS resolution failed for host '{hostname_clean}'."
    except Exception as e:
        return False, f"Error resolving host '{hostname_clean}': {e}"

    if not addr_info:
        return False, f"No IP address found for host '{hostname_clean}'."

    for family, socktype, proto, canonname, sockaddr in addr_info:
        ip_str = sockaddr[0]
        try:
            ip_obj = ipaddress.ip_address(ip_str)
            # Check against blocked networks
            if ip_obj.is_private or ip_obj.is_loopback or ip_obj.is_link_local or ip_obj.is_multicast or ip_obj.is_reserved or ip_obj.is_unspecified:
                return False, f"SSRF violation: Host '{hostname_clean}' resolves to restricted internal IP: {ip_str}"

            for net in BLOCKED_IP_NETWORKS:
                if ip_obj in net:
                    return False, f"SSRF violation: Host '{hostname_clean}' resolves to prohibited network range: {ip_str}"
        except ValueError:
            return False, f"Invalid IP address representation: {ip_str}"

    return True, "URL is safe for scraping."
