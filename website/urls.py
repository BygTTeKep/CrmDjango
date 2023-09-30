from django.urls import path
from .views import (home,
                    logout_user,
                    register_user,
                    customer_record,
                    delete_record,
                    add_record,
                    update_record,
                    GetRecordListView,
                    GerRecordDetailView,
)

app_name = "website"
urlpatterns = [
    path('', home, name='home'),
    # path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', register_user, name='register'),
    path('record/<int:pk>', customer_record, name='record'),
    path('delete_record/<int:pk>', delete_record, name='delete_record'),
    path('update_record/<int:pk>', update_record, name='update_record'),
    path('add_record/', add_record, name='add_record'),
    path('api/record', GetRecordListView.as_view(), name='apiRecord'),
    path('api/record/<int:pk>', GerRecordDetailView.as_view(), name='apiRecordDetails'),
]