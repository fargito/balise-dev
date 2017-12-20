from django.contrib import admin
from .models import Task, Comment


class TaskAdmin(admin.ModelAdmin):
	list_display = ('mandat', 'description', 'initiator', 'due_date', 'is_urgent', 'is_closed')
	list_filter = ('is_urgent', 'is_closed', 'mandat__promotion', 'mandat__binet')
	search_fields = ('mandat__binet__nom', 'initiator__username', 'description')

class CommentAdmin(admin.ModelAdmin):
	list_display = ('creation_date', 'author', 'task', 'text', 'admin_only')
	list_filter = ('admin_only', 'creation_date', 'task__mandat__promotion', 'task__mandat__binet')
	search_fields = ('author__username', 'text', 'task__mandat__binet__nom')


admin.site.register(Task, TaskAdmin)
admin.site.register(Comment, CommentAdmin)