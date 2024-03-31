from django.urls import path
from . import views

urlpatterns = [
    # ...
    path('studentindex/', views.student_index, name='studentindex'),
    path('student/generalbooks/',views.general_books_view,name='generalbooks'),
    path('student/journal/',views.journals_books_view,name='journals'),
    path('student/papers/',views.papers_books_view,name='papers'),
    path('student/novels/',views.novels_books_view,name='novels'),
    path('student/first_year_1_1/',views.first_year_1_1,name='first_year_1_1'),
    path('student/first_year_1_2/',views.first_year_1_2,name='first_year_1_2'),
    path('student/second_year_2_1/',views.second_year_2_1,name='second_year_2_1'),
     path('student/second_year_2_2/',views.second_year_2_2,name='second_year_2_2'),
    path('student/third_year_3_1/',views.third_year_3_1,name='third_year_3_1'),
    path('student/third_year_3_2/',views.third_year_3_2,name='third_year_3_2'),
    path('student/fourth_year_4_1/',views.fourth_year_4_1,name='fourth_year_4_1'),
    path('student/fourth_year_4_2/',views.fourth_year_4_2,name='fourth_year_4_2'), 
    path('student/fetchusertickets/',views.fetch_user_ticket,name='fetchusersticket'),
    path('student/profile/',views.studentprofile,name='profile'),
    path('student/change_password/', views.change_password, name='change_password'),
    path('libraryadmin/profile/logout',views.logout,name='logout'),
]
