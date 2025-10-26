# core/models/feira.py - MODELOS FEIRA E CONGRESSO (NÃO GERENCIADOS)

from django.db import models
from django.contrib.postgres.fields import ArrayField


class Feira(models.Model):
    """
    Model não-gerenciado para tabela 'feiras' do Directus
    As tabelas já existem no banco - Django apenas lê/escreve nelas
    """
    id = models.AutoField(primary_key=True)
    status = models.CharField(max_length=255, default='draft')
    sort = models.IntegerField(null=True, blank=True)
    user_created = models.UUIDField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    user_updated = models.UUIDField(null=True, blank=True)
    date_updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    # Campos específicos da Feira
    nome = models.CharField(max_length=255, null=True, blank=True, verbose_name='Nome da Feira')
    periodo = models.TextField(null=True, blank=True, verbose_name='Período')
    publico_alvo = models.CharField(max_length=255, null=True, blank=True, verbose_name='Público Alvo')
    credenciamento = models.TextField(null=True, blank=True)
    local = models.CharField(max_length=255, null=True, blank=True)
    diferencial = models.CharField(max_length=255, null=True, blank=True)
    Observacoes = models.TextField(null=True, blank=True, verbose_name='Observações')

    # Descontos
    desconto_nivel_1 = models.CharField(max_length=255, null=True, blank=True, verbose_name='Desconto Nível 1')
    desconto_nivel_2 = models.CharField(max_length=255, null=True, blank=True, verbose_name='Desconto Nível 2')
    desconto_cupom_1 = models.CharField(max_length=255, null=True, blank=True, verbose_name='Desconto Cupom 1')
    desconto_cupom_2 = models.CharField(max_length=255, null=True, blank=True, verbose_name='Desconto Cupom 2')

    # Ingressos
    ingresso_black = models.TextField(null=True, blank=True, verbose_name='Ingresso Black')
    ingresso_experience = models.TextField(null=True, blank=True, verbose_name='Ingresso Experience')

    # Congressos relacionados
    lista_congressos = models.TextField(null=True, blank=True)

    # Informações adicionais
    Infraestrutura_e_servicos = models.TextField(null=True, blank=True, verbose_name='Infraestrutura e Serviços')
    Oportunidades_de_negocio = models.TextField(null=True, blank=True, verbose_name='Oportunidades de Negócio')
    Gatilhos_de_urgencia = models.TextField(null=True, blank=True, verbose_name='Gatilhos de Urgência')

    # Credenciamento (armazenado como JSON no Directus)
    credenciamento_categorias = models.TextField(null=True, blank=True)

    # Links
    link_expositores = models.CharField(max_length=255, null=True, blank=True)
    link_embaixadores = models.CharField(max_length=255, null=True, blank=True)

    # Embedding para AI (não usar diretamente no Django)
    # embedding = models.TextField(null=True, blank=True)  # Tipo USER-DEFINED do Postgres

    class Meta:
        db_table = 'feiras'  # Nome da tabela no banco
        managed = False  # Django NÃO vai criar/modificar esta tabela
        verbose_name = 'Feira'
        verbose_name_plural = 'Feiras'
        ordering = ['nome']

    def __str__(self):
        return self.nome or f'Feira #{self.id}'


class Congresso(models.Model):
    """
    Model não-gerenciado para tabela 'congressos' do Directus
    """
    id = models.AutoField(primary_key=True)
    status = models.CharField(max_length=255, default='draft')
    sort = models.IntegerField(null=True, blank=True)
    user_created = models.UUIDField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    user_updated = models.UUIDField(null=True, blank=True)
    date_updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    # Campos específicos do Congresso
    nome = models.CharField(max_length=255, null=True, blank=True, verbose_name='Nome do Congresso')
    feira = models.IntegerField(null=True, blank=True, verbose_name='ID da Feira')  # FK para feiras
    id_feira = models.IntegerField(null=True, blank=True, verbose_name='ID Feira (duplicado)')
    Periodo = models.CharField(max_length=255, null=True, blank=True, verbose_name='Período')

    # Informações
    palestrantes = models.TextField(null=True, blank=True)
    diferencial = models.TextField(null=True, blank=True)

    # Ingressos Black
    ingresso_black_valor = models.TextField(null=True, blank=True, verbose_name='Ingresso Black - Valor')
    ingresso_black_link = models.CharField(max_length=255, null=True, blank=True, verbose_name='Ingresso Black - Link')
    ingresso_black_lote = models.CharField(max_length=255, null=True, blank=True, verbose_name='Ingresso Black - Lote')
    ingresso_black_status = models.CharField(max_length=255, null=True, blank=True, verbose_name='Ingresso Black - Status')

    # Ingressos Experience
    ingresso_experience_valor = models.CharField(max_length=255, null=True, blank=True, verbose_name='Ingresso Experience - Valor')
    ingresso_experience_link = models.CharField(max_length=255, null=True, blank=True, verbose_name='Ingresso Experience - Link')
    ingresso_experience_lote = models.CharField(max_length=255, null=True, blank=True, verbose_name='Ingresso Experience - Lote')
    ingresso_experience_status = models.CharField(max_length=255, null=True, blank=True, verbose_name='Ingresso Experience - Status')

    # Chatwoot
    tag_chatwoot = models.CharField(max_length=255, null=True, blank=True)
    chatwoot = models.CharField(max_length=255, null=True, blank=True)

    # Embedding para AI (não usar diretamente no Django)
    # embedding = models.TextField(null=True, blank=True)  # Tipo USER-DEFINED do Postgres

    class Meta:
        db_table = 'congressos'  # Nome da tabela no banco
        managed = False  # Django NÃO vai criar/modificar esta tabela
        verbose_name = 'Congresso'
        verbose_name_plural = 'Congressos'
        ordering = ['nome']

    def __str__(self):
        return self.nome or f'Congresso #{self.id}'

    def get_feira(self):
        """Retorna objeto Feira relacionado"""
        if self.feira:
            try:
                return Feira.objects.get(id=self.feira)
            except Feira.DoesNotExist:
                return None
        return None
