import re
import requests
from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})


def get_response(url, path):
    try:
        res = requests.get(url)
        if res.status_code != 200:
            return 0
        driver = webdriver.Chrome(service=Service(
            executable_path=path), options=options)
        driver.get(url)
        return driver
    except Exception as e:
        print(e)
        return 0


def redirect_count(driver):
    return len(driver.get_log('performance'))


def iframe_count(driver):
    return len(driver.find_elements(By.TAG_NAME, 'iframe'))


def hyperlink_ratios(driver, url):
    all_hyperlinks = driver.find_elements(By.TAG_NAME, 'a')
    internal_hyperlinks = []

    parsed_url = urlparse(url)
    base_url = parsed_url.scheme + '://' + parsed_url.netloc

    for hyperlink in all_hyperlinks:
        href = hyperlink.get_attribute('href')
        if href and (href.startswith('/') or href.startswith(base_url)):
            internal_hyperlinks.append(href)

    total_hyperlinks = len(all_hyperlinks)

    if total_hyperlinks > 0:
        return (len(internal_hyperlinks) / total_hyperlinks, 1 - (len(internal_hyperlinks) / total_hyperlinks))
    else:
        return (0, 0)


def right_click(driver):
    try:
        driver.execute_script(
            "document.addEventListener('contextmenu', function(e){e.preventDefault();}, false);")
        return 1
    except:
        return 0


def popup_count(driver):
    script_tags = driver.find_elements(By.TAG_NAME, "script")
    javascript_code = [tag.get_attribute(
        'innerHTML') for tag in script_tags if tag.get_attribute('innerHTML')]

    popup_window_count = 0
    for code in javascript_code:
        if re.search(r'window\.open\s*\(', code):
            popup_window_count = 1
            break

    return popup_window_count


def get_features(url, path):
    driver = get_response(url, path)
    if driver == 0:
        return 0
    internal_ratio, external_ratio = hyperlink_ratios(driver, url)

    features = [redirect_count(driver), iframe_count(
        driver), internal_ratio, external_ratio, right_click(driver), popup_count(driver)]

    driver.quit()

    return features
