from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

s = Service(executable_path="D:\python\chromedriver.exe")
browser = webdriver.Chrome(service=s)

browser.get(url="http://orteil.dashnet.org/experiments/cookie/")
cookie = browser.find_element(By.ID, "cookie")
end_time = time.time() + 5 * 60
# price_list = [int(cost.get_attribute("textContent").split("-")[1].replace(",", "")) for cost in item_costs]

time_interval = time.time() + 5
while time.time() <= end_time:
    cookie.click()

    if time.time() >= time_interval:
        money = browser.find_element(By.ID, "money").text.replace(",", "")
        store_items = browser.find_elements(By.CSS_SELECTOR, "#store> div")
        item_costs = browser.find_elements(By.CSS_SELECTOR, "#store div b")

        store_dict = {num: {"id": store_items[num].get_attribute("id"),
                            "class": store_items[num].get_attribute("class"),
                            "price": int(item_costs[num].get_attribute("textContent").split("-")[1].replace(",", ""))}
                      for num in range(len(store_items))}

        active_list = []
        for key in store_dict.keys():
            if store_dict[key]["class"] != "grayed":
                active_list.append(store_dict[key])

        try:
            if int(money) > active_list[-1]["price"]:
                browser.find_element(By.ID, str(active_list[-1]["id"])).click()
        except IndexError:
            pass

        time_interval = time.time() + 5



print(f"cookies/second : {browser.find_element(By.ID, 'cps').text}")

browser.quit()
