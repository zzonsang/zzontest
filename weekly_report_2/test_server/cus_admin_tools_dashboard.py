"""
This file was generated with the customdashboard management command, it
contains the two classes for the main dashboard and app index dashboard.
You can customize these classes as you want.

To activate your index dashboard add the following to your settings.py::
    ADMIN_TOOLS_INDEX_DASHBOARD = 'test_server.cus_admin_tools_dashboard.CustomIndexDashboard'

And to activate the app index dashboard::
    ADMIN_TOOLS_APP_INDEX_DASHBOARD = 'test_server.cus_admin_tools_dashboard.CustomAppIndexDashboard'
"""

from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from admin_tools.dashboard import modules, Dashboard, AppIndexDashboard
from admin_tools.utils import get_admin_site_name
from vdi_report.models import CustomFeed
import logging

logger = logging.getLogger('weekly_report')

class CustomIndexDashboard(Dashboard):
    columns = 3
    
    """
    Custom index dashboard for test_server.
    """
    def init_with_context(self, context):
        
        site_name = get_admin_site_name(context)
        logger.debug('[sitename][%s]' % site_name)
        # append a link list module for "quick links"
        self.children.append(modules.LinkList(
            _('Quick links'),
            layout='inline',
            draggable=False,
            deletable=False,
            collapsible=False,
            children=[
                [_('Return to site'), '/'],
                [_('Add report'), '/vdi_report/report/add/'],
                [_('Change password'),
                 reverse('%s:password_change' % site_name)],
                [_('Log out'), reverse('%s:logout' % site_name)],
            ]
        ))

        # append an app list module for "Applications"
        self.children.append(modules.AppList(
            _('Applications'),
            exclude=('django.contrib.*',),
        ))

        # append an app list module for "Administration"
        self.children.append(modules.AppList(
            _('Administration'),
            models=('django.contrib.*',),
        ))

        # append a recent actions module
        self.children.append(modules.RecentActions(_('Recent Actions'), 5))

        # append custom feed modules
        feeds = CustomFeed.objects.all()
        for feed in feeds:
            logger.debug('[feed]' + feed.title)
            self.children.append(modules.Feed(
                _(feed.title),
                feed_url = feed.feed_url,
                limit = feed.limit,
                enabled=False
            ))

        # append a feed module
        self.children.append(modules.Feed(
            _('Latest Django News'),
            feed_url='http://www.djangoproject.com/rss/weblog/',
            limit=5,
#            enabled=False
        ))

        # append another link list module for "support".
        self.children.append(modules.LinkList(
            _('Support'),
            children=[
                {
                    'title': _('Django documentation'),
                    'url': 'http://docs.djangoproject.com/',
                    'external': True,
                },
                {
                    'title': _('Django "django-users" mailing list'),
                    'url': 'http://groups.google.com/group/django-users',
                    'external': True,
                },
                {
                    'title': _('Django irc channel'),
                    'url': 'irc://irc.freenode.net/django',
                    'external': True,
                },
            ]
        ))


class CustomAppIndexDashboard(AppIndexDashboard):
    """
    Custom app index dashboard for test_server.
    """

    # we disable title because its redundant with the model list module
    title = ''

    def __init__(self, *args, **kwargs):
        AppIndexDashboard.__init__(self, *args, **kwargs)

        # append a model list module and a recent actions module
        self.children += [
            modules.ModelList(self.app_title, self.models),
            modules.RecentActions(
                _('Recent Actions'),
                include_list=self.get_app_content_types(),
                limit=5
            )
        ]
        
#        # append custom feed modules
#        feeds = CustomFeed.objects.all()
#        for feed in feeds:
#            logger.debug('[feed]' + feed.title)
#            self.children.append(modules.Feed(
#                _(feed.title),
#                feed_url = feed.feed_url,
#                limit = feed.limit,
#                enabled=False
#            ))

    def init_with_context(self, context):
        """
        Use this method if you need to access the request context.
        """
#        # append custom feed modules
#        feeds = CustomFeed.objects.all()
#        for feed in feeds:
#            logger.debug('[feed]' + feed.title)
#            self.children.append(modules.Feed(
#                _(feed.title),
#                feed_url = feed.feed_url,
#                limit = feed.limit,
#                enabled=False
#            ))
        
        return super(CustomAppIndexDashboard, self).init_with_context(context)
