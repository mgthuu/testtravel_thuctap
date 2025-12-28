import pytest
import time
from pages.booking_page import BookingPage
from selenium.webdriver.common.by import By

class TestPHPTravelsBookings:

    @pytest.fixture(scope="class", autouse=True)
    def setup_data(self, driver):
        page = BookingPage(driver)
        # 1. Login
        page.login("user@phptravels.com", "demouser")
        
        # 2. Kiểm tra dữ liệu tại /bookings
        try:
            page.navigate_to_bookings()
            # Nếu thấy dòng 'No data available', đi tạo booking
            if "No data available" in driver.page_source:
                page.create_booking_data()
                page.navigate_to_bookings()
        except Exception as e:
            print(f"Lỗi khi chuẩn bị dữ liệu: {e}")
            page.navigate_to_bookings()

    def test_gui_elements(self, driver):
        """Kiểm tra giao diện bảng - TC_01"""
        page = BookingPage(driver)
        page.navigate_to_bookings()
        table = driver.find_element(By.ID, "data")
        assert table.is_displayed()

    @pytest.mark.parametrize("search_key", ["Paid", "Confirmed"])
    def test_search_functionality(self, driver, search_key):
        """Kiểm tra tìm kiếm - TC_14"""
        page = BookingPage(driver)
        page.search_general(search_key)
        time.sleep(3) # Chờ bảng lọc
        table_text = driver.find_element(By.ID, "data").text
        if "No matching records" not in table_text:
            assert search_key.lower() in table_text.lower()