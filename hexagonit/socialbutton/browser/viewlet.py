from AccessControl.SecurityManagement import getSecurityManager
from AccessControl.SecurityManagement import newSecurityManager
from AccessControl.SecurityManagement import setSecurityManager
from AccessControl.User import SpecialUser
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import safe_unicode
from five import grok
from hexagonit.socialbutton.browser.interfaces import IHexagonitSocialbuttonLayer
from hexagonit.socialbutton.data import SocialButtonConfig
from hexagonit.socialbutton.interfaces import ILanguageCountry
from hexagonit.socialbutton.interfaces import ISocialButtonHidden
from plone.app.layout.globals.interfaces import IViewView
from plone.registry.interfaces import IRegistry
from zope.component import getMultiAdapter
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
            if data.content_types and types.getTypeInfo(self.context).id not in data.content_types:
                continue
            if not data.enabled:
                continue
            if self._normalize(data.view_models) and self.context.getLayout() not in self._normalize(data.view_models):
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
        context_state = getMultiAdapter(
            (self.context, self.request), name='plone_context_state')
        portal_state = getMultiAdapter(
            (self.context, self.request), name='plone_portal_state')
        res = []
        for key in self.buttons:
            item = {'code_id': key}
            code_text = items[key]['code_text']
            lang = portal_state.language()
            text = u''.join(self._normalize(code_text))
            code_text = text.format(
                TITLE=self._get_method('Title'),
                DESCRIPTION=self._get_method('Description'),
                URL=context_state.current_base_url(),
                LANG=lang,
                LANG_COUNTRY=ILanguageCountry(self.context)(lang),
                # ICON=items[key]['code_icon'],
                PORTAL_URL=portal_state.portal_url())
            item['code_text'] = code_text
            res.append(item)
        return res

    def _get_method(self, name):
        """Returns method value with name or empty string.

        :param name: Method name.
        :type name: str

        :rtype: unicode
        """
        met = getattr(self.context, name, u'')
        if met:
            return safe_unicode(met())
        return met
