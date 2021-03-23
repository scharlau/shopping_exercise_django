# -- FILE: features/environment.py
from behave import use_fixture
from behave_fixtures import django_test_runner, django_test_case
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

os.environ["DJANGO_SETTINGS_MODULE"] = "mysite.settings"

# Use the chrome driver specific to your version of Chrome browser and put it in ./driver directory
# CHROME_DRIVER = os.path.join(os.path.join(os.path.dirname(__file__), 'driver'), 'chromedriver')
CHROME_DRIVER = os.path.join('driver/chromedriver')
chrome_options = Options()
# comment out the line below if you want to see the browser launch for tests
# possibly add time.sleep() if required
chrome_options.add_argument("--headless")
chrome_options.add_argument('--no-proxy-server')
chrome_options.add_argument("--proxy-server='direct://'")
chrome_options.add_argument("--proxy-bypass-list=*")

def before_all(context):
    use_fixture(django_test_runner, context)
    context.browser = webdriver.Chrome(options=chrome_options, executable_path=CHROME_DRIVER)
    context.browser.set_page_load_timeout(time_to_wait=200)

def before_scenario(context, scenario):
    use_fixture(django_test_case, context)