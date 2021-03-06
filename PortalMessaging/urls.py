from PortalMessaging.forms import MessageForm
from PortalMessaging.views import IndexMessage, MessageDetails, MessageView, ReplyView

__author__ = 'cloquet'


from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^$', IndexMessage.as_view(), name='message_index'),
    url(r'^write_message/$', MessageView.as_view(), name='write_msg'),
    url(r'^(?P<message_id>[\d]+)/reply_message/$', ReplyView.as_view(), name='reply_msg'),
    url(r'^(?P<message_id>[\d]+)/$', MessageDetails.as_view(), name='message_details'),
        )