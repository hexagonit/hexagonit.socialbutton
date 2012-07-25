from hexagonit.socialbutton.interfaces import ISocialButtonCode
from hexagonit.socialbutton.interfaces import ISocialButtonConfig
from zope.interface import implements


class Data(object):

    def __init__(self, code_id, **kwargs):
        self.code_id = code_id
        for key in kwargs:
            setattr(self, key, kwargs[key])


class SocialButtonCode(Data):

    implements(ISocialButtonCode)


class SocialButtonConfig(Data):

    implements(ISocialButtonConfig)
