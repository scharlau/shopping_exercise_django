# A Shopping Exercise in Python with Django

A Python Django driven shopping example for deliberate practice

Django follows a model-view-controller architecture so that you can put code in a 'good' place for reuse. However, in Django the names are different. Models are models, views in Django are controllers, and it uses templates as views. Remember this as we go forward and it will help to keep things clearer.

This is NOT a proper shopping site, but the back end of what one could be. It has some of the authentication and security aspects that you'd expect using what's available in Django. The current implementation probably needs more refinement, but works as a starting point for an example. The purpose of this is to let you explore how you retrieve and display the information that you want to show on the pages of the site.

The goal of 'deliberate practice' is to think about how you'd solve this challenge, and to work at developing code to make this work. There is no single 'correct' version of this code. The purpose of the exercise is to become familiar with different ways of making the application work. You should explore how this simple application is done in Django so that you understand how variables in views are shown in the templates you see in the browser.

Under 'deliberate practice' we offer up the challenge, then think about options for developing a solution, and code for 12 minutes. After that we pause to discuss how people are approaching the problem, and what they're trying to do. This should be repeated three times and then wrapped up with time for people to express what they found most useful during the session. This should take an hour.

You can clone the repository for this application, and then add the required libraries, plus set up your environment. Start by cloning this repo to your own device, using either the command line, or download it as zip file. Then open a terminal in the app's directory and use the commands below to get started.

## Set up your environment
 We can start developing our application to display the data. In Codio, create a new project folder called 'shopping' and then cd into the folder via the terminal and execute these commands:

        pyenv local 3.7.0 # this sets the local version of python to 3.7.0
        python3 -m venv .venv # this creates the virtual environment for you
        source .venv/bin/activate # this activates the virtual environment
        pip install --upgrade pip [ this is optional]  # this installs pip, and upgrades it if required.

If you use another IDE, please check its documentation on how to setup a virtual environment.

