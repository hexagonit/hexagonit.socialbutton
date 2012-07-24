
from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from hexagonit.utils.stringutils import safe_utf8
from plone.memoize import view    # use:    @view.memoize
from hexagonit.socialbutton import  _
from hexagonit.socialbutton.interfaces import ISocialCodesView
from urllib import quote_plus
from zope.i18n import translate
from zope.interface import implements
import json


page = ".insertAfter('#controlbar')"
newsletter = image = ".appendTo('#region-content')"
blog = ".insertBefore('.discussion:first')"
assortedevent = ".insertAfter('#controlbar')"

# Activated page models
page_pagemodels = """
primacontrol_model1_image_upleft
primacontrol_model2_image_upright
primacontrol_model3_no_images
primacontrol_model4_big_image_upleft
primacontrol_model5_big_image_upright
primacontrol_model6_two_images_upleft
primacontrol_model7_two_images_upright
primacontrol_model8_images_bottom
primacontrol_model9_images_left
primacontrol_model10_images_right
primacontrol_model11_wide_top_image
primacontrol_model67_wide_image_others_right
amnesty_campaign_page
""".strip().split()


def for_all(lst, value, extra):
    """Make a dict with keys from ``lst`` and the same value ``value``,
    updated by extra dict (this way, it can be chained) .
    """
    d = dict((i, value) for i in lst)
    d.update(extra)
    return d


def code_placing_decision():

    return {
        'under': {
            'BlogEntry': {'': blog, },
            'AssortedEvent': {'': assortedevent, '*': ''},
            'Page': for_all(page_pagemodels, page, {'': page, '*': None}),
            '*': None,
            },
        '*': 'under',
        # This is not a place, but also belongs to the configuraton:
        'addon_javascripts': dict(
            facebook_like="""<script type="text/javascript" src="http://connect.facebook.net/%(LANG)s/all.js#xfbml=1"></script>""",  #"
            facebook_recommend="""<script type="text/javascript" src="http://connect.facebook.net/%(LANG)s/all.js#xfbml=1"></script>""",  #"
            twitter="""<script type="text/javascript" src="http://platform.twitter.com/widgets.js"></script>""",
            )
        }


# each target place will have div with certain class (for styling)
place_prefix = "primacontrolSocialSlots"
place_wrapper = """<div class="visualClear %s"></div>"""  # NB visualClear is not always needed?
div_place_op = ".appendTo('.%s')"

# each addon will have its own div also
individual_wrapper = """<div id="primacontrol-social-slot-%s">%s</div>"""

placement_statement = """$(%(CODE)s)%(PLACE)s;"""
place_script = """<script type="text/javascript">//<![CDATA[
(function($) {$(document).ready(function() {%s});}(jQuery));
//]]></script>"""

languages = dict(
    fi="fi_FI",
    sv="sv_SE",
    en="en_US",
    ru="ru_RU",
    )

def decide(d, k):
    """Get value from the dict or default value."""
    if d is None:
        return None
    v = d.get(k, Ellipsis)
    if v is Ellipsis:
        k1 = d.get('*', Ellipsis)
        return d.get(k1, None)
    return v

SHOW_SOCIAL_ADDONS_PROPERTY = 'show_social_addons'

