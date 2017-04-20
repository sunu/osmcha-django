# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView
from django.views import defaults
from django.views import static as static_views

from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='OSMCHA API')

urlpatterns = [
    url(r'^about/$', TemplateView.as_view(template_name='pages/about.html'), name="about"),

    # Django Admin
    url(r'^admin/', include(admin.site.urls)),

    # django-rest-social-auth token urls
    url(r'^api/v1/login/', include('rest_social_auth.urls_token')),
    # User management
    url(r'^api/v1/users/', include("osmchadjango.users.urls", namespace="users")),

    # api docs
    url(r'^api-docs/', schema_view, name='api-docs'),
    url(r'^', schema_view),

    # Your stuff: custom urls includes go here
    url(r'^api/v1/', include("osmchadjango.changeset.urls", namespace="changeset")),
    url(r'^api/v1/', include("osmchadjango.feature.urls", namespace="feature")),
    url(r'^api/v1/', include("osmchadjango.supervise.urls", namespace="supervise")),

    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        url(r'^400/$', defaults.bad_request),
        url(r'^403/$', defaults.permission_denied),
        url(r'^404/$', defaults.page_not_found),
        url(r'^500/$', defaults.server_error),
        ]


# If static files are not intercepted by the web-server, serve them with the dev-server:
if settings.DEBUG is False:   # if DEBUG is True it will be served automatically
    urlpatterns += [
        url(r'^static/(?P<path>.*)$', static_views.serve, {'document_root': settings.STATIC_ROOT}),
        ]
