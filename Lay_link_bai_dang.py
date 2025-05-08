from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import re

def get_html_with_selenium(url):
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.get(url)
    
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    html = driver.page_source
    driver.quit()
    return html

def parse_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    return soup


def extract_links(soup):
    links = []
    pattern = re.compile(r'-pr\d+')
    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        if "/ban-" in href and pattern.search(href):
            links.append("https://batdongsan.com.vn" + href)
    return links

def save_links_to_file(links, filename):
    with open(filename, 'a') as file: 
        for link in links:
            file.write(link + '\n')

def main(input_file):
    with open(input_file, 'r') as file:
        urls = file.read().splitlines()

    filename = 'links_tong_hop_ha_dong.txt'
    for url in urls:
        html = get_html_with_selenium(url)
        soup = parse_html(html)
        links = extract_links(soup)
        save_links_to_file(links, filename)
        print(f"Đã lưu {len(links)} liên kết từ {url} vào file {filename}")

if __name__ == '__main__':
    input_file = 'links_p_hd.txt'  
    main(input_file)
