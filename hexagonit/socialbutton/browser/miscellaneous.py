from Products.Five.browser import BrowserView
from hexagonit.socialbutton.interfaces import ISocialButtonHidden
from zope.interface import alsoProvides
from zope.interface import noLongerProvides


class Miscellaneous(BrowserView):

    def social_buttons_hidden(self):
        return ISocialButtonHidden.providedBy(self.context)

    def hide_social_buttons(self):
        alsoProvides(self.context, ISocialButtonHidden)
        self.context.reindexObject(idxs=['object_provides'])
        url = self.context.absolute_url()
        return self.request.response.redirect(url)

    def show_social_buttons(self):
        noLongerProvides(self.context, ISocialButtonHidden)
        self.context.reindexObject(idxs=['object_provides'])
        url = self.context.absolute_url()
        return self.request.response.redirect(url)
