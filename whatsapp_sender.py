from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep


def create_driver(tel_number, text_message):
    options = webdriver.ChromeOptions()
    options.add_argument('--allow-profiles-outside-user-dir')
    options.add_argument('--enable-profile-shortcut-manager')
    options.add_argument(r'user-data-dir=C:\Program Files\Google\Chrome')
    options.add_argument('--profile-directory=Profile 1')
    options.add_argument('--profiling-flush=2592000')
    options.add_argument('--enable-aggressive-domstorage-flushing')

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=options)
    wait = WebDriverWait(driver, 30)

    url = f"https://web.whatsapp.com/send?phone={tel_number}&text={text_message}"
    driver.get(url)
    btn_path = '/html/body/div[1]/div/div/div[5]/div/footer/div[1]/div/span[2]/div/div[2]/div[2]/button'
    wait.until(EC.element_to_be_clickable((By.XPATH, btn_path)))
    driver.find_element(By.XPATH, btn_path).click()
    sleep(2)
