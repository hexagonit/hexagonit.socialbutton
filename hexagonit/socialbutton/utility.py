from five import grok
from plone.app.vocabularies.types import BAD_TYPES
from zope.interface import implements
from zope.interface import Interface


class IBadTypes(Interface):
    """Interface for excluding bad types from vocabularies."""


class BadTypes(grok.GlobalUtility):
    implements(IBadTypes)

    def __call__(self):
        types = list(BAD_TYPES)
        types.remove('Plone Site')
        return tuple(types)
