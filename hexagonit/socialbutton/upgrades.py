from Products.CMFCore.utils import getToolByName
from plone.registry.interfaces import IRegistry
from zope.component import getUtility

import logging

PROFILE_ID = 'profile-hexagonit.socialbutton:default'


def upgrade_1_to_2(context, logger=None):
    """Reimport registry.xml"""
    if logger is None:
        logger = logging.getLogger(__name__)

    registry = getUtility(IRegistry)
    codes = registry['hexagonit.socialbutton.codes']
    from hexagonit.socialbutton.utility import IConvertToUnicode
    convert = getUtility(IConvertToUnicode)
    if codes:
        for key in codes:
            logger.info('Removing code_icon from {0}'.format(key))
            del codes[key][u'code_icon']
            logger.info('Removed code_icon from {0}'.format(key))
            codes[key] = convert(codes[key])
            logger.info('Updating code_text of {0}'.format(key))
            text = codes[key][u'code_text'].format(
                TITLE='${title}', DESCRIPTION='${description}', URL='${url}',
                LANG='${lang}', LANG_COUNTRY='${lang_country}', PORTAL_URL='${portal_url}')
            codes[key][u'code_text'] = text
            logger.info('Updated code_text of {0}'.format(key))

    config = registry['hexagonit.socialbutton.config']
    if config:
        for key in config:
            if not config[key][u'view_models']:
                config[key][u'view_models'] = u'*'
            if not config[key][u'content_types']:
                config[key][u'content_types'] = u'*'
            config[key] = convert(config[key])

    setup = getToolByName(context, 'portal_setup')
    logger.info('Reimporting registry.xml.')
    setup.runImportStepFromProfile(PROFILE_ID, 'plone.app.registry', run_dependencies=False, purge_old=False)
    logger.info('Reimported registry.xml.')

    logger.info('Setting records for hexagonit.socialbutton.codes and hexagonit.socialbutton.config.')
    if codes:
        registry['hexagonit.socialbutton.codes'] = codes
    if config:
        registry['hexagonit.socialbutton.config'] = config
    logger.info('Set records for hexagonit.socialbutton.codes and hexagonit.socialbutton.config.')
