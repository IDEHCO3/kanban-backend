from django.conf.urls import include, url

from scrum import views

app_name="kanban"

urlpatterns = (

    url(r'^scrum-list/',include('scrum.urls',namespace='scrum')),
    url(r'^$', views.index, name='kanban')


)


