from diff import ImageDiff
from driver import NeedleWebDriver
import os
from PIL import Image
import sys


class Spindle(object):
    """
    Object which provides tools for testing CSS with Selenium.
    """
    #: An instance of :py:class:`~needle.driver.NeedleWebDriver`, created when 
    #: each test is run.
    driver = None

    driver_command_executor = 'http://127.0.0.1:4444/wd/hub'
    driver_desired_capabilities = {
        'browserName': 'firefox',
    }
    driver_browser_profile = None

    capture = False
    output_path = None

    def __init__(self, *args, **kwargs):
        self.driver = self.get_web_driver()
        self.capture = kwargs['capture'] if 'capture' in kwargs else False
        self.output_path = kwargs['output_path'] if 'output_path' in kwargs else os.path.dirname(__file__)

    # def __call__(self, *args, **kwargs):
    #     self.driver = self.get_web_driver()
    #     super(Spindle, self).__call__(*args, **kwargs)
    #     self.driver.close()

    def get_web_driver(self):
        return NeedleWebDriver(
            self.driver_command_executor,
            self.driver_desired_capabilities,
            self.driver_browser_profile
        )

    def assertScreenshot(self, element, name, threshold=0.1):
        """
        Assert that a screenshot of an element is the same as a screenshot on disk,
        within a given threshold.
        
        :param element: Either a CSS selector as a string or a 
                        :py:class:`~needle.driver.NeedleWebElement` object that 
                        represents the element to capture.
        :param name: A name for the screenshot, which will be appended with 
                     ``.png``.
        :param threshold: The threshold for triggering a test failure.
        """
        if isinstance(element, basestring):
            element = self.driver.find_element_by_css_selector(element)
        if isinstance(name, basestring):
            filename = os.path.join(
                self.output_path,
                '%s.png' % name
            )
        else:
            # names can be filehandles for testing. This sucks - we
            # should write out files to their correct location
            filename = name

        if self.capture:
            element.get_screenshot().save(filename)
        else:
            image = Image.open(filename)
            # now take another screenshot and re open it (yea i know) but there were issues wth colours

            screenshot_filename = filename.replace('.png','-compare.png')
            screenshot = element.get_screenshot().save(screenshot_filename)

            screenshot = Image.open(screenshot_filename)
            
            diff = ImageDiff(screenshot, image)
            distance = abs(diff.get_distance())
            if distance > threshold:
                raise AssertionError("The saved screenshot for '%s' did not match "
                                     "the screenshot captured (by a distance of %.2f)" 
                                     % (name, distance))





    

