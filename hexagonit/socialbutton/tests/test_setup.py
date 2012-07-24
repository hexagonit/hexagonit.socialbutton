from hexagonit.socialbutton.tests.base import IntegrationTestCase
from Products.CMFCore.utils import getToolByName


class TestCase(IntegrationTestCase):
    """TestCase for Plone setup."""

    def setUp(self):
        self.portal = self.layer['portal']

    def test_is_hexagonit_socialbutton_installed(self):
        installer = getToolByName(self.portal, 'portal_quickinstaller')
        self.failUnless(installer.isProductInstalled('hexagonit.socialbutton'))

    def test_browserlayer(self):
        from hexagonit.socialbutton.browser.interfaces import IHexagonitSocialbuttonLayer
        from plone.browserlayer import utils
        self.failUnless(IHexagonitSocialbuttonLayer in utils.registered_layers())

    def test_uninstall__package(self):
        installer = getToolByName(self.portal, 'portal_quickinstaller')
        installer.uninstallProducts(['hexagonit.socialbutton'])
        self.failIf(installer.isProductInstalled('hexagonit.socialbutton'))

    def test_uninstall__browserlayer(self):
        installer = getToolByName(self.portal, 'portal_quickinstaller')
        installer.uninstallProducts(['hexagonit.socialbutton'])
        from hexagonit.socialbutton.browser.interfaces import IHexagonitSocialbuttonLayer
        from plone.browserlayer import utils
        self.failIf(IHexagonitSocialbuttonLayer in utils.registered_layers())