class SocialCodesView(BrowserView):
    """SocialCodesView view"""

    implements(ISocialCodesView)

    def codes(self, *args, **kwargs):
        """Get social html codes. When used with True
        check_visibility_switch_only parameter, returns empty string
        or non-empty string, depending on whether codes would be added
        in the real situation (except for the local override
        property).
        """
        context = aq_inner(self.context)
        # meta_type = context.meta_type
        meta_type = context.Type()
        portal_url = getToolByName(context, 'portal_url')()
        social_properties = getToolByName(context, 'portal_properties').social_properties
        addons = social_properties.getProperty('all_addons', None)
        allowed_metatypes = social_properties.getProperty('allowed_metatypes', [])
        if addons is None or meta_type not in allowed_metatypes:
            return ""

        check_visibility_switch_only = kwargs.get('check_visibility_switch_only', False)

        if not check_visibility_switch_only:
            show_addons = context.getProperty(SHOW_SOCIAL_ADDONS_PROPERTY, None)
            if show_addons is not None and show_addons is False:
                return ""

        try:
            lang = context.REQUEST["LANGUAGE"]
        except (KeyError, AttributeError):
            language_tool = getToolByName(context, 'portal_languages')
            lang = language_tool.getDefaultLanguage()

        # decision_dict = aq_inner(self.context).unrestrictedTraverse('code_placing_decision')()
        decision_dict = code_placing_decision()
        addon_javascripts = decision_dict.get('addon_javascripts', {})

        # Gather places (slots) first, and list addons belonging to them
        places = {}
        for addon in addons:
            for place in social_properties.getProperty(addon + '_places', []):
                places.setdefault(place, []).append(addon)

        codes = ""  # accumulate jQuery manipulation commands here

        javascript_codes = set()
        # organize places and addons in them into stream of manipulation commands
        for place in places:
            place_op = self.decide_on_place_operation(decision_dict, place,
                                                      **{'meta_type': meta_type,
                                                         'page_model': context.getProperty('layout', '')})
            if place_op is None:
                continue

            # No need to continue. We know that at least one plugin is coming. Return non-empty string.
            if check_visibility_switch_only:
                return "<!--ok-->"

            # class, which will identify the place
            place_class = place_prefix + place.capitalize()
            # add code which will insert the place's slot into proper place
            codes += placement_statement % dict(CODE=json.dumps(place_wrapper % place_class), PLACE=place_op)

            for addon in places[place]:
                social = social_properties.getProperty(addon + '_code', None)
                if social is None:
                    continue
                hidden = social_properties.getProperty(addon + '_hidden', None)
                if hidden is not None and hidden:
                    continue

                social = social.replace('$URL', context.absolute_url())
                social = social.replace('$TITLE', quote_plus(safe_utf8(context.Title())))
                social = social.replace('$PORTAL', portal_url)

                code_to_place = individual_wrapper % (addon, social)

                # add codes which will insert specific addon
                codes += placement_statement % dict(CODE=json.dumps(code_to_place), PLACE=div_place_op % place_class)
                # also, we need javascripts. One script needs to be inserted only once
                javascript_codes.add(addon_javascripts.get(addon, '') % dict(LANG=languages.get(lang, 'en_US')))

        # No codes gathered - switch action not visible
        if check_visibility_switch_only:
            return ""

        return "\n".join(javascript_codes) + "\n" + (place_script % codes)

    def decide_on_place_operation(self, decision_dict, place, **args):
        """Dicide on where to place the code, based on some paramaeters."""
        meta_type = args.get('meta_type')
        page_model = args.get('page_model')

        # Nested dict, levels of nesting: place ('under'), meta_type, page_model. Default is defined as '*',
        # value of which is a key for the default value.

        place_op = decide(decide(decide(decision_dict, place), meta_type), page_model)
        return place_op

    @view.memoize
    def show_switch(self):
        """Checks which on/off switch action needs to be shown. Returns: None (do not show switch action),
        'off' (now on, show off-action), 'on' (now off, show on-action)
        """
        context = aq_inner(self.context)
        if self.codes(check_visibility_switch_only=True):
            show_addons = context.getProperty(SHOW_SOCIAL_ADDONS_PROPERTY, None)
            if show_addons is not None and show_addons is False:
                return 'on'
            else:
                return 'off'
        return None

    def show_off_switch(self):
        return self.show_switch() == 'off'

    def show_on_switch(self):
        return self.show_switch() == 'on'

    def main_view_url(self):
        context = aq_inner(self.context)
        site_props = getToolByName(context, 'portal_properties').site_properties
        types_list = site_props.getProperty('typesUseViewActionInListings')
        url = context.absolute_url()
        if context.portal_type in types_list:
            return '%s/view' % url
        else:
            return url


    def switch(self, target):
        """Switch social addons visibility to 'on' or 'off'.
        """
        context = aq_inner(self.context)
        switch_state = self.show_switch()
        if switch_state is None:
            message = _(u'ERROR: Not possible to switch visibility of social plugins.')
            # this message should not appear normally
        else:
            if switch_state == target:
                old_value = context.getProperty(SHOW_SOCIAL_ADDONS_PROPERTY, None)
                new_value = target == 'on'
                if old_value is None:
                    context.manage_addProperty(SHOW_SOCIAL_ADDONS_PROPERTY, new_value, 'boolean')
                else:
                    context.manage_changeProperties(**{SHOW_SOCIAL_ADDONS_PROPERTY: new_value})
                # switched
            else:
                pass
                # no switch needed
            if target == 'on':
                message = _(u'Social plugins switched on.')
            else:
                message = _(u'Social plugins switched off.')

        self.request.response.redirect(safe_utf8(self.main_view_url()) + \
                                           '/?portal_status_message=' + \
                                           quote_plus(safe_utf8(translate(message, context=self.request))))

