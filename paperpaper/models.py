from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse
import os


class Event(models.Model):
    """Modelo para eventos acadêmicos (SBES, SBCARS, etc.)"""
    name = models.CharField(max_length=200, verbose_name="Nome do Evento")
    acronym = models.CharField(max_length=20, unique=True, verbose_name="Sigla")
    promoting_entity = models.CharField(max_length=200, verbose_name="Entidade Promotora")
    slug = models.SlugField(unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Evento"
        verbose_name_plural = "Eventos"
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.acronym})"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.acronym.lower())
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('event_detail', kwargs={'slug': self.slug})


class Edition(models.Model):
    """Modelo para edições de eventos (SBES 2024, etc.)"""
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='editions')
    year = models.PositiveIntegerField(verbose_name="Ano")
    location = models.CharField(max_length=200, verbose_name="Local")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Edição"
        verbose_name_plural = "Edições"
        unique_together = ['event', 'year']
        ordering = ['-year']

    def __str__(self):
        return f"{self.event.acronym} {self.year} - {self.location}"

    def get_absolute_url(self):
        return reverse('edition_detail', kwargs={'slug': self.event.slug, 'year': self.year})


class Author(models.Model):
    """Modelo para autores de artigos"""
    full_name = models.CharField(max_length=200, verbose_name="Nome Completo")
    slug = models.SlugField(unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Autor"
        verbose_name_plural = "Autores"
        ordering = ['full_name']

    def __str__(self):
        return self.full_name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.full_name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('author_detail', kwargs={'slug': self.slug})


def article_pdf_upload_path(instance, filename):
    """Função para definir o caminho de upload dos PDFs"""
    return f'articles/{instance.edition.event.slug}/{instance.edition.year}/{filename}'


class Article(models.Model):
    """Modelo para artigos acadêmicos"""
    title = models.CharField(max_length=500, verbose_name="Título")
    authors = models.ManyToManyField(Author, related_name='articles', verbose_name="Autores")
    edition = models.ForeignKey(Edition, on_delete=models.CASCADE, related_name='articles')
    start_page = models.PositiveIntegerField(verbose_name="Página Inicial", null=True, blank=True)
    end_page = models.PositiveIntegerField(verbose_name="Página Final", null=True, blank=True)
    pdf_file = models.FileField(upload_to=article_pdf_upload_path, verbose_name="Arquivo PDF", null=True, blank=True)
    bibtex_key = models.CharField(max_length=100, verbose_name="Chave BibTeX", blank=True)
    slug = models.SlugField(max_length=600, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Artigo"
        verbose_name_plural = "Artigos"
        ordering = ['-edition__year', 'title']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title[:100])
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('article_detail', kwargs={'pk': self.pk})

    @property
    def pages_range(self):
        """Retorna o range de páginas formatado"""
        if self.start_page and self.end_page:
            return f"{self.start_page}--{self.end_page}"
        return ""

    @property
    def authors_list(self):
        """Retorna lista de nomes dos autores"""
        return [author.full_name for author in self.authors.all()]

    @property
    def authors_string(self):
        """Retorna string com nomes dos autores separados por vírgula"""
        return ", ".join(self.authors_list)


class NotificationSubscription(models.Model):
    """Modelo para inscrições de notificações por email"""
    full_name = models.CharField(max_length=200, verbose_name="Nome Completo")
    email = models.EmailField(verbose_name="Email")
    is_active = models.BooleanField(default=True, verbose_name="Ativo")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Inscrição de Notificação"
        verbose_name_plural = "Inscrições de Notificação"
        unique_together = ['full_name', 'email']

    def __str__(self):
        return f"{self.full_name} - {self.email}"


class BibtexImport(models.Model):
    """Modelo para rastrear importações de BibTeX"""
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    bibtex_file = models.FileField(upload_to='imports/bibtex/')
    zip_file = models.FileField(upload_to='imports/pdfs/', null=True, blank=True)
    total_entries = models.PositiveIntegerField(default=0)
    successful_imports = models.PositiveIntegerField(default=0)
    failed_imports = models.PositiveIntegerField(default=0)
    import_log = models.TextField(blank=True, verbose_name="Log de Importação")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Importação BibTeX"
        verbose_name_plural = "Importações BibTeX"
        ordering = ['-created_at']

    def __str__(self):
        return f"Importação {self.id} - {self.created_at.strftime('%d/%m/%Y %H:%M')}"
