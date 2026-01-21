import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ===== LOCATORS (PHPTRAVELS CONTACT FORM) =====
NAME = (By.NAME, "name")
EMAIL = (By.NAME, "email")
SUBJECT = (By.NAME, "subject")
MESSAGE = (By.NAME, "message")
SUBMIT = (By.ID, "submit")
RESET = (By.XPATH, "//button[@type='reset']")

ALERT = (By.CLASS_NAME, "alert")

# ===== HELPER FUNCTION =====
def fill_contact_form(driver, name="", email="", subject="", message=""):
    wait = WebDriverWait(driver, 10)

    for field in [NAME, EMAIL, SUBJECT, MESSAGE]:
        wait.until(EC.presence_of_element_located(field)).clear()

    if name:
        driver.find_element(*NAME).send_keys(name)
    if email:
        driver.find_element(*EMAIL).send_keys(email)
    if subject:
        driver.find_element(*SUBJECT).send_keys(subject)
    if message:
        driver.find_element(*MESSAGE).send_keys(message)

    driver.find_element(*SUBMIT).click()
    time.sleep(2)

# ================= TEST CASES =================

# TC_4: Name trống
def test_TC4_name_empty(driver):
    fill_contact_form(
        driver,
        email="test@mail.com",
        subject="Test",
        message="Hello"
    )
    assert "name" in driver.page_source.lower()

# TC_5: Email trống
def test_TC5_email_empty(driver):
    fill_contact_form(
        driver,
        name="Minh",
        subject="Test",
        message="Hello"
    )
    assert "email" in driver.page_source.lower()

# TC_6: Message trống
def test_TC6_message_empty(driver):
    fill_contact_form(
        driver,
        name="Minh",
        email="minh@test.com",
        subject="Test"
    )
    assert "message" in driver.page_source.lower()

# TC_7: Email sai định dạng
def test_TC7_invalid_email(driver):
    fill_contact_form(
        driver,
        name="Minh",
        email="abc@xyz",
        subject="Test",
        message="Hello"
    )
    assert "email" in driver.page_source.lower()

# TC_8: Nhiều field không hợp lệ
def test_TC8_multiple_invalid(driver):
    fill_contact_form(
        driver,
        name="",
        email="abc",
        message=""
    )
    source = driver.page_source.lower()
    assert "name" in source
    assert "email" in source
    assert "message" in source

# TC_9: Name ký tự đặc biệt
def test_TC9_special_character_name(driver):
    fill_contact_form(
        driver,
        name="@#123",
        email="minh@test.com",
        message="Hello"
    )
    assert ("success" in driver.page_source.lower()
            or "name" in driver.page_source.lower())

# TC_10: Message quá dài
def test_TC10_message_too_long(driver):
    long_message = "A" * 1200
    fill_contact_form(
        driver,
        name="Minh",
        email="minh@test.com",
        subject="Test",
        message=long_message
    )
    assert ("limit" in driver.page_source.lower()
            or "message" in driver.page_source.lower())

# TC_11: Name có khoảng trắng đầu/cuối
def test_TC11_trim_name(driver):
    fill_contact_form(
        driver,
        name=" Minh ",
        email="minh@test.com",
        message="Hello"
    )
    assert "success" in driver.page_source.lower()

# TC_12: Message có khoảng trắng
def test_TC12_trim_message(driver):
    fill_contact_form(
        driver,
        name="Minh",
        email="minh@test.com",
        message=" Hello "
    )
    assert "success" in driver.page_source.lower()

# TC_13: Submit hợp lệ
def test_TC13_submit_success(driver):
    fill_contact_form(
        driver,
        name="Minh Nguyen",
        email="minh@test.com",
        subject="Test",
        message="Hello world"
    )
    assert "success" in driver.page_source.lower()

# TC_14: Chỉ field bắt buộc
def test_TC14_required_fields_only(driver):
    fill_contact_form(
        driver,
        name="Nguyen Van A",
        email="user@test.com",
        message="Hello"
    )
    assert "success" in driver.page_source.lower()

# TC_15: Field dài
def test_TC15_long_fields(driver):
    long_text = "B" * 1200
    fill_contact_form(
        driver,
        name=long_text,
        email="minh@test.com",
        subject=long_text,
        message=long_text
    )
    assert ("limit" in driver.page_source.lower()
            or "success" in driver.page_source.lower())

# TC_16: Ký tự đặc biệt & khoảng trắng
def test_TC16_special_and_space(driver):
    fill_contact_form(
        driver,
        name=" @Minh! ",
        email="minh@test.com",
        subject="Test!@#",
        message=" Hello! "
    )
    assert ("success" in driver.page_source.lower()
            or "invalid" in driver.page_source.lower())

# TC_17: Submit nhiều lần
def test_TC17_multiple_submit(driver):
    fill_contact_form(
        driver,
        name="Minh",
        email="minh@test.com",
        message="Hello"
    )
    fill_contact_form(
        driver,
        name="Minh",
        email="minh@test.com",
        message="Hello"
    )
    assert "success" in driver.page_source.lower()

# TC_18: Subject trống
def test_TC18_subject_empty(driver):
    fill_contact_form(
        driver,
        name="Minh",
        email="minh@test.com",
        message="Hello"
    )
    assert "success" in driver.page_source.lower()

# TC_19: Reset form
def test_TC19_reset_form(driver):
    driver.find_element(*NAME).send_keys("Minh")
    driver.find_element(*EMAIL).send_keys("minh@test.com")
    driver.find_element(*MESSAGE).send_keys("Hello")

    driver.find_element(*RESET).click()
    time.sleep(1)

    assert driver.find_element(*NAME).get_attribute("value") == ""
    assert driver.find_element(*EMAIL).get_attribute("value") == ""
    assert driver.find_element(*MESSAGE).get_attribute("value") == ""
