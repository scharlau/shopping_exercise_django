# A Shopping Exercise in Python with Django
A Python Django driven shopping example for deliberate practice

This is NOT a proper shopping site, but the back end of what one could be. It is missing the authentication and security aspects that you'd expect. The purpose of this is to let you explore how you retrieve and display the information that you want to show on the pages of the site.

The goal of 'deliberate practice' is to think about how you'd solve this challenge, and to work at developing code to make this work. There is no single 'correct' version of this code. The purpose of the exercise it become familiar with different ways of making the application work. You should explore how this simple application is done in Rails so that you understand how variables in controllers are show up in the views you see in the browser.

Under 'deliberate practice' we offer up the challenge, then think about options for developing a solution, and code for 12 minutes. After that we pause to discuss how people are approaching the problem, and what they're trying to do. This should be repeated three times and then wrapped up with time for people to express what they found most useful during the session. This should take an hour.

You can clone the repository for this application, and then add the required libraries, plus set up your environment. Start by cloning this repo to your own devise, using either the command line, or download it as zip file. Then open a terminal in the app's directory and use the commands below to get started.

## Set up your environment
 We can start developing our application to display the data. Create a new project folder called 'polar_bears' and then cd into the folder via the terminal and execute these commands:

        pyenv local 3.7.0 # this sets the local version of python to 3.7.0
        python3 -m venv .venv # this creates the virtual environment for you
        source .venv/bin/activate # this activates the virtual environment
        pip install --upgrade pip [ this is optional]  # this installs pip, and upgrades it if required.

We will use Django (https://www.djangoproject.com) as our web framework for the application. We install that with 
        
        pip install django

And that will install django version 3.1.3 with its associated dependencies. We can now start to build the application.

We can now add in some random content for the shopping application using the Faker library from https://pypi.org/project/Faker/. Install Faker with the command: 

        pip install Faker

Now we can set about changing the nouns, adjectives and other parts of mystory with values from Faker. Go to https://faker.readthedocs.io/en/stable/providers.html and look through the options for Standard Providers to see if you want to change any details in values used in setup_db.py.
