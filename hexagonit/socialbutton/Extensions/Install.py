from StringIO import StringIO
from Products.CMFCore.utils import getToolByName


def uninstall(self):
    out = StringIO()
    print >> out, "Removing hexagonit.socialbutton"

    portal_setup = getToolByName(self, 'portal_setup')
    portal_setup.runAllImportStepsFromProfile(
        'profile-hexagonit.socialbutton:uninstall',
        purge_old=False)
