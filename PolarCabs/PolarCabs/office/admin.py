from django.contrib import admin
from .models import Office, Person


class PersonInline(admin.TabularInline):
    model = Person
    extra = 1
    fields = ('rank', 'name', 'position')
    verbose_name = "Співробітник"
    verbose_name_plural = "Співробітники"


class OfficeAdmin(admin.ModelAdmin):
    list_display = ('cabinet', 'description', 'person_count')
    search_fields = ('cabinet', 'description')
    list_filter = ('cabinet',)
    inlines = [PersonInline]
    ordering = ['cabinet']
    list_per_page = 20

    def person_count(self, obj):
        return obj.persons.count()

    person_count.short_description = "Кількість співробітників"


class PersonAdmin(admin.ModelAdmin):
    list_display = ('name', 'rank', 'position', 'office')
    search_fields = ('name', 'rank', 'position')
    list_filter = ('office',)
    ordering = ['name']
    list_per_page = 20


admin.site.register(Office, OfficeAdmin)
admin.site.register(Person, PersonAdmin)