We will use Django (https://www.djangoproject.com) as our web framework for the application. We install that with 
        
        pip install django

That will install the latest django version with its associated dependencies. We can now start to build the application.

We can now add in some random content for the shopping application using the Faker library from https://pypi.org/project/Faker/. Install Faker with the command: 

        pip install Faker

Now we can use Faker to generate customer and product details in the 'shop/management/commands/populate_tables.py' file. Go to https://faker.readthedocs.io/en/stable/providers.html and look through the options for Standard Providers to see if you want to change any details in values used.

You should now be able to populate the tables with the command:

        python3 manage.py populate_tables

Then you can start the server to see it running. 

You will need to create a superuser as well if you want to work with the admin features. You can do that with the command:

        python3 manage.py createsuperuser

Otherwise each customer created is also a user with a default password set in the management/commands/populate_tables.py file.

# Updated Features
Following the basic start of this repo, I saw the need to modify it for use to serve a few more situations. To that end it now also represents an example of working with BDD style testing using Behave, and there is a discussion about the changes made to enable authentication, which wasn't originally included.

## Behave added for BDD
This adds driver directory and features with steps directory.
We can now add the testing library Behave, along with Selenium and the appropriate web drivers for your system, which you can find at https://selenium-python.readthedocs.io/installation.html#drivers Then put the binary at driver/chromedriver in your app, as you see in the repo. If you use another Browser, you need to use another webdriver (e.g. geckodriver for Firefox) and adopt the environment.py accordingly.

You might want to look at the documentation for Behave https://behave.readthedocs.io/en/latest/ 
You should look at Selenium documentation for [navigating web pages] (https://www.selenium.dev/selenium/docs/api/py/webdriver_remote/selenium.webdriver.remote.webdriver.html#module-selenium.webdriver.remote.webdriver)

#### Codio options for Behave
If doing this on Codio, then you can add the chromedriver as follows from the command line before downloading the driver:
Open a terminal and install the chromium browser with the command:

        sudo apt-get install -y chromium-browser

This will install the browser plus its required libraries. If that still shows missing libraries, then use this command for the rest. Hopefully, they were installed with the browser, but they might not have been.

        sudo apt-get install -y libglib2.0-0 libnss3 libgconf-2-4 libfontconfig1

This should now give you chrome. You now can look over the install log in the terminal to see which version number of the chromedriver that you need to install in the driver folder.

#### Mac OS options for Behave
If you're on a Mac, then you will need to remove the chrome driver from quarantine with the command

        xattr -d com.apple.quarantine <name-of-executable>

as found and detailed at https://stackoverflow.com/questions/60362018/macos-catalinav-10-15-3-error-chromedriver-cannot-be-opened-because-the-de 

## Changing the database
In order to add authentication based on the built-in User model of Django, the database needed to be migrated, and as it's using sqlite3, it got in a tangle. This includes steps on how to reset migrations using scenario 1 at https://simpleisbetterthancomplex.com/tutorial/2016/07/26/how-to-reset-migrations.html along with documentation on the manage.py commands. You can avoid this by setting up your application using the User model from the beginning as set out below.

### Customers and Staff members
Build on the django User model detailed at https://docs.djangoproject.com/en/4.0/ref/contrib/auth/#django.contrib.auth.models.User which will be all members, and 'staff' will have 'is_staff' set to True. See also https://docs.djangoproject.com/en/4.0/topics/auth/default/ for details.
The best explanation of this is at https://blog.crunchydata.com/blog/extending-djangos-user-model-with-onetoonefield while https://dev.to/coderasha/create-advanced-user-sign-up-view-in-django-step-by-step-k9m had more details on creating the signup form and details about integrating the user and customer models.

This changed the customer model so that it extended the main user model. This impacted the way the model instances are created, and how they are retrieved for display. The fields used in the templates to display the list of customer, and their detail pages, also needed modification. You can see this if you look at the history of the models.py and populate_tables.py files.

Changes were also made to settings.py in order to add details for the LOGIN_REDIRECT_URL = '/' and LOGOUT_REDIRECT_URL = '/' so that they wouldn't default to the one for admin. With this in place, then new login and logout templates could be used, and people would end up at a suitable page during the login process.

The registration and login approaches were borrowed from https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Authentication, which uses the built-in AuthenticationForm https://docs.djangoproject.com/en/4.0/topics/auth/default/ of Django. The Mozilla documents cover lots of useful materials. Do look at these for more options that you might find useful too.

### The Payment System 
This uses sessions to put items into a basket, which can be seen via 'Basket' link, and then shifted to 'Purchase' with user details. This is based in part on the example at https://github.com/PacktPublishing/Django-3-by-Example/tree/master/Chapter08 [note: I kept this old link intentionally, since it has been referenced as a source, the new link would be https://github.com/PacktPublishing/Django-4-by-example/tree/main/Chapter08] from a book of the same name.

A key for the basket is set in settings.py, which will be unique for each shopper.
A person needs an account before they can see the payment page.

### There is still more to do with this
This still needs more work. There is currently no way to set up admin users, other than using the admin system to change users to 'staff', who could then see a dashboard of orders, and customers. The dashboard that's there is a placeholder, which only 'is_staff' can see. You can look at this other repo for ideas of how to add visuals to it https://github.com/scharlau/polar_bears_django_visuals based on what you find interesting.

A better version would only allow staff to remove and edit the products too. Ideally, there should be more tests too. It would've made developing these extra parts easier if tests showed where the pages 'broke' as parts were added.
Oh, and the stuff from faker adds extra characters, which is a pain. Those need to be cleaned up.

##  Doing the Work
Work through the three rounds with a partner, or on your own, depending upon your circumstances. Each round should be twelve minutes, followed by a discussion of where you are and what has been working, as well as, what you're working on next.

You may want to refer to the shop/models.py file to understand the database schema before you get started. Some of you might even want to diagram the schema. 

You might also want to spend a few minutes at the start of each round planning what you might want to do.

You'll see that this version works with the objects in the shop/models.py file to manipulate the data we display on the page. This means we've mostly abstracted away the SQL, and are working with objects for our queries and the dislay of results.

There are some forms here for the products. These add the basic CRUD methods (create, read, update and delete). You could add similar ones for other objects.

## The Exercises

1. Round one should be fixing the order_detail.html page to show names of items and customers, who placed the order. If you have time, then you can also fix the customer_details.html page to show the customer's orders, and let them click through to the order_details.html page, which also needs more details added so customers/staff can see items.
2. Round two should be implementing the 'dashboard' page to show the total value of orders placed by customers.
3. Round three is adding it so that customers can see their own orders.
