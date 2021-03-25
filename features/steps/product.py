import urllib
from urllib.parse import urljoin, urlparse
from behave import given, when, then
from django.conf import settings
from django.shortcuts import resolve_url

# examples pulled from:
# https://www.selenium.dev/selenium/docs/api/py/webdriver_remote/selenium.webdriver.remote.webelement.html?highlight=send%20keys
# https://www.selenium.dev/selenium/docs/api/py/webdriver_remote/selenium.webdriver.remote.webdriver.html#module-selenium.webdriver.remote.webdriver


@given( "we want to add a product")
def user_on_product_newpage(context):
    base_url = urllib.request.url2pathname(context.test_case.live_server_url)
    print(base_url)
    open_url = urljoin(base_url,'/product_new/')
    context.browser.get(open_url)


@when( "we fill in the form")
def user_fills_in_the_form(context):
    # use print(context.browser.page_source) to aid debugging
    print(context.browser.page_source)
    name_textfield = context.browser.find_element_by_name('name')
    name_textfield.send_keys('thing one')
    price_textfield = context.browser.find_element_by_name('price')
    price_textfield.send_keys(3)
    context.browser.find_element_by_name('submit').click()

@then( "it succeeds")
def product_added(context):
    assert 'thing one' in context.browser.page_source