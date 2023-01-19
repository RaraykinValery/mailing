from django.contrib import admin

from manager.models import Client, Mailing, Message

admin.site.register(Client)
admin.site.register(Mailing)
admin.site.register(Message)
