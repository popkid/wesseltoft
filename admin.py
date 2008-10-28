from django.contrib import admin
from wesseltoft.models import *


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}

class EntryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    
class LinkAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(Category, CategoryAdmin)
admin.site.register(Entry, EntryAdmin)
admin.site.register(Link, LinkAdmin)


