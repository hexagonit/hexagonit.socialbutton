from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import unittest2 as unittest


class HexagonitSocialbuttonLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        """Set up Zope."""
        import hexagonit.socialbutton
        self.loadZCML(package=hexagonit.socialbutton)
        z2.installProduct(app, 'hexagonit.socialbutton')

    def setUpPloneSite(self, portal):
        """Set up Plone."""
        self.applyProfile(portal, 'hexagonit.socialbutton:default')

    def tearDownZope(self, app):
        """Tear down Zope."""
        z2.uninstallProduct(app, 'hexagonit.socialbutton')


FIXTURE = HexagonitSocialbuttonLayer()
INTEGRATION_TESTING = IntegrationTesting(
    bases=(FIXTURE,), name="HexagonitSocialbuttonLayer:Integration")
FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(FIXTURE,), name="HexagonitSocialbuttonLayer:Functional")


class IntegrationTestCase(unittest.TestCase):
    """Base class for integration tests."""

    layer = INTEGRATION_TESTING


class FunctionalTestCase(unittest.TestCase):
    """Base class for functional tests."""

    layer = FUNCTIONAL_TESTING
