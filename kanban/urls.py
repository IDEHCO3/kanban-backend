from django.conf.urls import include, url

app_name="kanban"

urlpatterns = (

    url(r'^scrum-list/',include('scrum.urls',namespace='scrum')),


)


