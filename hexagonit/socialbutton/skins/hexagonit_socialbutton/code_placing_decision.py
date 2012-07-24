# -*- coding: utf-8 -*-
"""
Decision-making dictionary for the social codes' placement operation.
"""

# jQuery selectors
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

return {
    'under': {
#        'ATImage': {'': image,},
#        'NewsletterTheme': {'': newsletter,},
        'BlogEntry': {'': blog,},
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
