from django.conf.urls.defaults import patterns, url


urlpatterns = patterns(
    'apps.hmi.views',
    url(r'^realtime_watch/$',
        'realtime_watch',
        name='realtime_watch'),
    url(r'^svg_file/(?P<svg_pk>\d+)/$',
        'svg_file',
        name='svg_file'),
    url(r'^energy_plot/$',
        'energy_plot',
        name='energy_plot'),
    url(r'^energy_export/(?P<ai_pk>\d+)/(?P<date_from>\d{4}-\d{1,2}\-\d{1,2})/(?P<date_to>\d{4}-\d{1,2}\-\d{1,2})/$',
        'energy_export',
        name='energy_export'),
    url(r'^month_report/(?P<year>\d{4})/(?P<month>\d{1,2})/$',
        'month_energy_report',
        name='month_energy_report'),
    url(r'^month_report/$',
        'month_energy_report',
        name='month_energy_report'),
)
