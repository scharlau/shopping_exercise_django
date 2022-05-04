import urllib
from urllib.parse import urljoin, urlparse
from behave import given, when, then, model
from django.conf import settings
from django.shortcuts import resolve_url

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

@given(u'we have specific products to add')
def specific_products(context):
    base_url = urllib.request.url2pathname(context.test_case.live_server_url)
    open_url = urljoin(base_url,'/product_new/')
    for row in context.table:
        context.browser.get(open_url)
        name_textfield = context.browser.find_element_by_name('name')
        name_textfield.send_keys(row['name'])
        price_textfield = context.browser.find_element_by_name('price')
        price_textfield.send_keys(row['price'])
        context.browser.find_element_by_name('submit').click()
        assert row['name'] in context.browser.page_source
       
@when(u'we visit the listing page')
def step_impl(context):
    base_url = urllib.request.url2pathname(context.test_case.live_server_url)
    open_url = urljoin(base_url,'/product_list')
    context.browser.get(open_url)
    print(context.browser.page_source)
    assert 'Product List' in context.browser.page_source

@then(u'we will find \'another thing\'')
def step_impl(context):
    assert 'another thing' in context.browser.page_source