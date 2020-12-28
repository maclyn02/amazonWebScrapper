from selenium import webdriver

DIRECTORY = 'reports'
NAME = 'PS4'
CURRENCY = '£'
MIN_PRICE = '200'
MAX_PRICE = '600'
FILTERS = {
    'min': MIN_PRICE,
    'max': MAX_PRICE
}
BASE_URL = 'https://www.amazon.co.uk/'


def getChromeDriver(options):
    return webdriver.Chrome('./chromedriver', chrome_options=options)

def getChromeOptions():
    return webdriver.ChromeOptions()

def setIgnoreCertificateError(options):
    options.add_argument('--ignore-certificate-errors')

def setBrowserIncognito(options):
    options.add_argument('--incognito')

def setHeadless(options):
    options.add_argument('--headless')