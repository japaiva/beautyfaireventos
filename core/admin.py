from django.contrib import admin
from .models import Feira, Congresso


@admin.register(Feira)
class FeiraAdmin(admin.ModelAdmin):
    list_display = ['id', 'nome', 'periodo', 'local', 'status']
    list_filter = ['status']
    search_fields = ['nome', 'local']
    readonly_fields = ['id', 'date_created', 'date_updated', 'user_created', 'user_updated']

    fieldsets = (
        ('Informações Básicas', {
            'fields': ('id', 'status', 'nome', 'periodo', 'local', 'publico_alvo')
        }),
        ('Credenciamento', {
            'fields': ('credenciamento', 'credenciamento_categorias')
        }),
        ('Ingressos', {
            'fields': ('ingresso_black', 'ingresso_experience')
        }),
        ('Descontos', {
            'fields': ('desconto_nivel_1', 'desconto_nivel_2', 'desconto_cupom_1', 'desconto_cupom_2')
        }),
        ('Links', {
            'fields': ('link_expositores', 'link_embaixadores')
        }),
        ('Detalhes', {
            'fields': ('diferencial', 'Infraestrutura_e_servicos', 'Oportunidades_de_negocio',
                      'Gatilhos_de_urgencia', 'Observacoes', 'lista_congressos'),
            'classes': ('collapse',)
        }),
        ('Auditoria', {
            'fields': ('date_created', 'user_created', 'date_updated', 'user_updated'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Congresso)
class CongressoAdmin(admin.ModelAdmin):
    list_display = ['id', 'nome', 'feira', 'Periodo', 'status']
    list_filter = ['status']
    search_fields = ['nome']
    readonly_fields = ['id', 'date_created', 'date_updated', 'user_created', 'user_updated']

    fieldsets = (
        ('Informações Básicas', {
            'fields': ('id', 'status', 'nome', 'feira', 'id_feira', 'Periodo')
        }),
        ('Conteúdo', {
            'fields': ('palestrantes', 'diferencial')
        }),
        ('Ingressos Black', {
            'fields': ('ingresso_black_valor', 'ingresso_black_link', 'ingresso_black_lote', 'ingresso_black_status')
        }),
        ('Ingressos Experience', {
            'fields': ('ingresso_experience_valor', 'ingresso_experience_link',
                      'ingresso_experience_lote', 'ingresso_experience_status')
        }),
        ('Chatwoot', {
            'fields': ('tag_chatwoot', 'chatwoot'),
            'classes': ('collapse',)
        }),
        ('Auditoria', {
            'fields': ('date_created', 'user_created', 'date_updated', 'user_updated'),
            'classes': ('collapse',)
        }),
    )
