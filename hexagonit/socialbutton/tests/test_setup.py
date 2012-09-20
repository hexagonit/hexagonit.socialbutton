from Products.CMFCore.utils import getToolByName
from hexagonit.socialbutton.tests.base import IntegrationTestCase


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

    def test_metadata__version(self):
        setup = getToolByName(self.portal, 'portal_setup')
        self.assertEqual(
            setup.getVersionForProfile('profile-hexagonit.socialbutton:default'),
            u'2'
        )

    def get_record(self, name):
        from zope.component import getUtility
        from plone.registry.interfaces import IRegistry
        return getUtility(IRegistry).records.get(name)

    def test_registry__record__hexagonit_socialbutton_codes__field(self):
        from plone.registry.field import Dict
        record = self.get_record('hexagonit.socialbutton.codes')
        self.assertIsInstance(record.field, Dict)

    def test_registry__record__hexagonit_socialbutton_codes__field__title(self):
        record = self.get_record('hexagonit.socialbutton.codes')
        self.assertEqual(record.field.title, u'Codes for Social Buttons')

    def test_registry__record__hexagonit_socialbutton_codes__field__key_type(self):
        from plone.registry.field import TextLine
        record = self.get_record('hexagonit.socialbutton.codes')
        self.assertIsInstance(record.field.key_type, TextLine)

    def test_registry__record__hexagonit_socialbutton_codes__field__value_type(self):
        from plone.registry.field import Dict
        record = self.get_record('hexagonit.socialbutton.codes')
        self.assertIsInstance(record.field.value_type, Dict)

    def test_registry__record__hexagonit_socialbutton_config__field(self):
        from plone.registry.field import Dict
        record = self.get_record('hexagonit.socialbutton.config')
        self.assertIsInstance(record.field, Dict)

    def test_registry__record__hexagonit_socialbutton_config__field__title(self):
        record = self.get_record('hexagonit.socialbutton.config')
        self.assertEqual(record.field.title, u'Configuration for Social Buttons')

    def test_registry__record__hexagonit_socialbutton_config__field__key_type(self):
        from plone.registry.field import TextLine
        record = self.get_record('hexagonit.socialbutton.config')
        self.assertIsInstance(record.field.key_type, TextLine)

    def test_registry__record__hexagonit_socialbutton_config__field__value_type(self):
        from plone.registry.field import Dict
        record = self.get_record('hexagonit.socialbutton.config')
        self.assertIsInstance(record.field.value_type, Dict)

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

    def test_uninstall__registry__hexagonit_socialbutton_codes(self):
        installer = getToolByName(self.portal, 'portal_quickinstaller')
        installer.uninstallProducts(['hexagonit.socialbutton'])
        from zope.component import getUtility
        from plone.registry.interfaces import IRegistry
        registry = getUtility(IRegistry)
        with self.assertRaises(KeyError):
            registry['hexagonit.socialbutton.codes']

    def test_uninstall__registry__hexagonit_socialbutton_config(self):
        installer = getToolByName(self.portal, 'portal_quickinstaller')
        installer.uninstallProducts(['hexagonit.socialbutton'])
        from zope.component import getUtility
        from plone.registry.interfaces import IRegistry
        registry = getUtility(IRegistry)
        with self.assertRaises(KeyError):
            registry['hexagonit.socialbutton.config']
