from amazon_config import (
    BASE_URL,
    DIRECTORY,
    NAME,
    FILTERS,
    CURRENCY,
    getChromeDriver,
    getChromeOptions,
    setBrowserIncognito,
    setHeadless,
    setIgnoreCertificateError
)
from selenium.webdriver.common.keys import Keys
import time
import pandas


class GenerateReport:
    def __init__(self, results_dict):
        formatted_results = pandas.DataFrame(
            results_dict, columns=['product id', 'product name', 'product price'])
        formatted_results.to_csv('product_results.csv', sep=',', index=False, encoding='utf-8')


class AmazonAPI:
    def __init__(self, search_term, filters, base_url, currency):
        self.base_url = base_url
        self.search_term = search_term
        options = getChromeOptions()
        setBrowserIncognito(options)
        setIgnoreCertificateError(options)
        self.driver = getChromeDriver(options)
        self.currency = currency
        self.price_filter = f"&rh=p_36%3A{filters['min']}00-{filters['max']}00"

    def run(self):
        print("Starting the script...")
        print(f"Looking for '{self.search_term}' in products ")
        links = self.get_product_links()
        print(f"{len(links)} links found")
        results = self.scrape_data(links)
        GenerateReport(results)

    def get_product_links(self):
        self.driver.get(self.base_url)
        search_box = self.driver.find_element_by_css_selector(
            '#twotabsearchtextbox')
        search_box.send_keys(self.search_term)
        search_box.send_keys(Keys.ENTER)
        self.driver.get(f"{self.driver.current_url}{self.price_filter}")
        time.sleep(2)  # wait for results to load

        products = self.driver.find_elements_by_css_selector(
            "span[cel_widget_id*='MAIN-SEARCH_RESULTS-1'] h2>a:not([aria-hidden])")
        product_links = []
        for product in products:
            product_links.append(product.get_attribute('href'))
        return product_links

    def scrape_data(self, links):
        results = {
            'product id': [],
            'product name': [],
            'product price': [],
        }
        for link in links:
            self.driver.get(link)
            product_id = self.driver.find_element_by_css_selector(
                "link[rel='canonical']").get_attribute('href').rsplit('/', 1)[1]
            results['product id'].append(product_id)
            name = self.driver.find_element_by_css_selector(
                '#productTitle').text.strip()
            results['product name'].append(name)
            price = 'N/A'
            try:
                price = self.driver.find_element_by_css_selector(
                    '#priceblock_ourprice').text.strip()
            except:
                print(f'Price not found for {product_id}')
            results['product price'].append(price)

        return results

    def quit_browser(self):
        self.driver.quit()


if __name__ == '__main__':
    amazon = AmazonAPI(NAME, FILTERS, BASE_URL, CURRENCY)

    try:
        amazon.run()
    except Exception as e:
        print(f"Error Occured: {e}")
    finally:
        amazon.quit_browser()
