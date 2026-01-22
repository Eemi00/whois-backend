import socket

# Tehdään function jolla haetaan kaikki top level domainit jotta ei tarvitse itse listata 1500+ 
def get_tld_server(tld):
    # Kysytään IANA:ta kaikki tiedot
    iana_server = "whois.iana.org"

    response = raw_socket_query(tld, iana_server)

    for line in response.splitlines():
        if "whois:" in line.lower():
            return line.split(":")[-1].strip()
    
    return None


def raw_socket_query(query, server):
    # Luodaan socketti
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(5)
    try:
        # Yhdistetään whois serveriin
        sock.connect((server, 43))
        # Lähetetään query
        sock.send(f"{query}\r\n".encode("utf-8"))

        # Otetaan vastaus takaisin
        full_response = b""
        # Käytetään while looppia jotta tiedot ei vain katkaise jos se ylittää 4096 byten rajan
        while True:
            data = sock.recv(4096)
            if not data:
                break
            full_response += data
        
        return full_response.decode("utf-8", errors="ignore") # Palautetaan koodi muotoon jonka käyttäjä voi helposti lukea
    finally:
        sock.close() # Suljetaan yhteys


def parse_the_data(raw_text):
    lines = raw_text.splitlines() # Tehdään tiedoista rivejä jotta JSON lukee ne paremmin ja saadaan ne paremmin näkymään fronttiin
    parsed_data = {} # Aloitetaan tyhjällä dictionaryllä

    # Luuppi jolla parsitaan data luettavaksi fronttia varten
    for line in lines:

        # Jos domainia ei löydy se on vapaana, tulostetaan se
        if "not found" in line.lower():
            return {"status": "available"}

        if ":" in line: # Tämä siksi jotta koodi välittää vain riveistä jossa on : esim "status: Registered"
            parts = line.split(":", 1)
            key = parts[0].strip().replace(".", "")
            value = parts[1].strip()
            
            # Tarkistetaan onko tieto jo teidossamme jotta sitä ei tarvitse toistaa
            if key in parsed_data:
                # Jos tieto on jo lista lisätään se
                if isinstance(parsed_data[key], list):
                    parsed_data[key].append(value)
                # Jos se on yksi stringi vain muutetaan se listaksi
                else:
                    parsed_data[key] = [parsed_data[key], value]
            else:
                parsed_data[key] = value
    return parsed_data


def get_whois_data(domain):
    
    tld = domain.split(".")[-1]

    # Haetaan top level domainin server
    target_server = get_tld_server(tld)

    # Tarkistetaan onko serveri oikea
    if not target_server:
        return {"error": f"Could not find a WHOIS server for .{tld}"}
    
    raw_text = raw_socket_query(domain, target_server)

    # Määritellään vastaus
    return parse_the_data(raw_text)