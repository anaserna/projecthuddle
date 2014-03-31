""" 
backlog/urls.py - maps url patterns to views 
"""
from django.conf.urls import patterns, url

from backlog import views

urlpatterns = patterns('',
    # UserStory Views
    # VIEW                TEMPLATE                        URL PATTERN
    # --------------------------------------------------------------------
    # IndexView           index.html                      /backlog/
    # DetailView          detail.html                     /backlog/<id>
    # UserStoryCreate     userstory_form.html             /backlog/add/
    # UserStoryUpdate     userstory_edit.html             /backlog/edit/<id>
    # UserStoryDelete     userstory_confirm_delete.html   /backlog/delete/<id>
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<pk>\d+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^add/$', views.UserStoryCreate.as_view(), name='userstory_add'),
    url(r'^edit/(?P<pk>\d+)/$', views.UserStoryUpdate.as_view(), name='userstory_edit'),
    url(r'^delete/(?P<pk>\d+)/$', views.UserStoryDelete.as_view(), name='userstory_delete'),
    
    # SprintBacklogView   sprint_backlog.html             /backlog/sprint/
    url(r'^sprint/$', views.SprintBacklogView.as_view(), name='sprint_backlog'),
    
    # Chart View
    #                                                     /backlog/chart/
    url(r'^sprint/chart/$', views.image_burndown_chart, name='chart'),
    
    # TimeRecord Views
    # VIEW                TEMPLATE                        URL PATTERN
    # --------------------------------------------------------------------
    # TimeRecordList      timerecords_list.html           /backlog/time/
    # TimeRecordView      time_record.html                /backlog/time/<id>
    # TimeRecordCreate    timerecord_form.html            /backlog/time/add/
    # TimeRecordUpdate    edit_time_record.html           /backlog/time/edit/<id>
    # TimeRecordDelete    timerecord_confirm_delete.html  /backlog/time/delete/<id>
    url(r'^time/$', views.TimeRecordList.as_view(), name='timerecords_list'),
    url(r'^time/(?P<pk>\d+)/$', views.TimeRecordView.as_view(), name='time_record'),
    url(r'^time/add/$', views.TimeRecordCreate.as_view(), name='time_record_add'),
    url(r'^time/edit/(?P<pk>\d+)/$', views.TimeRecordUpdate.as_view(), name='time_record_edit'),
    url(r'^time/delete/(?P<pk>\d+)/$', views.TimeRecordDelete.as_view(), name='time_record_delete'),
        
    # Sprint views 
    # VIEW                TEMPLATE                    URL PATTERN
    # --------------------------------------------------------------------
    # SprintListView      sprint_list.html            /backlog/settings/
    # SprintDetailView    settings.html               /backlog/settings/<id>/
    # SprintCreateView    sprint_form.html            /backlog/settings/add/
    # SprintUpdateView    sprint_edit.html            /backlog/settings/edit/<id>
    # SprintDeleteView    sprint_confirm_delete.html  /backlog/delete/<id>
    url(r'^settings/$', views.SprintListView.as_view(), name='settings'),
    url(r'^settings/(?P<pk>\d+)/$', views.SprintDetailView.as_view(), name='view_sprint'),
    url(r'^settings/add/$', views.SprintCreateView.as_view(), name='create_sprint'),
    url(r'^settings/edit/(?P<pk>\d+)/$', views.SprintUpdateView.as_view(), name='sprint_edit'),
    url(r'^settings/delete/(?P<pk>\d+)/$', views.SprintDeleteView.as_view(), name='sprint_delete'),
)