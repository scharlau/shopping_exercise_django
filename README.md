# A Shopping Exercise in Python with Django
A Python Django driven shopping example for deliberate practice

This is NOT a proper shopping site, but the back end of what one could be. It is missing the authentication and security aspects that you'd expect. The purpose of this is to let you explore how you retrieve and display the information that you want to show on the pages of the site.

The goal of 'deliberate practice' is to think about how you'd solve this challenge, and to work at developing code to make this work. There is no single 'correct' version of this code. The purpose of the exercise it become familiar with different ways of making the application work. You should explore how this simple application is done in Django so that you understand how variables in views are show up in the templates you see in the browser.

Under 'deliberate practice' we offer up the challenge, then think about options for developing a solution, and code for 12 minutes. After that we pause to discuss how people are approaching the problem, and what they're trying to do. This should be repeated three times and then wrapped up with time for people to express what they found most useful during the session. This should take an hour.

You can clone the repository for this application, and then add the required libraries, plus set up your environment. Start by cloning this repo to your own devise, using either the command line, or download it as zip file. Then open a terminal in the app's directory and use the commands below to get started.

## Set up your environment
 We can start developing our application to display the data. Create a new project folder called 'shopping' and then cd into the folder via the terminal and execute these commands:

        pyenv local 3.7.0 # this sets the local version of python to 3.7.0
        python3 -m venv .venv # this creates the virtual environment for you
        source .venv/bin/activate # this activates the virtual environment
        pip install --upgrade pip [ this is optional]  # this installs pip, and upgrades it if required.

We will use Django (https://www.djangoproject.com) as our web framework for the application. We install that with 
        
        pip install django

And that will install django version 3.1.3 with its associated dependencies. We can now start to build the application.

We can now add in some random content for the shopping application using the Faker library from https://pypi.org/project/Faker/. Install Faker with the command: 

        pip install Faker

Now we can use Faker to generate customer and product details in the 'shop/management/commands/populate_tables.py' file. Go to https://faker.readthedocs.io/en/stable/providers.html and look through the options for Standard Providers to see if you want to change any details in values used.

You should now be able to populate the tables with the command:

        python3 manage.py populate_tables

Then you can start the server to see it running. 

##  Doing the Work

Work through the three rounds with a partner, or on your own, depending upon your circumstances. Each round should be twelve minutes, followed by a discussion of where you are and what has been working, as well as, what you're working on next.

You may want to refer to the shop/models.py file to understand the database schema before you get started. Some of you might even want to diagram the schema. 

You might also want to spend a few minutes at the start of each round planning what you might want to do.

You'll see that this version works with the objects in the shop/models.py file to manipulate the data we display on the page. This means we've mostly abstracted away the SQL, and are working with objects for our queries and the dislay of results.

There are some forms here for the products. These add the basic CRUD methods (create, read, update and delete). You could add similar ones for other objects.

## Behave added for BDD

This adds driver directory, and features, with steps directory.
We can now add the testing library Behave, along with Selenium for and the appropriate web drivers for your system, which you can find at https://selenium-python.readthedocs.io/installation.html#drivers Then put the binary at driver/chromedriver in your app, as you see in the repo. 

If you're on a Mac, then you will need to remove the chrome driver from quarantine with the command

        xattr -d com.apple.quarantine <name-of-executable>

as found and detailed at https://stackoverflow.com/questions/60362018/macos-catalinav-10-15-3-error-chromedriver-cannot-be-opened-because-the-de 

You might want to look at the documentation for Behave https://behave.readthedocs.io/en/latest/ 
You should look at Selenium documentation for [navigating web pages] (https://www.selenium.dev/selenium/docs/api/py/webdriver_remote/selenium.webdriver.remote.webdriver.html#module-selenium.webdriver.remote.webdriver)

### Codio options
If doing this on Codio, then you can add the chromedriver as follows, first before downloading the driver:
Open a terminal and install the chromium browser with the command:

        sudo apt-get install -y chromium-browser

This will install the browser plus its required libraries. If that still shows missing libraries, then use this command for the rest. Hopefully, they were installed with the browser, but they might not have been.

        sudo apt-get install -y libglib2.0-0 libnss3 libgconf-2-4 libfontconfig1

This should now give you chrome. You now can look over the install log in the terminal to see which version number of the chromedriver that you need to install in the driver folder.

## Modifying the Example to Include Authentication
The example would benefit from being more of a true e-commerce site. This meant making some changes as detailed below.

#### Changing the database
In order to do this, the database needed to be migrated, and as it's using sqlite3, it got in a tangle, The steps on how to reset migrations using scenario 1 at https://simpleisbetterthancomplex.com/tutorial/2016/07/26/how-to-reset-migrations.html along with documentation on the manage.py commands.

### Customers and Staff members
Build on the django User model detailed at https://docs.djangoproject.com/en/3.1/ref/contrib/auth/#django.contrib.auth.models.User which will be all members, and 'staff' will have 'is_staff' set to True. See also https://docs.djangoproject.com/en/3.1/topics/auth/default/ for details.
The best explanation of this is at https://blog.crunchydata.com/blog/extending-djangos-user-model-with-onetoonefield while https://dev.to/coderasha/create-advanced-user-sign-up-view-in-django-step-by-step-k9m had more details on creating the signup form and details about integrating the user and customer models.

This changed the customer model so that it extended the main user model. This impacted the way the model instances are created, and how they are retrieved for display. The fields used in the templates to display the list of customer, and their detail pages, also needed modification.

The registration and login approaches were borrowed from https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Authentication, which cover lots of useful materials.

### The Payment System 
This uses sessions to put items into a basket, which can be seen via 'Basket' link, and then shifted to 'Purchase' with user details. A value object holds items in basket for moving through to payments. After purchase the basket is cleared.

A better version would allow customers to remove items from the basket, and to specify their shipping address.





### The Exercises

1. Round one should be fixing the order_detail.html page to show names of items and customers, who placed the order. If you have time, then you can also fix the customer_details.html page to show the customer's orders, and let them click through to the order_details.html page.
2. Round two should be creating a 'dashboard' page to show the total value of orders placed by customers.
3. Round three is making round two work when you scale up the database by changing the numbers in the loops for the hop/management/commands/populate_tables.py file to work with 50 customers and orders of 10 items per customer.
