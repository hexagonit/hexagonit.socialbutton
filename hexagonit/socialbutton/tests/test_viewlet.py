from hexagonit.socialbutton.tests.base import IntegrationTestCase


class TestSocialButtonsViewlet(IntegrationTestCase):
    """TestCase testing SocialButtonsViewlet class."""

    def setUp(self):
        self.portal = self.layer['portal']

    def createViewlet(self):
        from hexagonit.socialbutton.browser.viewlet import SocialButtonsViewlet
        from zope.publisher.browser import TestRequest
        return SocialButtonsViewlet(self.portal, TestRequest(), None, None)

    def test__normalize__value_None(self):
        viewlet = self.createViewlet()
        self.assertIsNone(viewlet._normalize(None))
