with open("urls_batdongsan.txt", "w") as file:
    base_url = "https://batdongsan.com.vn/nha-dat-ban-hai-ba-trung/p"
    for page in range(1, 371):
        url = f"{base_url}{page}"
        file.write(url + "\n")
