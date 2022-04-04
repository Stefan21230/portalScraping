import pytest
from pytest import fixture
from selenium import webdriver
from selenium.webdriver.chrome.service import Service


@fixture(scope="class")  # the browser will load only once for all the test cases as its scope is class level
def setup(request, initialize_driver):
    driver = initialize_driver
    # driver.maximize_window()
    driver.get("https://jnportal.ujn.gov.rs")
    request.cls.driver = driver
    yield
    driver.close()
    driver.quit()


@fixture(scope="class")
def initialize_driver(browser):

    # Chrome options

    opt_chrome = webdriver.ChromeOptions()
    opt_chrome.add_argument("--start-maximized")
    # opt_chrome.add_argument("--headless")

    # Firefox options

    opt_firefox = webdriver.FirefoxOptions()
    opt_firefox.add_argument("--start-maximized")

    if browser not in ["chrome", "firefox"]:
        raise Exception(f"{browser} this browser is not supported")

    # Browser selector is based on @fixtures/addoption
    if browser == "chrome":
        driver = webdriver.Chrome(service=Service(r"C:\Chrome driver\chromedriver.exe"), options=opt_chrome)
        driver.implicitly_wait(10)
        return driver
    elif browser == "firefox":
        driver = webdriver.Firefox(options=opt_firefox)
        driver.implicitly_wait(10)
        return driver


def pytest_addoption(parser):
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        help="browsers: chrome, firefox"
    )


@fixture(scope="session")
def browser(request):
    browser = request.config.getoption("--browser")
    return browser
