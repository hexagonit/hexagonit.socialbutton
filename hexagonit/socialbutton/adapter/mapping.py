from five import grok
from hexagonit.socialbutton.config import LANGUAGE_COUNTRY
from hexagonit.socialbutton.interfaces import ILanguageCountry
from zope.interface import Interface


class LanguageCountry(grok.Adapter):
    grok.context(Interface)
    grok.provides(ILanguageCountry)

    def __call__(self, lang, **kwargs):
        """Returns lang_country locale string.

        :param lang: Language code.
        :type lang: str

        :rtype: str
        """
        return '{0}_{1}'.format(lang, LANGUAGE_COUNTRY[lang])
