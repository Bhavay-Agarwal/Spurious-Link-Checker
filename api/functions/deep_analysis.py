import whois
import requests
from urllib.parse import urlparse


def get_nordvpn_data(url):
    url = "https://link-checker.nordvpn.com/v1/public-url-checker/check-url"
    response = requests.post(url, json={"url": url})

    if response.status_code != 200:
        return 0

    data = response.json()
    return data


def get_wot(url):
    parsed_url = urlparse(url)
    hostname = parsed_url.hostname

    wot_url = f"https://www.mywot.com/api/safetyCheck?url={hostname}"

    response = requests.get(wot_url)
    if response.status_code != 200:
        return 0

    data = response.json()
    return data


def get_network_data(url):
    parsed_url = urlparse(url)
    hostname = parsed_url.hostname

    network_url = f"https://www.semrush.com/website/_next/data/oRdLlbm0yiaFnUnliBotH/{hostname}/overview.json?domain={hostname}"
    response = requests.get(network_url)
    if response.status_code != 200:
        return 0

    data = response.json()
    return data


def analyze_link(url):
    network_data = get_network_data(url)
    wot_data = get_wot(url)
    nord_data = get_nordvpn_data(url)
    whois_data = whois.whois(url)

    traffic = network_data["pageProps"]["page"]["trafficStats"]

    return {
        "wot": wot_data["score"] or "N/A",
        "global_rank": traffic["globalRank"]["value"] or "N/A",
        "network_traffic": traffic["visits"]["value"] or "N/A",
        "creation_date": whois_data["creation_date"] or "N/A",
        "expiration_date": whois_data["expiration_date"] or "N/A",
        "nordvpn": nord_data["status"] or "N/A"
    }
