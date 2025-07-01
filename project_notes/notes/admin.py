from django.contrib import admin
from .models import *
from django.contrib.admin import AdminSite
from django.contrib import admin

class NoteSparrowAdminSite(AdminSite):
    site_header = "NoteSparrow Admin"
    site_title = "NoteSparrow Admin Portal"
    index_title = "Welcome to NoteSparrow Administration"

admin_site = NoteSparrowAdminSite(name='notesparrow_admin')


admin.site.register(Profile)
admin.site.register(Feedback)
admin.site.register(Note)
admin.site.register(SentNote)


admin.site.site_header = "NoteSparrow Admin"
admin.site.site_title = "NoteSparrow Admin Portal"
admin.site.index_title = "Welcome to NoteSparrow Administration"
