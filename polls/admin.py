# Register your models here.

from django.contrib import admin
from .models import Questions, Choice


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
                 (None, {'fields': ['question_text']}),
                 ('Data information', {'fields': ['puplished_date']}),
                ]
    inlines = [ChoiceInline]
    list_display = ('question_text', 'puplished_date', 'was_puplished_recently')
    list_filter = ['puplished_date']
    search_fields = ['question_text']


admin.site.register(Questions, QuestionAdmin)
