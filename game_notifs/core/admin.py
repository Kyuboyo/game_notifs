from django.contrib import admin
from django.forms import URLInput

from .models import ImagesModel, CategoriesModel, GamesModel

class ImagesModelAdmin(admin.ModelAdmin):
    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'url':
            kwargs['widget'] = URLInput(attrs={'oninput': 'this.nextElementSibling.href=this.value'})
        return super().formfield_for_dbfield(db_field, **kwargs)

class ImagesModelInLine(admin.TabularInline):
    model = ImagesModel

class CategoriesModelInLine(admin.TabularInline):
    model = CategoriesModel

class GamesModelAdmin(admin.ModelAdmin):
    inlines = [ImagesModelInLine, CategoriesModelInLine]

admin.site.register(ImagesModel, ImagesModelAdmin)
admin.site.register(GamesModel, GamesModelAdmin)