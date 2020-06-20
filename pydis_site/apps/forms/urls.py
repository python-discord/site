from django.urls import path

from .views import edit, index


app_name = 'forms'

urlpatterns = [
    path('', index.FormIndexView.as_view(), name="forms_index"),
    path('edit/<str:form_id>', edit.FormEditView.as_view(), name="edit_form")
]
