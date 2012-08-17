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


class IConvertToUnicode(Interface):
    """Interface for converting dictionary data into unicode."""


class ConvertToUnicode(grok.GlobalUtility):
    implements(IConvertToUnicode)

    def __call__(self, data):
        """Convert dictionary keys from sting to unicode and
        all types of values into unicode."""
        items = {}
        for key in data:
            value = data[key]
            key = unicode(key)
            if isinstance(value, bool):
                items[key] = unicode(value)
            elif isinstance(value, set):
                items[key] = u','.join(value)
            else:
                items[key] = unicode(value)
        return items
