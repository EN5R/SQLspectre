import time
import random
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from concurrent.futures import ThreadPoolExecutor
import requests
import urllib.parse
from datetime import datetime

def print_banner():
    banner = r"""
		  ___  ___  _                    _           
		 / __|/ _ \| |   ____ __  ___ __| |_ _ _ ___ 
		 \__ \ (_) | |__(_-< '_ \/ -_) _|  _| '_/ -_)
		 |___/\__\_\____/__/ .__/\___\__|\__|_| \___|
		                   |_|                        
            
            			by @E5R with ❤
            							v1


	My Github Profile: 		https://github.com/EN5R
	My X Profile:			https://x.com/EN544R
	My Telegram Channel: 		https://t.me/+K3G9CJmZfShmOGI0
	My Buy Me a Coffee Page:	https://buymeacoffee.com/en5r
	
    """
    print(banner)

# ANSI escape kodlarıyla renkler
class Colors:
    INFO = "\033[92m"   # Yeşil (Bilgi mesajları)
    WARNING = "\033[93m"  # Sarı (Uyarılar)
    ERROR = "\033[91m"  # Kırmızı (Hatalar)
    VULNERABILITY = "\033[91m"  # Kırmızı (Zafiyetler)
    RESET = "\033[0m"   # Renk sıfırlama

# Loglama için kullanılan sınıf
class Logger:
    """Programın loglarını yönetir."""
    
    def __init__(self, log_file='scanner.log'):
        self.log_file = log_file
        self.setup_logging()

    def setup_logging(self):
        """Log dosyasını ayarlar."""
        if not os.path.exists(self.log_file):
            with open(self.log_file, 'w') as f:
                f.write("")

    def log(self, message, level='INFO'):
        """Mesajı log dosyasına yazar."""
        log_entry = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} [{level}] {message}"
        with open(self.log_file, 'a') as f:
            f.write(f"{log_entry}\n")
        print(log_entry)

# Payload dosyasını yöneten sınıf
class PayloadLoader:
    """Payload dosyasını yüklemek ve yönetmek için kullanılan sınıf."""
    
    def __init__(self, filepath):
        self.filepath = filepath
        self.payloads = []

    def load_payloads(self):
        """Payloadları dosyadan yükler."""
        if os.path.exists(self.filepath):
            with open(self.filepath, 'r') as file:
                self.payloads = [line.strip() for line in file.readlines() if line.strip()]
            print(f"{Colors.INFO}INFO: {len(self.payloads)} payloads loaded from {self.filepath}.{Colors.RESET}")
        else:
            print(f"{Colors.ERROR}ERROR: Payload file not found: {self.filepath}{Colors.RESET}")

    def get_payloads(self):
        """Yüklenen payloadları döndürür."""
        return self.payloads

# SQL Injection tarayıcı sınıfı
class SQLInjectionScanner:

    """SQL Injection tarayıcı sınıfı."""

    def __init__(self, url, payloads, headers=None, proxies=None, logger=None):
        self.url = url if url.endswith('?') else url + '?'
        self.payloads = payloads
        self.headers = headers if headers else {"User-Agent": "Mozilla/5.0"}
        self.proxies = proxies
        self.logger = logger
        self.start_time = time.time()  # Performance timing

    def scan(self):
        """Taramayı başlatır."""
        start_time = time.time()  # Taramayı başlatan zamanı alın

        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = {executor.submit(self.send_request, payload): payload for payload in self.payloads}

            for future in futures:
                payload = futures[future]
                try:
                    future.result()  # İş parçacığının sonucunu al
                except Exception as e:
                    self.logger.log(f"Error for payload '{payload}': {str(e)}", level="ERROR")

        elapsed_time = time.time() - start_time  # Geçen süreyi hesaplayın
        self.logger.log(f"{Colors.INFO}INFO: Scan completed in {elapsed_time:.2f} seconds.{Colors.RESET}")

    def send_request(self, payload):
        """Payload ile isteği gönderir."""
        try:
            encoded_payload = urllib.parse.quote(payload)
            target_url = f"{self.url}{encoded_payload}"
        
            # Proxy kullanımı
            proxy = self.rotate_proxies()
        
            response = requests.get(target_url, headers=self.headers, proxies=proxy)

            # Sadece 200 yanıt kodunu kontrol et
            if response.status_code == 200 and self.is_vulnerable(response.text):
                log_message = self.format_log_message(payload, response)
                self.logger.log(log_message, level=f"{Colors.VULNERABILITY}VULNERABILITY{Colors.RESET}")
        except requests.RequestException as req_err:
            self.logger.log(f"Request error for payload '{payload}': {str(req_err)}", level="ERROR")
        except Exception as e:
            self.logger.log(f"Unexpected error for payload '{payload}': {str(e)}", level="ERROR")

    def rotate_proxies(self):
        """Birden fazla proxy arasında dönüşümlü olarak geçiş yapar."""
        if self.proxies:
            proxy = random.choice(self.proxies)
            return {"http": proxy, "https": proxy}
        return None

    def is_vulnerable(self, response_text):
        """Yanıtın SQL hatası içerip içermediğini kontrol eder."""
        sql_error_keywords = [
            'syntax error', 'unrecognized token', 'near "', 'unterminated', 'access denied', 'table', 'column'
        ]
        return any(keyword in response_text.lower() for keyword in sql_error_keywords)

    def format_log_message(self, payload, response):
        """Loglanacak mesajı formatlar."""
        return (f"found:\n\n"
                f"Payload: {payload}\n\n"
                f"URL: {response.url}\n\n"
                f"Response Code: {response.status_code}\n\n"
                f"Response Snippet: {response.text[:100]}...\n\n"
                "----------------------------------\n\n")


