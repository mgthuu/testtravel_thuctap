import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BookingPage:
    def __init__(self, driver):
        self.driver = driver
        # Tăng timeout lên 30 giây vì web demo rất chậm
        self.wait = WebDriverWait(self.driver, 30)

    # --- Locators ---
    EMAIL_INPUT = (By.NAME, "email")
    PASSWORD_INPUT = (By.NAME, "password")
    LOGIN_BTN = (By.XPATH, "//button[@type='submit']")
    SEARCH_INPUT = (By.CSS_SELECTOR, "input[type='search']")
    TABLE = (By.ID, "data")

    # --- Actions ---
    def login(self, email, password):
        self.driver.get("https://www.phptravels.net/login")
        # Nhập thông tin
        self.wait.until(EC.visibility_of_element_located(self.EMAIL_INPUT)).send_keys(email)
        self.driver.find_element(*self.PASSWORD_INPUT).send_keys(password)
        
        # Click Login
        btn = self.wait.until(EC.element_to_be_clickable(self.LOGIN_BTN))
        self.driver.execute_script("arguments[0].click();", btn)
        
        # Chờ đợi thông minh: Đợi URL thay đổi hoặc cookie được thiết lập
        time.sleep(5) 

    def navigate_to_bookings(self):
        self.driver.get("https://www.phptravels.net/bookings")
        # Đợi bảng xuất hiện
        self.wait.until(EC.presence_of_element_located(self.TABLE))

    def search_general(self, text):
        search_field = self.wait.until(EC.visibility_of_element_located(self.SEARCH_INPUT))
        search_field.clear()
        search_field.send_keys(text)

    def create_booking_data(self):
        """Tạo dữ liệu nhanh bằng cách truy cập thẳng link hotel"""
        self.driver.get("https://www.phptravels.net/hotels")
        time.sleep(3)