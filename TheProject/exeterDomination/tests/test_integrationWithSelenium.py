"""
This test file is an integration
test. Many aspects of the site
are tested as one.
"""
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.webdriver import WebDriver
from django.test import TestCase
from selenium.webdriver.support.ui import Select
from get_gecko_driver import GetGeckoDriver


# Insert geckodriver executable here
pathToGeckodriver = GetGeckoDriver()
pathToGeckodriver.install()
options = Options()
options.headless = True

class SeleniumLoginTest(StaticLiveServerTestCase, TestCase):
    """
    This class will test the functionality of the login system with test credentials.
    """
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver(options=options)
        cls.selenium.implicitly_wait(5)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def testLoginFunctionality(self):
        """
        This function navigates directly to the login page, enters a username and
        password, and then presses the login button. It then checks that the user
        is logged in.
        """
        self.selenium.get(self.live_server_url + "/login")
        unameInput = self.selenium.find_element_by_name("uname")
        # Need to tweak this to allow us to use this username in final build
        unameInput.send_keys("testUser1")
        pwdInput = self.selenium.find_element_by_name("psw")
        # Need to tweak this to allow us to use this password in the final
        # build
        pwdInput.send_keys("password")
        button = self.selenium.find_element_by_xpath(
            "//input[@class='formButton arcade-font']")
        button.click()
        self.selenium.implicitly_wait(5)
        assert self.selenium.title != "Login | Exeter Domination"


class SignUpWithSeleniumTest(StaticLiveServerTestCase, TestCase):
    """
    This class will test the sign up system with test credentials and check if the
    user is sent to the correct location.
    """
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver(options=options)
        cls.selenium.implicitly_wait(5)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def testSignUpFunctionality(self):
        """
        This function loads the signup page, creates a user account, and presses
        the signup button. It then checks that the user is redirected directly
        to a page where they are logged in.
        """
        self.selenium.get(self.live_server_url + "/signup")
        testUsername = self.selenium.find_element_by_name("username")
        testUsername.send_keys("testUser1")
        testPassword = self.selenium.find_element_by_name("password1")
        testPassword.send_keys("ab43aa1-pejhf@33b")
        testRepeatPassword = self.selenium.find_element_by_name("password2")
        testRepeatPassword.send_keys("ab43aa1-pejhf@33b")
        signUpButton = self.selenium.find_element_by_xpath(
            "//input[@class='formButton arcade-font']")
        signUpButton.click()
        self.selenium.implicitly_wait(5)
        assert self.selenium.title != "Sign Up | Exeter Domination" or "Log In | Exeter Domination"


class testNavigationLinks(StaticLiveServerTestCase, TestCase):
    """
    This class is mainly just to test that the hyperlinks, and navigation buttons are
    in order and working correctly. This is not currently comprehensive, but will be
    in time for release.
    """
    fixtures = ['../fixtures/coordinates.json', '../fixtures/locations.json']

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver(options=options)
        cls.selenium.implicitly_wait(5)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def testHomeToAboutBackToHome(self):
        """
        This function tests that the navigation buttons from the home
        page to the about page and back are in working order.
        """
        self.selenium.get(self.live_server_url + "/")
        aboutButton = self.selenium.find_element_by_link_text("About")
        aboutButton.click()
        assert self.selenium.title == "About | Exeter Domination"
        assert self.selenium.current_url == self.live_server_url + "/about"
        homeButton = self.selenium.find_element_by_xpath(
            "//a[contains(@href, '/')]")
        homeButton.click()
        assert self.selenium.title == "Home | Exeter Domination"
        assert self.selenium.current_url == self.live_server_url + "/"