class SeleniumWebDriver:
    """Selenium ile web otomasyonu gerçekleştiren sınıf."""
    
    def __init__(self, logger, driver_path="chromedriver", headless=True):
        self.logger = logger
        self.driver_path = driver_path
        self.headless = headless
        self.browser = self.setup_browser()

    def setup_browser(self):
        chrome_options = Options()
        if self.headless:
            chrome_options.add_argument("--headless")
        service = Service(executable_path=self.driver_path)
        browser = webdriver.Chrome(service=service, options=chrome_options)
        return browser

    def fetch_url(self, url):
        self.logger.log(f"{Colors.INFO}INFO: Fetching URL: {url}{Colors.RESET}")
        self.browser.get(url)
    
        try:
            # JavaScript'nin yüklenmesini bekleyin
            WebDriverWait(self.browser, 30).until(lambda driver: driver.execute_script('return document.readyState') == 'complete')

            # Belirli bir öğenin yüklenmesini bekleyin
            #WebDriverWait(self.browser, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "css-selector-of-an-element")))
        
            page_source = self.browser.page_source
            self.logger.log(f"Page Source Retrieved: {page_source[:100]}")
            return page_source
        except Exception as e:
            self.logger.log(f"{Colors.ERROR}ERROR: {str(e)}{Colors.RESET}")
            
    def close_browser(self):
        """Tarayıcıyı kapatır."""
        self.logger.log(f"{Colors.INFO}INFO: Closing browser.{Colors.RESET}")
        self.browser.quit()

# Kullanıcı etkileşimlerini yöneten sınıf
class UserInterface:
    """Kullanıcı ile etkileşim sağlayan sınıf."""
    
    def __init__(self):
        self.url = ''
        self.payload_file = ''
        self.use_proxy = None
        self.use_selenium = False

    def collect_input(self):
        """Kullanıcıdan gerekli bilgileri toplar."""
        self.url = input("Enter the target URL (with a parameter): ")
        self.payload_file = input("Enter the payload file path (e.g., payloads.txt): ")
        self.use_proxy = input("Enter proxy (leave blank if not used, or enter multiple separated by commas): ") or None
        self.use_selenium = input("Use Selenium for web automation? (y/n): ").lower() == 'y'


def main():
    """Ana fonksiyon."""
    print_banner()
    ui = UserInterface()
    ui.collect_input()

    loader = PayloadLoader(ui.payload_file)
    loader.load_payloads()
    payloads = loader.get_payloads()

    logger = Logger()

    if payloads:
        proxies = ui.use_proxy.split(",") if ui.use_proxy else None
        scanner = SQLInjectionScanner(ui.url, payloads, proxies=proxies, logger=logger)
        
        if ui.use_selenium:
            selenium_driver = SeleniumWebDriver(logger)
            logger.log(f"{Colors.INFO}INFO: Starting scan using Selenium on {ui.url}...{Colors.RESET}")
            page_source = selenium_driver.fetch_url(ui.url)
            logger.log(f"Page Source Retrieved: {page_source[:100]}")
            selenium_driver.close_browser()

        logger.log(f"{Colors.INFO}INFO: Starting scan on {ui.url}...{Colors.RESET}")
        scanner.scan()
        logger.log(f"{Colors.INFO}INFO: Scan complete.{Colors.RESET}")
    else:
        logger.log(f"{Colors.ERROR}ERROR: No payloads loaded. Exiting program.{Colors.RESET}")


# Programı başlat
if __name__ == "__main__":
    main()
