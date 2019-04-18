from django.conf.urls import include, url

from scrum import views

app_name="kanban"

urlpatterns = (

    url(r'^kanban-ggt/scrum-list/',include('scrum.urls',namespace='scrum')),
    url(r'^kanban-ggt/$', views.index, name='kanban')


)


