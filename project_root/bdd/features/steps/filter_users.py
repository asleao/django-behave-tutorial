from behave import * # We'll need to import all from behave first
from accounts.factories import InterestFactory,UserFactory
from accounts.models import Interest

# Then we can copy the snippets into our file
@given('there are a number of interests')
def impl(context):
    interests = [InterestFactory(name=row['interest']) for row in context.table]

@given('there are many users, each with different interests')
def impl(context):
    for row in context.table:
        interest_names = row['interests'].split(', ')
        interests = Interest.objects.filter(name__in=interest_names)
        UserFactory(email=row['email'], interests=interests)

@given('I am a logged in user')
def impl(context):
    # First we need to create the user to login.
    user_to_login = UserFactory(email='log.me.in@test.test')
    # All properties (other than email) will be inherited from our UserFactory.
    # Therefore our password for this user will be 'pass'.

    # We visit the login page
    # context.config.server_url is by default set to http://localhost:8081
    # (Thanks to Cynthia Kiser for pointing this out.)
    # In this example we're visiting http://localhost:8081/accounts/login/
    context.browser.visit(context.config.server_url + 'accounts/login/')

    # Next, we log in our user by interacting with the login form
    # Splinter has a handy fill function that helps us fill form fields based
    # on their name.  We'll use it to fill in the username and password fields.
    context.browser.fill('username', user_to_login.email)
    context.browser.fill('password', 'pass')

    # Finally we find the submit button (by its CSS attribute) and click on it!
    context.browser.find_by_css('form input[type=submit]').first.click()

@when('I filter the list of users by "{checked}"')
def impl(context,checked):
    # First we visit the page where we see all the users.
    # In our example, this happens to be the root domain.
    context.browser.visit(context.context.config.server_url)

    # Then we get the list of interests
    checked = checked.split(', ');
    for check in checked:
        # And click on each label.
        # This code assumes we have a form where each interest is listed as a
        # label containing a checkbox.
        path = "//label[contains(.,'{}')]/input".format(check)
        context.browser.find_by_xpath(path).click()

    # Finally, we submit the form
    context.browser.find_by_css('form input[type=submit]').first.click()

@then('I see "{count}" users')
def impl(context,count):
    # Assuming there is a <div class="user-card"></div> for each user
    users = context.browser.find_by_css('.user-card')

    # We can now assert that the number of users on the page
    # is equal to the number we expect
    assert len(users) == int(count)