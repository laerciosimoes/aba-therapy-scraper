#!/usr/bin/env python3
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait


class ChromeDriverManager:
    """
    Manages the initialization and shutdown of the Chrome WebDriver.

    Attributes:
        driver: An instance of Selenium WebDriver.
        wait: A WebDriverWait instance for explicit waits.
    """

    def __init__(self, headless: bool = False, wait_time: int = 20) -> None:
        """
        Initializes Chrome with the specified options.

        :param headless: Boolean flag to run Chrome in headless mode.
        :param driver_path: Optional path to the chromedriver executable.
        :param wait_time: Timeout (in seconds) for explicit wait operations.
        """
        chrome_options: Options = Options()
        if headless:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        self.driver: webdriver.Chrome = webdriver.Chrome(options=chrome_options)

        self.driver.maximize_window()
        self.wait: WebDriverWait = WebDriverWait(self.driver, wait_time)

    def quit(self) -> None: 
        """
        Closes the Chrome WebDriver.
        """
        self.driver.quit()
