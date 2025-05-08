from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import csv
import time
import os

def initialize_driver():
    """Khởi tạo trình duyệt Chrome sử dụng webdriver-manager với chế độ full screen"""
    options = webdriver.ChromeOptions()
    options.add_argument("--start-fullscreen")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def capture_full_page_screenshot(driver, url, output_folder):
    driver.get(url)
    time.sleep(5)

    driver.maximize_window()

    total_height = driver.execute_script("return document.body.scrollHeight")
    total_width = driver.execute_script("return document.body.scrollWidth")
    driver.set_window_size(total_width, total_height)

    file_name = f"screenshot_{url.split('/')[-1]}.png"
    file_path = os.path.join(output_folder, file_name)
    driver.save_screenshot(file_path)
    print(f"Đã chụp ảnh toàn bộ trang của {url} và lưu tại {file_path}")

def get_html(driver, url):
    driver.get(url)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

    try:
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "re__detail-content")]'))
        )
    except Exception as e:
        print("Không thể tải phần tử chi tiết:", e)

    return driver.page_source

def parse_html(html):
    return BeautifulSoup(html, 'html.parser')

def extract_data(soup):
    data = {}

    title = soup.find('h1', class_='re__pr-title')
    address = soup.find('span', class_='re__pr-short-description')

    description_div = soup.find('div', class_='re__section-body re__detail-content js__section-body js__pr-description js__tracking')
    if description_div:
        description = description_div.get_text(separator=' ').replace('\n', ' ').strip()
    else:
        description = 'N/A'

    short_info_items = soup.find('div', class_='re__pr-short-info re__pr-config js__pr-config')
    posted_date = short_info_items.find('span', string='Ngày đăng').find_next('span').text if short_info_items and short_info_items.find('span', string='Ngày đăng') else 'N/A'
    expiry_date = short_info_items.find('span', string='Ngày hết hạn').find_next('span').text if short_info_items and short_info_items.find('span', string='Ngày hết hạn') else 'N/A'
    listing_type = short_info_items.find('span', string='Loại tin').find_next('span').text if short_info_items and short_info_items.find('span', string='Loại tin') else 'N/A'
    listing_id = short_info_items.find('span', string='Mã tin').find_next('span').text if short_info_items and short_info_items.find('span', string='Mã tin') else 'N/A'

    specs_items = soup.find_all('div', class_='re__pr-specs-content-item')
    area = specs_items[0].find('span', class_='re__pr-specs-content-item-value').text.strip() if len(specs_items) > 0 else 'N/A'
    price = specs_items[1].find('span', class_='re__pr-specs-content-item-value').text.strip() if len(specs_items) > 1 else 'N/A'
    frontage = specs_items[2].find('span', class_='re__pr-specs-content-item-value').text.strip() if len(specs_items) > 2 else 'N/A'
    entrance_width = specs_items[3].find('span', class_='re__pr-specs-content-item-value').text.strip() if len(specs_items) > 3 else 'N/A'
    house_direction = specs_items[4].find('span', class_='re__pr-specs-content-item-value').text.strip() if len(specs_items) > 4 else 'N/A'
    balcony_direction = specs_items[5].find('span', class_='re__pr-specs-content-item-value').text.strip() if len(specs_items) > 5 else 'N/A'
    number_of_floors = specs_items[6].find('span', class_='re__pr-specs-content-item-value').text.strip() if len(specs_items) > 6 else 'N/A'
    bedrooms = specs_items[7].find('span', class_='re__pr-specs-content-item-value').text.strip() if len(specs_items) > 7 else 'N/A'
    toilets = specs_items[8].find('span', class_='re__pr-specs-content-item-value').text.strip() if len(specs_items) > 8 else 'N/A'
    legal_status = specs_items[9].find('span', class_='re__pr-specs-content-item-value').text.strip() if len(specs_items) > 9 else 'N/A'
    interior = specs_items[10].find('span', class_='re__pr-specs-content-item-value').text.strip() if len(specs_items) > 10 else 'N/A'

    data['Title'] = title.text.strip() if title else 'N/A'
    data['Address'] = address.text.strip() if address else 'N/A'
    data['Description'] = description
    data['Posted Date'] = posted_date.strip() if posted_date else 'N/A'
    data['Expiry Date'] = expiry_date.strip() if expiry_date else 'N/A'
    data['Price'] = price if price else 'N/A'
    data['Area'] = area if area else 'N/A'
    data['House Direction'] = house_direction if house_direction else 'N/A'
    data['Balcony Direction'] = balcony_direction if balcony_direction else 'N/A'
    data['Bedrooms'] = bedrooms if bedrooms else 'N/A'
    data['Toilets'] = toilets if toilets else 'N/A'
    data['Frontage'] = frontage if frontage else 'N/A'
    data['Entrance Width'] = entrance_width if entrance_width else 'N/A'
    data['Number of Floors'] = number_of_floors if number_of_floors else 'N/A'
    data['Legal Status'] = legal_status if legal_status else 'N/A'
    data['Interior'] = interior if interior else 'N/A'
    data['Listing Type'] = listing_type if listing_type else 'N/A'
    data['Listing ID'] = listing_id if listing_id else 'N/A'

    return data

def save_to_csv(data, filename):
    file_exists = os.path.isfile(filename)
    with open(filename, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=data.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(data)

def main(input_file, output_folder, filename):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    driver = initialize_driver()
    with open(input_file, 'r') as file:
        urls = [url.strip() for url in file.readlines()]

    for url in urls:
        try:
            capture_full_page_screenshot(driver, url, output_folder)
            html = get_html(driver, url)
            soup = parse_html(html)
            data = extract_data(soup)
            save_to_csv(data, filename)
            print(f"Đã lưu dữ liệu cho {url}")
        except Exception as e:
            print(f"Lỗi khi xử lý {url}: {e}")

    driver.quit()
    print(f"Dữ liệu đã được lưu vào {filename}")

if __name__ == '__main__':
    input_file = 'links_tong_hop_ha_dong.txt'
    output_folder = 'D:/FPTpoly/Kỳ 4/Dự án 1/Code/data_image_ha_dong'
    filename = 'Data_batdongsan_com_vn_ha_dong.csv'
    main(input_file, output_folder, filename)
