import re
from urllib.parse import urlparse

top_brands = ["facebook", "instagram", "twitter", "linkedin", "pinterest", "snapchat", "reddit", "tumblr", "tiktok", "whatsapp",
              "google", "bing", "yahoo", "baidu", "duckduckgo", "yandex", "aol", "ask", "excite", "ecosia",
              "amazon", "ebay", "walmart", "etsy", "alibaba", "target", "bestbuy", "flipkart", "taobao", "asos",
              "drive", "dropbox", "onedrive", "icloud", "box", "mega", "pcloud", "amazon", "sync", "mediafire", "outlook", "mail", "protonmail", "gmx", "tutanota",
              "netflix", "youtube", "spotify", "amazon", "hulu", "disneyplus", "apple", "hbomax", "twitch", "paramountplus",
              "irs", "ssa", "medicare", "usps", "weather", "fbi", "cdc", "nasa", "whitehouse",
              "steam", "xbox", "playstation", "epicgames", "nintendo", "origin", "uplay", "gog", "roblox"]


def having_ip_address(url):
    match = re.search(
        '(([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.'
        '([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\/)|'  # IPv4
        '(([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.'
        '([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\/)|'  # IPv4 with port
        # IPv4 in hexadecimal
        '((0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\/)'
        '(?:[a-fA-F0-9]{1,4}:){7}[a-fA-F0-9]{1,4}|'
        '([0-9]+(?:\.[0-9]+){3}:[0-9]+)|'
        '((?:(?:\d|[01]?\d\d|2[0-4]\d|25[0-5])\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d|\d)(?:\/\d{1,2})?)', url)  # Ipv6
    if match:
        return 1
    else:
        return 0


def subdomain_has_brand(parts):
    if len(parts) >= 3:
        subdomain = parts[0]
        for brand in top_brands:
            if brand in subdomain:
                return 1
        return 0
    else:
        return 0


def path_has_brand(tokens):
    for token in tokens:
        for brand in top_brands:
            if brand in token:
                return 1
    return 0


def has_shortened_url(url):
    match = re.search('bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs|'
                      'yfrog\.com|migre\.me|ff\.im|tiny\.cc|url4\.eu|twit\.ac|su\.pr|twurl\.nl|snipurl\.com|'
                      'short\.to|BudURL\.com|ping\.fm|post\.ly|Just\.as|bkite\.com|snipr\.com|fic\.kr|loopt\.us|'
                      'doiop\.com|short\.ie|kl\.am|wp\.me|rubyurl\.com|om\.ly|to\.ly|bit\.do|t\.co|lnkd\.in|'
                      'db\.tt|qr\.ae|adf\.ly|goo\.gl|bitly\.com|cur\.lv|tinyurl\.com|ow\.ly|bit\.ly|ity\.im|'
                      'q\.gs|is\.gd|po\.st|bc\.vc|twitthis\.com|u\.to|j\.mp|buzurl\.com|cutt\.us|u\.bb|yourls\.org|'
                      'x\.co|prettylinkpro\.com|scrnch\.me|filoops\.info|vzturl\.com|qr\.net|1url\.com|tweez\.me|v\.gd|'
                      'tr\.im|link\.zip\.net',
                      url)
    if match:
        return 1
    else:
        return 0


def lexical_analysis(url):
    features = []

    features.append(len(str(url)))
    parsed_url = urlparse(url)

    hostname = parsed_url.hostname
    domain = parsed_url.netloc
    path = parsed_url.path
    scheme = str(parsed_url.scheme)

    domain_tokens = domain.split('.')
    path_tokens = [token for token in path.split('/') if token]

    domain_lengths = [len(token) for token in domain_tokens]
    path_lengths = [len(token) for token in path_tokens]

    features.append(len(hostname) if hostname else 0)
    features.append(len(domain_tokens) if domain_tokens else 0)
    features.append(len(path_tokens) if path_tokens else 0)
    features.append(sum(domain_lengths)/len(domain_tokens)
                    if len(domain_lengths) > 0 else 0)
    features.append(sum(path_lengths)/len(path_lengths)
                    if len(path_tokens) > 0 else 0)
    features.append(max(domain_lengths) if len(domain_lengths) > 0 else 0)
    features.append(max(path_lengths) if len(path_lengths) > 0 else 0)
    features.append(having_ip_address(url))
    features.append(subdomain_has_brand(domain_tokens))
    features.append(path_has_brand(path_tokens))
    features.append(1 if scheme == 'https' else 0)
    features.append(has_shortened_url(url))

    return features
