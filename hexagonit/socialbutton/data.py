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

    def __init__(self, code_id, **kwargs):
        super(self.__class__, self).__init__(code_id, **kwargs)
        self.view_permission_only = True if self.view_permission_only == u'True' else False
        self.enabled = True if self.enabled == u'True' else False
        if self.content_types:
            self.content_types = set(self.content_types.split(u','))
        else:
            self.content_types = set()
