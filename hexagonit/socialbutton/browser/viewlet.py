from AccessControl.SecurityManagement import getSecurityManager
from AccessControl.SecurityManagement import newSecurityManager
from AccessControl.SecurityManagement import setSecurityManager
from AccessControl.User import SpecialUser
from Products.CMFCore.utils import getToolByName
from five import grok
from hexagonit.socialbutton.browser.interfaces import IHexagonitSocialbuttonLayer
from hexagonit.socialbutton.data import SocialButtonConfig
from hexagonit.socialbutton.interfaces import ISocialButtonHidden
from plone.app.layout.globals.interfaces import IViewView
from plone.registry.interfaces import IRegistry
from plone.stringinterp.interfaces import IStringInterpolator
from zope.component import getUtility
from zope.interface import Interface
from zope.viewlet.interfaces import IViewletManager


grok.templatedir('viewlets')


class anonymous_access(object):
    """ Context anonymous to use like this:
    with anonymous_access(request):
        do_something()
    """

    def __init__(self, request, roles=('Anonymous', )):
        self.request = request
        self._roles = roles

    def __enter__(self):
        self.real_sm = getSecurityManager()
        newSecurityManager(
            self.request,
            SpecialUser('Anonymous User', '', self._roles, [])
        )
        return self.real_sm

    def __exit__(self, exc_type, exc_value, traceback):
        setSecurityManager(self.real_sm)


class SocialButtonsViewlet(grok.Viewlet):
    grok.context(Interface)
    grok.layer(IHexagonitSocialbuttonLayer)
    grok.name('hexagonit.socialbutton.viewlet')
    grok.require('zope2.View')
    grok.template('social-buttons')
    grok.view(IViewView)
    grok.viewletmanager(IViewletManager)

    def _normalize(self, value):
        """Normalize and make it list."""
        if value:
            return [l.strip() for l in value.strip().splitlines() if l.strip()]

    @property
    def manager_name(self):
        return self.manager.__name__.replace('.', '-')

    @property
    def buttons(self):
        keys = []
        if ISocialButtonHidden.providedBy(self.context):
            return keys
        registry = getUtility(IRegistry)
        items = registry['hexagonit.socialbutton.config']
        types = getToolByName(self.context, 'portal_types')
        for key in items:
            data = SocialButtonConfig(str(key), **items[key])
            if u'*' not in data.content_types and types.getTypeInfo(self.context).id not in data.content_types:
                continue
            if not data.enabled:
                continue
            if u'*' not in self._normalize(data.view_models) and self.context.getLayout() not in self._normalize(data.view_models):
                continue
            if self.manager.__name__ not in self._normalize(data.viewlet_manager):
                continue
            with anonymous_access(self.request):
                if data.view_permission_only and not getSecurityManager().checkPermission('View', self):
                    continue
            keys.append(key)
        return keys

    def items(self):
        registry = getUtility(IRegistry)
        items = registry['hexagonit.socialbutton.codes']
        res = []
        for key in self.buttons:
            item = {'code_id': key}
            code_text = items[key]['code_text']
            item['code_text'] = IStringInterpolator(self.context)(code_text)
            res.append(item)
        return res
