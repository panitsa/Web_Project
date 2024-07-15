#admin.py
from django.contrib import admin
from .models import Representative, Activity_news, Villagepublic, Income_expenses, ChatMessage



class RepresentativeAdmin(admin.ModelAdmin):
    
    list_display = ('image', 'first_name', 'last_name', 'position', 'phone_number')
    list_display_links = ('image', 'first_name', 'last_name', 'position', 'phone_number')

admin.site.register(Representative, RepresentativeAdmin)


class Activity_newsAdmin(admin.ModelAdmin):
    list_display = ('image', 'text', 'date', 'time')
    search_fields = ('image', 'text', 'date', 'time')

admin.site.register(Activity_news, Activity_newsAdmin)

class VillagepublicAdmin(admin.ModelAdmin):
    list_display = ('image', 'first_name', 'last_name', 'position', 'phone_number')
    search_fields = ('image', 'first_name', 'last_name', 'position', 'phone_number')
    
admin.site.register(Villagepublic, VillagepublicAdmin)

class Income_expensesAdmin(admin.ModelAdmin):
    list_display = ('date','time', 'income', 'expenses', 'image')
    search_fields = ('date','time', 'income', 'expenses', 'image')

admin.site.register(Income_expenses, Income_expensesAdmin)



class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'message', 'timestamp', 'category', 'user']  # Adjusted to include 'user' instead of 'admin'
    list_filter = ['timestamp', 'category']  # Removed 'admin' from list_filter

admin.site.register(ChatMessage, ChatMessageAdmin)

