"""
This script depends on this:
docker run -d -p 4444:4444 --shm-size="2g" selenium/standalone-chrome:4.27.0-20250101
"""
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


def get_content(url: str) -> str | None:
    """Fetch content from a WeChat article URL.
    
    Args:
        url: The WeChat article URL to fetch
        
    Returns:
        The article content as text if successful, None otherwise
    """
    options = ChromeOptions()
    options.set_capability('se:recordVideo', True)
    options.set_capability('se:screenResolution', '1920x1080')
    options.set_capability('se:name', 'test_visit_basic_auth_secured_page (ChromeTests)')

    # Add headless mode and other options to bypass restrictions
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument(
        '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    )

    # Try connecting to Selenium server, handle connection errors gracefully
    try:
        driver = webdriver.Remote(
            options=options,
            command_executor="http://localhost:4444/wd/hub"
        )
    except Exception as e:
        print(
            f"Failed to connect to Selenium server at localhost:4444 - {e}\n"
            "Make sure Docker is running and execute:\n"
            "docker run -d -p 4444:4444 --shm-size=\"2g\" selenium/standalone-chrome:4.27.0-20250101"
        )
        return None

    try:
        driver.get(url)

        # Wait for either the content or the error message to appear
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.rich_media_content, .weui-msg__title')))

            # Check if we got the error page
            error_elements = driver.find_elements(By.CSS_SELECTOR, '.weui-msg__title')
            if error_elements and "违规" in error_elements[0].text:
                return None

            # Extract the article content
            content = driver.find_element(By.CSS_SELECTOR, '.rich_media_content')
            return content.text

        except TimeoutException:
            return None

    finally:
        driver.quit()
