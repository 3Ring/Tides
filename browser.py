from selenium import webdriver

# Chrome
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By

from typing import Tuple
from selenium.webdriver.remote.webelement import WebElement


class Browser:
    def __init__(self, driver):
        self.driver = driver

    async def nav(self, url: str, next: str = None, timeout: int = 2) -> None:
        """
        The function navigates to a url and confirms that the browser has navigated to the correct url

        :param url: The URL to navigate to
        :param next: The URL where the browser will be redirected to
        """
        if next is None:
            next = url
        self.driver.get(url)
        await self._confirm_nav(next, timeout)

    async def _confirm_nav(self, url: str, timeout: int, partial_url: bool = False):
        """
        Wait for the URL to be the expected URL

        :param url: The URL to navigate to
        :param timeout: The amount of time (in seconds) we’re willing to wait for our target element to be found,
        defaults to 10
        :param partial_url: If you want to wait for a partial url, for example, if you want to wait for
        https://www.google.com/search?q=test, you can set partial_url=True, defaults to False
        """
        try:
            if partial_url:
                WebDriverWait(self.driver, timeout).until(
                    expected_conditions.url_contains(url)
                )
            else:
                WebDriverWait(self.driver, timeout).until(
                    expected_conditions.url_to_be(url)
                )
        except Exception as e:
            print(f"currrent url is: {self.driver.current_url}. expected is: {url}")
            raise e

    async def get_element(
        self, locator: Tuple[By, str], timeout: int = 2, is_hidden: bool = False
    ) -> WebElement:
        """
        Wait for the element to be present in the DOM and return its The WebElement object.

        :param locator: A tuple of the form (by, selector) where by is a By class and selector is a string
        :param timeout: The amount of time to wait for the element to be visible, defaults to 10
        :param is_hidden: If True, the element is expected to be hidden, defaults to False
        :return: The WebElement object.
        """
        el = WebDriverWait(self.driver, timeout).until(
            expected_conditions.presence_of_element_located(locator)
        )
        assert el.is_displayed() != is_hidden
        return el

    async def get_all_elements(
        self, locator: Tuple[By, str], timeout: int = 2
    ) -> list[WebElement]:
        """
        Wait for the all elements to be present in the DOM and return the WebElement objects in a list.
        Primarily used to make sure there is only one

        :param locator: A tuple of the form (by, selector) where by is a By class and selector is a string
        :param timeout: The amount of time to wait for the element to be visible, defaults to 10
        :return: The WebElement object.
        """
        els = WebDriverWait(self.driver, timeout).until(
            expected_conditions.presence_of_all_elements_located(locator)
        )
        return els

    def clear_cookies(self) -> None:
        self.driver.delete_all_cookies

    @staticmethod
    def make_chrome() -> webdriver.Chrome:
        """
        Create a Chrome webdriver with headless options
        :return: Chrome webdriver
        """
        options = ChromeOptions()
        options.headless = True
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(options=options, service=service)
        assert driver is not None
        return driver
