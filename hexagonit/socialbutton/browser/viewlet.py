from five import grok
from hexagonit.socialbutton.browser.interfaces import IHexagonitSocialbuttonLayer
from plone.app.layout.viewlets.interfaces import IBelowContent
from zope.interface import Interface


grok.templatedir('viewlets')


class SocialButtonsViewlet(grok.Viewlet):
    grok.context(Interface)
    grok.layer(IHexagonitSocialbuttonLayer)
    grok.name('hexagonit.socialbutton.viewlet')
    grok.require('zope2.View')
    grok.template('social-buttons')
    grok.viewletmanager(IBelowContent)

    def items(self):
        return []
