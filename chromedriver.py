import os
import zipfile

from selenium import webdriver
from selenium.webdriver.chrome.service import Service

PROXY_HOST = '45.140.13.119'  # rotating proxy or host
PROXY_PORT = 80 # port
PROXY_USER = 'zlmuzgxn' # username
PROXY_PASS = 'bx516jctkebo' # password


manifest_json = """
{
    "version": "1.0.0",
    "manifest_version": 2,
    "name": "Chrome Proxy",
    "permissions": [
        "proxy",
        "tabs",
        "unlimitedStorage",
        "storage",
        "<all_urls>",
        "webRequest",
        "webRequestBlocking"
    ],
    "background": {
        "scripts": ["background.js"]
    },
    "minimum_chrome_version":"22.0.0"
}
"""

background_js = """
var config = {
        mode: "fixed_servers",
        rules: {
        singleProxy: {
            scheme: "http",
            host: "%s",
            port: parseInt(%s)
        },
        bypassList: ["localhost"]
        }
    };

chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

function callbackFn(details) {
    return {
        authCredentials: {
            username: "%s",
            password: "%s"
        }
    };
}

chrome.webRequest.onAuthRequired.addListener(
            callbackFn,
            {urls: ["<all_urls>"]},
            ['blocking']
);
""" % (PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS)


def get_chromedriver(use_proxy=False, user_agent=None):
    path = os.path.dirname(os.path.abspath(__file__))
    option = webdriver.ChromeOptions()
    if use_proxy:
        pluginfile = 'proxy_auth_plugin.zip'

        with zipfile.ZipFile(pluginfile, 'w') as zp:
            zp.writestr("manifest.json", manifest_json)
            zp.writestr("background.js", background_js)
        #option.add_extension(pluginfile)
    if user_agent:
        option.add_argument('--user-agent=%s' % user_agent)
    
    chrome_prefs = {}
    #option.experimental_options["prefs"] = chrome_prefs
    chrome_prefs["profile.default_content_settings"] = {"images": 2}
    chrome_prefs["profile.managed_default_content_settings"] = {"images": 2} 
    service = Service('./chromedriver')   
    option.add_experimental_option("excludeSwitches", ["enable-automation"])
    option.add_experimental_option('useAutomationExtension', False)
    #option.add_argument('user-data-dir=/home/dev/personalProjects/upwork/jerry/tmp')
    #option.add_argument("profile-directory=profile")
    option.add_argument("--proxy-server=http://66.42.95.53:20417")
    option.add_argument("--headless") 
    driver = webdriver.Chrome(service=service, options=option)
    driver.maximize_window()
    return driver

def main():
    driver = get_chromedriver(use_proxy=True)
    #driver.get('https://www.google.com/search?q=my+ip+address')
    driver.get("https://whatismyipaddress.com/")
    import time
    time.sleep(5)
    pass

if __name__ == '__main__':
    main()
