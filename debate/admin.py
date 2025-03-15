from django.contrib import admin
from .models import Debate, Participant, Argument

@admin.register(Debate)
class DebateAdmin(admin.ModelAdmin):
    list_display = ('topic', 'debate_type', 'host', 'is_active', 'created_at')
    list_filter = ('debate_type', 'is_active')
    search_fields = ('topic',)

@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('get_name', 'debate', 'total_score')
    list_filter = ('debate',)
    search_fields = ('guest_name', 'user__username')

    def get_name(self, obj):
        return obj.guest_name if obj.user is None else obj.user.username
    get_name.short_description = 'Participant Name'

@admin.register(Argument)
class ArgumentAdmin(admin.ModelAdmin):
    list_display = ('participant', 'content_preview', 'score', 'submitted_at')
    list_filter = ('participant__debate',)
    search_fields = ('content',)

    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content'
