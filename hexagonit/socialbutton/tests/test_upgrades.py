from hexagonit.socialbutton.tests.base import IntegrationTestCase


PROFILE_ID = 'profile-hexagonit.socialbutton.tests.old:old'


class TestCase(IntegrationTestCase):
    """TestCase for Plone setup."""

    def setUp(self):
        self.portal = self.layer['portal']

    def test_upgrades_1_to_2(self):
        from Products.CMFCore.utils import getToolByName
        from plone.registry.interfaces import IRegistry
        from zope.component import getUtility

        setup = getToolByName(self.portal, 'portal_setup')
        setup.runImportStepFromProfile(PROFILE_ID, 'plone.app.registry', run_dependencies=False, purge_old=False)

        registry = getUtility(IRegistry)
        codes = {
            u'aaa': {
                u'code_id': u'aaa',
                u'code_text': u'{TITLE}, {DESCRIPTION}, {URL}, {LANG}, {LANG_COUNTRY}, {PORTAL_URL}, {{script}}',
                u'code_icon': u'ICON-AAA',
            },
            u'bbb': {
                u'code_id': u'bbb',
                u'code_text': u'<BBB />',
                u'code_icon': u'ICON-BBB',
            },
        }
        registry['hexagonit.socialbutton.codes'] = codes

        config = {
            u'aaa': {
                u'code_id': u'aaa',
                u'content_types': set(),
                u'viewlet_manager': 'plone.abovecontent',
                u'view_models': None,
                u'view_permission_only': True,
                u'enabled': True,
            },
            u'bbb': {
                u'code_id': u'bbb',
                u'content_types': set(['Document', 'Folder']),
                u'viewlet_manager': 'plone.abovecontent\nplone.belowcontent',
                u'view_models': 'document_view',
                u'view_permission_only': False,
                u'enabled': False,
            },
        }
        registry['hexagonit.socialbutton.config'] = config

        from hexagonit.socialbutton.upgrades import upgrade_1_to_2
        upgrade_1_to_2(self.portal)
        self.assertEqual(
            registry['hexagonit.socialbutton.codes'],
            {
            u'aaa': {
                u'code_id': u'aaa',
                u'code_text': u'${title}, ${description}, ${url}, ${lang}, ${lang_country}, ${portal_url}, {script}',
            },
            u'bbb': {
                u'code_id': u'bbb',
                u'code_text': u'<BBB />',
            },
        })
        self.assertEqual(
            registry['hexagonit.socialbutton.config'],
            {
            u'aaa': {
                u'code_id': u'aaa',
                u'content_types': u'*',
                u'viewlet_manager': u'plone.abovecontent',
                u'view_models': u'*',
                u'view_permission_only': u'True',
                u'enabled': u'True',
            },
            u'bbb': {
                u'code_id': u'bbb',
                u'content_types': u'Folder,Document',
                u'viewlet_manager': u'plone.abovecontent\nplone.belowcontent',
                u'view_models': u'document_view',
                u'view_permission_only': u'False',
                u'enabled': u'False',
            },
        })
