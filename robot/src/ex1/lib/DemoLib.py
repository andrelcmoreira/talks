from robot.api.deco import keyword

class DemoLib(object):

    """Demo test library implementation"""

    @keyword("Hello, I'm a custom keyword")
    def custom_keyword(self):
        """Example of a custom keyword"""
        print("I'm alive!")

    @keyword("Hello, I'm a custom keyword with parameter ${param}")
    def custom_keyword_with_parameter(self, param):
        """Example of a custom keyword with parameter"""
        print("I'm alive and I have a parameter: {}".format(param))
