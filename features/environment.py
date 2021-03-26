from behave import fixture, use_fixture
import os, urllib
import django
from django.shortcuts import resolve_url
from django.test import selenium
from django.test.testcases import TestCase
from django.test.runner import DiscoverRunner
from django.test.testcases import LiveServerTestCase
# from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

os.environ["DJANGO_SETTINGS_MODULE"] = "mysite.settings"
django.setup()

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
    context.test = TestCase()
    context.test.setUpClass()
    use_fixture(django_test_case, context)

def after_scenario(context, scenario):
    context.test.tearDownClass()
    del context.test

def after_all(context):
    context.browser.quit()

@fixture
def django_test_runner(context):
    context.test_runner = DiscoverRunner()
    context.test_runner.setup_test_environment()
    context.old_db_config = context.test_runner.setup_databases()
    yield
    context.test_runner.teardown_databases(context.old_db_config)
    context.test_runner.teardown_test_environment()

@fixture
def django_test_case(context):
    context.test_case = LiveServerTestCase
    context.test_case.setUpClass()
    yield
    context.test_case.tearDownClass()
    del context.test_case