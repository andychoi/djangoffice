from django import template

from djangoffice.menu import build_menu_items

register = template.Library()

@register.inclusion_tag('menu.html', takes_context=True)
def include_menu(context, section=None, page=None):
    """
    Display section and current section (if any) page menus.

    Sample usage::

        {% include_menu "some_section" %}
        {% include_menu "some_section" "some_page" %}
    """
    if section:
        section_items, page_items = build_menu_items(context['user'], section, page)
    else:
        section_items = page_items = None
    #FIXME dump: https://stackoverflow.com/questions/54339582/fix-render-got-an-unexpected-keyword-argument-renderer-in-django-2-1
    return {
        # 'user': context['request'].user,        # user from the context request
        'user': context['user'],
        'section': section,
        'section_items': section_items,
        'page': page,
        'page_items': page_items,
    }
