from django.contrib import admin
from django.contrib.auth.models import Group, User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from django.urls import reverse
from django.db.models import Count
from .models import Event, Edition, Article, Author, NotificationSubscription, BibtexImport


# Customização do admin de usuários para adicionar grupos
class UserAdmin(BaseUserAdmin):
    list_display = BaseUserAdmin.list_display + ('get_groups',)
    list_filter = BaseUserAdmin.list_filter + ('groups',)

    def get_groups(self, obj):
        return ', '.join([group.name for group in obj.groups.all()])
    get_groups.short_description = 'Grupos'


# Re-registrar o modelo User com a versão customizada
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'acronym', 'promoting_entity', 'editions_count', 'created_at')
    list_filter = ('promoting_entity', 'created_at')
    search_fields = ('name', 'acronym', 'promoting_entity')
    prepopulated_fields = {'slug': ('acronym',)}
    readonly_fields = ('created_at', 'updated_at')

    def editions_count(self, obj):
        return obj.editions.count()
    editions_count.short_description = 'Nº Edições'

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('editions')


@admin.register(Edition)
class EditionAdmin(admin.ModelAdmin):
    list_display = ('event', 'year', 'location', 'articles_count', 'created_at')
    list_filter = ('event', 'year', 'created_at')
    search_fields = ('event__name', 'event__acronym', 'location')
    readonly_fields = ('created_at', 'updated_at')
    autocomplete_fields = ('event',)

    def articles_count(self, obj):
        return obj.articles.count()
    articles_count.short_description = 'Nº Artigos'

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('event').annotate(
            articles_count=Count('articles')
        )


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'articles_count', 'created_at')
    search_fields = ('full_name',)
    prepopulated_fields = {'slug': ('full_name',)}
    readonly_fields = ('created_at',)

    def articles_count(self, obj):
        return obj.articles.count()
    articles_count.short_description = 'Nº Artigos'

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            articles_count=Count('articles')
        )


class ArticleAuthorInline(admin.TabularInline):
    model = Article.authors.through
    extra = 1
    autocomplete_fields = ('author',)


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_authors', 'edition', 'pages_range', 'has_pdf', 'created_at')
    list_filter = ('edition__event', 'edition__year', 'created_at')
    search_fields = ('title', 'authors__full_name', 'edition__event__name')
    readonly_fields = ('slug', 'created_at', 'updated_at')
    autocomplete_fields = ('edition',)
    filter_horizontal = ('authors',)
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('title', 'edition', 'authors')
        }),
        ('Paginação e Arquivo', {
            'fields': ('start_page', 'end_page', 'pdf_file')
        }),
        ('Metadados', {
            'fields': ('bibtex_key', 'slug'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def get_authors(self, obj):
        return obj.authors_string[:100] + ('...' if len(obj.authors_string) > 100 else '')
    get_authors.short_description = 'Autores'

    def has_pdf(self, obj):
        if obj.pdf_file:
            return format_html('<span style="color: green;">✓</span>')
        return format_html('<span style="color: red;">✗</span>')
    has_pdf.short_description = 'PDF'

    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'edition__event'
        ).prefetch_related('authors')


@admin.register(NotificationSubscription)
class NotificationSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('full_name', 'email')
    readonly_fields = ('created_at',)
    actions = ['activate_subscriptions', 'deactivate_subscriptions']

    def activate_subscriptions(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} inscrições ativadas.')
    activate_subscriptions.short_description = 'Ativar inscrições selecionadas'

    def deactivate_subscriptions(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} inscrições desativadas.')
    deactivate_subscriptions.short_description = 'Desativar inscrições selecionadas'


@admin.register(BibtexImport)
class BibtexImportAdmin(admin.ModelAdmin):
    list_display = ('id', 'uploaded_by', 'total_entries', 'successful_imports', 
                   'failed_imports', 'success_rate', 'created_at')
    list_filter = ('uploaded_by', 'created_at')
    readonly_fields = ('uploaded_by', 'total_entries', 'successful_imports', 
                      'failed_imports', 'import_log', 'created_at')
    
    def success_rate(self, obj):
        if obj.total_entries > 0:
            rate = (obj.successful_imports / obj.total_entries) * 100
            return f"{rate:.1f}%"
        return "0%"
    success_rate.short_description = 'Taxa de Sucesso'

    def has_add_permission(self, request):
        return False  # Importações são criadas via interface personalizada


# Customização do site admin
admin.site.site_header = 'PaperPaper - Administração'
admin.site.site_title = 'PaperPaper Admin'
admin.site.index_title = 'Painel Administrativo'
