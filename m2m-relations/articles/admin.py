from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet

from .models import Article, Tag, Scope


class RelationshipInlineFormset(BaseInlineFormSet):
    def clean(self):
        count = 0
        for form in self.forms:
            if form.cleaned_data.get('is_main'):
                count += 1
            if count > 1:
                raise ValidationError('Вы уже выбрали главный тэг.')
            elif count < 1:
                raise ValidationError('Не выбран главный тэг.')
        return super().clean()


class ScopeInline(admin.TabularInline):
    model = Scope
    extra = 3
    formset = RelationshipInlineFormset


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [ScopeInline]
