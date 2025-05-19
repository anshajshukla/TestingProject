"""
Driver factory to create and configure WebDriver instances.
"""
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from utils.config import BROWSER, HEADLESS

def get_driver():
    """
    Create and return a WebDriver instance based on config settings.
    Returns:
        WebDriver: Configured browser driver instance
    """
    if BROWSER.lower() == "chrome":
        options = webdriver.ChromeOptions()
        if HEADLESS:
            options.add_argument("--headless")
        options.add_argument("--start-maximized")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()),
            options=options
        )
    elif BROWSER.lower() == "firefox":
        options = webdriver.FirefoxOptions()
        if HEADLESS:
            options.add_argument("--headless")
        driver = webdriver.Firefox(
            service=FirefoxService(GeckoDriverManager().install()),
            options=options
        )
    elif BROWSER.lower() == "edge":
        options = webdriver.EdgeOptions()
        if HEADLESS:
            options.add_argument("--headless")
        driver = webdriver.Edge(
            service=EdgeService(EdgeChromiumDriverManager().install()),
            options=options
        )
    else:
        raise ValueError(f"Unsupported browser: {BROWSER}")
    
    return driver
