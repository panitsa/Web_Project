from django.urls import path
from django.contrib.auth.views import *
from django.contrib.auth.decorators import *
from .views import *
from . import *


urlpatterns = [
    
    
    path('', home, name='home'),
    path('login_user/',login_user , name='login_user'),
    path('signup/', signup, name='signup'),
    path('logout_user/', logout_user, name='logout_user'),
    path('representative/', representative, name='representative'),
    path('activity_news/', activity_news, name='activity_news'),
    path('Income_expenses/', income_expenses, name='income_expenses'),
    
    path('admin/login/', LoginView.as_view(), name='admin_login'),
    path('admin/logout/', LogoutView.as_view(), name='admin_logout'),
    
    path('admin/admin_edit/', admin_edit, name='admin_edit'),
    
    path('admin/admin_edit/add_representative/', add_representative, name='add_representative'),
    path('admin/admin_representatives/', admin_representatives, name='admin_representatives'),
    path('admin/edit_representative/<int:representative_id>/', edit_representative, name='edit_representative'),
    path('admin/delete_representative/<int:representative_id>/', delete_representative, name='delete_representative'),
    
    path('admin/admin_edit/add_villagepublic/', add_villagepublic, name='add_villagepublic'),
    path('admin/admin_villagepublic/', admin_villagepublic, name='admin_villagepublic'),
    path('admin/edit_villagepublic/<int:villagepublic_id>/', edit_villagepublic, name='edit_villagepublic'),
    path('admin/delete_villagepublic/<int:villagepublic_id>/', delete_villagepublic, name='delete_villagepublic'),
    
    path('admin/admin_edit/add_activity_news/', add_activity_news, name='add_activity_news'), 
    path('admin/admin_activity_news/', admin_activity_news, name='admin_activity_news'),
    path('admin/edit_activity_news/<int:activity_news_id>/', edit_activity_news, name='edit_activity_news'),
    path('admin/delete_activity_news/<int:activity_news_id>/', delete_activity_news, name='delete_activity_news'),
    
    path('admin/admin_edit/add_income_expenses/', add_income_expenses, name='add_income_expenses'),
    path('admin/admin_income_expenses/', admin_income_expenses, name='admin_income_expenses'),
    path('admin/edit_income_expenses/<int:income_expenses_id>/', edit_income_expenses, name='edit_income_expenses'),
    path('admin/delete_income_expenses/<int:income_expenses_id>/', delete_income_expenses, name='delete_income_expenses'),
    
    path('chat_report/', chat_report, name='chat_report'),
    path('admin/user_list/', admin_user_list, name='admin_user_list'),
    path('admin/admin_edit/admin_road_chat/<int:user_id>/', admin_road_chat, name='admin_road_chat'),
    path('admin/admin_edit/admin_water_chat/<int:user_id>/', admin_water_chat, name='admin_water_chat'),
    path('admin/admin_edit/admin_electricity_chat/<int:user_id>/', admin_electricity_chat, name='admin_electricity_chat'),
    path('admin/admin_edit/admin_general_chat/<int:user_id>/', admin_general_chat, name='admin_general_chat'),
    
    path('road_chat/', road_chat, name='road_chat'), 
    path('water_chat/', water_chat, name='water_chat'),
    path('electricity_chat/', electricity_chat, name='electricity_chat'),
    path('general_chat/', general_chat, name='general_chat'),

    
    path('donation/', donation_form, name='donation_form'),
    path('admin_dashboard/', admin_dashboard, name='admin_dashboard'),
    path('approve_donation/<int:donation_id>/', approve_donation, name='approve_donation'),
    path('donation/<int:donation_id>/generate_pdf/', generate_donation_pdf, name='generate_donation_pdf'),
    path('thank_you/<int:donation_id>/', thank_you_page, name='thank_you_page'),
    
]


