from django.urls import path
from . import views

app_name = "form"

urlpatterns = [
    path("", views.index, name="index"),
    path("save/", views.save_form, name="save-form"),
    path("download-pdf/<uuid:uuid>", views.generate_pdf, name="download-pdf"),
    path("download-talon/<uuid:uuid>", views.download_talon, name="download-talon"),
    # path("new/", views.create_form, name="create"),
    # path("<int:pk>/", views.form_detail, name="detail"),
    # path("<int:pk>/edit/", views.edit_form, name="edit"),
    # path("<int:pk>/delete/", views.delete_form, name="delete"),
    # path("submit/", views.submit_form, name="submit"),
]