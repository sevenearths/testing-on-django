from django.conf import settings

def from_settings(request):
    options = {
        'jquery_js_link': settings.JQUERY_JS_LINK,
        'angular_js_link': settings.ANGULAR_JS_LINK,
        'font_awsome_css_link': settings.FONT_AWSOME_CSS_LINK,
        'semantic_css_link': settings.SEMANTIC_CSS_LINK,
        'semantic_js_link': settings.SEMANTIC_JS_LINK,
        'momentjs_js_link': settings.MOMENTJS_JS_LINK,
        'angular_momentjs_js_link': settings.ANGULAR_MOMENTJS_JS_LINK
    }
    return options