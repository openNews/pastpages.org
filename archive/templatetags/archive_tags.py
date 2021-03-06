from django import template
from archive.models import Update, Site
from django.db.models import Min, Max
from django.utils.timezone import localtime


class DateRangeNode(template.Node):
    def render(self, context):
        update_list = Update.objects.all()
        naive_min = update_list.aggregate(Min("start"))['start__min']
        naive_max = update_list.aggregate(Max("start"))['start__max']
        context['min_date'] = localtime(naive_min)
        context['max_date'] = localtime(naive_max)
        return ''


def do_daterange(parser, token):
    """ 
    Allows a template-level call for the min and max dates where archives
    are available
    
    Example usage:
    
        {% load archive_tags %}
        {% get_daterange %}
        {{ min_date }}
        {{ max_date }}
    
    """
    return DateRangeNode()


class SitelistNode(template.Node):
    def render(self, context):
        context['site_list'] = Site.objects.filter(status='active')
        return ''


def do_sitelist(parser, token):
    """ 
    Allows a template-level call a list of all the active sites.
    """
    return SitelistNode()


register = template.Library()
register.tag('get_daterange', do_daterange)
register.tag('get_sitelist', do_sitelist)
