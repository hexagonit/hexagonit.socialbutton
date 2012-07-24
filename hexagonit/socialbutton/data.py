from hexagonit.socialbutton.interfaces import IData
from hexagonit.socialbutton.interfaces import ISocialButtonConfig
from zope.interface import implements


class Data(object):

    implements(IData)

    def __init__(self, code_id, code_text):
        self.code_id = code_id
        self.code_text = code_text

    def __repr__(self):
        return '<Data with ={code_id!r}>'.format(
            code_id=self.code_id)


class SocialButtonConfig(object):

    implements(ISocialButtonConfig)

    def __init__(self, code_id, code_text):
        self.code_id = code_id
        self.code_text = code_text

    def __repr__(self):
        return '<Data with ={code_id!r}>'.format(
            code_id=self.code_id)
