from Products.CMFCore.utils import getToolByName
from plone.registry.interfaces import IRegistry
from zope.component import getUtility

import logging

PROFILE_ID = 'profile-hexagonit.socialbutton:default'


def upgrade_1_to_2(context, logger=None):
    """Reimport registry.xml"""
    if logger is None:
        # Called as upgrade step: define our own logger.
        logger = logging.getLogger(__name__)

    registry = getUtility(IRegistry)
    codes = registry['hexagonit.socialbutton.codes']

    for key in codes:
        logger.info('Removing code_icon from {0}'.format(key))
        del codes[key][u'code_icon']
        logger.info('Removed code_icon from {0}'.format(key))
        logger.info('Updating code_text of {0}'.format(key))
        text = codes[key][u'code_text'].format(TITLE='${title}', DESCRIPTION='${description}', URL='${url}',
            LANG='${lang}', LANG_COUNTRY='${lang_country}', PORTAL_URL='${portal_url}')
        codes[key]['code_text'] = text
        logger.info('Updated code_text of {0}'.format(key))

    config = registry['hexagonit.socialbutton.config']
    from hexagonit.socialbutton.utility import IConvertToUnicode
    for key in config:
        if config[key][u'view_models'] is None:
            config[key][u'view_models'] = u'*'
        if not config[key][u'content_types']:
            config[key][u'content_types'] = u'*'
        config[key] = getUtility(IConvertToUnicode)(config[key])

    setup = getToolByName(context, 'portal_setup')
    logger.info('Reimporting registry.xml.')
    # setup.runImportStepFromProfile('profile-hexagonit.socialbutton:uninstall', 'plone.app.registry', run_dependencies=False, purge_old=False)
    setup.runImportStepFromProfile(PROFILE_ID, 'plone.app.registry', run_dependencies=False, purge_old=False)
    logger.info('Reimported registry.xml.')

    logger.info('Setting records for hexagonit.socialbutton.codes and hexagonit.socialbutton.config.')
    registry['hexagonit.socialbutton.codes'] = codes
    registry['hexagonit.socialbutton.config'] = config
    logger.info('Set records for hexagonit.socialbutton.codes and hexagonit.socialbutton.config.')
