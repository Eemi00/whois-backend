import socket
import time

# Tehdään function jolla haetaan kaikki top level domainit jotta ei tarvitse itse listata 1500+
def get_tld_server(tld):
    iana_server = "whois.iana.org"
    response = raw_socket_query(tld, iana_server)

    for line in response.splitlines():
        if "whois:" in line.lower():
            return line.split(":")[-1].strip()

    return None


def raw_socket_query(query, server, port=43, connect_timeout=8, read_timeout=15, retries=3):
    last_err = None

    for attempt in range(retries + 1):
        try:
            with socket.create_connection((server, port), timeout=connect_timeout) as sock:
                sock.settimeout(read_timeout)
                sock.sendall(f"{query}\r\n".encode("utf-8"))

                chunks = []
                while True:
                    data = sock.recv(4096)
                    if not data:
                        break
                    chunks.append(data)

                return b"".join(chunks).decode("utf-8", errors="ignore")

        except (TimeoutError, socket.timeout, OSError) as e:
            last_err = e
            if attempt < retries:
                time.sleep(0.6 * (attempt + 1))
                continue

            # Give a clear error instead of crashing the API
            raise RuntimeError(f"WHOIS query to {server}:{port} failed: {e}") from e

    raise RuntimeError(f"WHOIS query to {server}:{port} failed") from last_err


def parse_the_data(raw_text):
    lines = raw_text.splitlines()
    parsed_data = {}

    for line in lines:
        if "not found" in line.lower():
            return {"status": "available"}

        if ":" in line:
            parts = line.split(":", 1)
            key = parts[0].strip().replace(".", "")
            value = parts[1].strip()

            if key in parsed_data:
                if isinstance(parsed_data[key], list):
                    parsed_data[key].append(value)
                else:
                    parsed_data[key] = [parsed_data[key], value]
            else:
                parsed_data[key] = value
    return parsed_data


def get_whois_data(domain):
    tld = domain.split(".")[-1]
    target_server = get_tld_server(tld)

    if not target_server:
        return {"error": f"Could not find a WHOIS server for .{tld}"}

    raw_text = raw_socket_query(domain, target_server)
    return parse_the_data(raw_text)