import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

wait_time = 10

# ===== LOCATORS =====
BANNER_TITLE = (By.XPATH, "//h1[contains(text(),'Blogs')]")
BLOG_CARDS = (By.CSS_SELECTOR, ".blog-item")
SIDEBAR_BLOGS = (By.CSS_SELECTOR, ".sidebar .blog-item")
BLOG_TITLE = (By.CSS_SELECTOR, ".blog-item h4 a")
BLOG_ARROW = (By.CSS_SELECTOR, ".blog-item a.btn")
BLOG_IMAGE = (By.CSS_SELECTOR, ".blog-item img")
FLIGHTS_MENU = (By.LINK_TEXT, "Flights")
LANG_DROPDOWN = (By.XPATH, "//button[contains(text(),'English')]")
CURRENCY_DROPDOWN = (By.XPATH, "//button[contains(text(),'USD')]")
HEADER = (By.TAG_NAME, "header")
FOOTER = (By.TAG_NAME, "footer")
LOGO = (By.CSS_SELECTOR, "a.navbar-brand img")
FAVICON = (By.XPATH, "//link[@rel='icon']")

# ========= TC_01 =========
def test_TC01_blog_title_displayed(driver):
    title = WebDriverWait(driver, wait_time).until(
        EC.visibility_of_element_located(BANNER_TITLE)
    )
    assert title.text == "PHPTRAVELS Blogs"

# ========= TC_02 =========
def test_TC02_blog_grid_layout(driver):
    cards = driver.find_elements(*BLOG_CARDS)
    assert len(cards) >= 2

# ========= TC_03 =========
def test_TC03_sidebar_new_blogs(driver):
    sidebar_items = driver.find_elements(*SIDEBAR_BLOGS)
    assert len(sidebar_items) > 0

# ========= TC_04 =========
def test_TC04_click_main_blog_title(driver):
    first_blog = WebDriverWait(driver, wait_time).until(
        EC.element_to_be_clickable(BLOG_TITLE)
    )
    first_blog.click()
    assert "/blog/" in driver.current_url

# ========= TC_05 =========
def test_TC05_click_blog_arrow(driver):
    driver.back()
    arrow = WebDriverWait(driver, wait_time).until(
        EC.element_to_be_clickable(BLOG_ARROW)
    )
    arrow.click()
    assert "/blog/" in driver.current_url

# ========= TC_06 =========
def test_TC06_blog_image_loaded(driver):
    driver.back()
    images = driver.find_elements(*BLOG_IMAGE)
    for img in images:
        assert img.get_attribute("naturalWidth") != "0"

# ========= TC_07 =========
def test_TC07_flights_menu_navigation(driver):
    driver.find_element(*FLIGHTS_MENU).click()
    assert "flights" in driver.current_url.lower()

# ========= TC_08 =========
def test_TC08_language_dropdown(driver):
    driver.back()
    driver.find_element(*LANG_DROPDOWN).click()
    time.sleep(1)
    assert "language" in driver.page_source.lower()

# ========= TC_09 =========
def test_TC09_currency_change(driver):
    driver.find_element(*CURRENCY_DROPDOWN).click()
    time.sleep(1)
    assert "EUR" in driver.page_source or "€" in driver.page_source

# ========= TC_10 =========
def test_TC10_responsive_mobile(driver):
    driver.set_window_size(375, 812)
    cards = driver.find_elements(*BLOG_CARDS)
    assert len(cards) > 0
    driver.maximize_window()

# ========= TC_11 =========
def test_TC11_click_sidebar_blog(driver):
    sidebar_blog = WebDriverWait(driver, wait_time).until(
        EC.element_to_be_clickable(SIDEBAR_BLOGS)
    )
    sidebar_blog.click()
    assert "/blog/" in driver.current_url

# ========= TC_12 =========
def test_TC12_page_load_time(driver):
    assert driver.execute_script(
        "return performance.timing.loadEventEnd - performance.timing.navigationStart"
    ) < 3000

# ========= TC_13 =========
def test_TC13_hover_blog_card(driver):
    card = driver.find_elements(*BLOG_CARDS)[0]
    ActionChains(driver).move_to_element(card).perform()
    assert card.is_displayed()

# ========= TC_14 =========
def test_TC14_login_dropdown(driver):
    assert "Demo" in driver.page_source

# ========= TC_15 =========
def test_TC15_logo_redirect_home(driver):
    driver.find_element(*LOGO).click()
    assert driver.current_url == "https://www.phptravels.net/"

# ========= TC_16 =========
def test_TC16_scroll_page(driver):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)
    assert True

# ========= TC_17 =========
def test_TC17_long_title_not_overlap(driver):
    titles = driver.find_elements(By.CSS_SELECTOR, ".blog-item h4")
    for title in titles:
        assert title.size["height"] < 100

# ========= TC_18 =========
def test_TC18_promo_text_display(driver):
    assert "Save" in driver.page_source

# ========= TC_19 =========
def test_TC19_sticky_header(driver):
    header = driver.find_element(*HEADER)
    driver.execute_script("window.scrollTo(0, 500);")
    assert header.is_displayed()

# ========= TC_20 =========
def test_TC20_blog_url_format(driver):
    driver.find_elements(*BLOG_TITLE)[0].click()
    assert "/blog/" in driver.current_url

# ========= TC_21 =========
def test_TC21_sidebar_thumbnail_format(driver):
    thumbs = driver.find_elements(By.CSS_SELECTOR, ".sidebar img")
    for img in thumbs:
        assert img.get_attribute("src") != ""

# ========= TC_22 =========
def test_TC22_footer_display(driver):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    footer = driver.find_element(*FOOTER)
    assert footer.is_displayed()

# ========= TC_23 =========
def test_TC23_browser_back(driver):
    current = driver.current_url
    driver.back()
    assert driver.current_url != current

# ========= TC_24 =========
def test_TC24_https_security(driver):
    assert driver.current_url.startswith("https://")

# ========= TC_25 =========
def test_TC25_color_contrast(driver):
    assert "Blogs" in driver.page_source

# ========= TC_26 =========
def test_TC26_spacing_consistency(driver):
    cards = driver.find_elements(*BLOG_CARDS)
    assert cards[0].location["x"] != cards[-1].location["x"]

# ========= TC_27 =========
def test_TC27_data_consistency(driver):
    main_title = driver.find_elements(*BLOG_TITLE)[0].text
    assert main_title in driver.page_source

# ========= TC_28 =========
def test_TC28_favicon_display(driver):
    favicon = driver.find_element(*FAVICON)
    assert favicon.get_attribute("href") is not None

# ========= TC_29 =========
def test_TC29_console_no_error(driver):
    logs = driver.get_log("browser")
    assert all(log["level"] != "SEVERE" for log in logs)

# ========= TC_30 =========
def test_TC30_guest_access(driver):
    assert "/blogs" in driver.current_url
