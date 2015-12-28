from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    url(r'^$', views.index_view, name='index'),
    url(r'^add/$', views.add_poll, name='add_poll'),
    url(r'^(?P<pk>\d+)/$', 
        login_required(views.DetailView.as_view()), name='detail'),
    url(r'^(?P<pk>\d+)/results/$', 
        login_required(views.ResultsView.as_view()), name='results'),
    url(r'^(?P<question_id>\d+)/vote/$', views.vote, name='vote'),
]