from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
import os


class Event(models.Model):
    """Modelo para eventos acadêmicos (SBES, SBCARS, etc.)"""
    name = models.CharField(max_length=200, verbose_name="Nome do Evento")
    acronym = models.CharField(max_length=20, unique=True, verbose_name="Sigla")
    promoting_entity = models.CharField(max_length=200, verbose_name="Entidade Promotora")
    slug = models.SlugField(unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")

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
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")

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
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")

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
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")

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
    
    def save(self, *args, **kwargs):
        # Check if this is a new article (no ID means it's new)
        is_new = not self.pk
        print(f"\nSaving article: {self.title}")
        print(f"Is new article: {is_new}")
        
        # First save the article
        super().save(*args, **kwargs)
        
        # Only send notifications for new articles
        if is_new:
            print("This is a new article, preparing to send notifications...")
            try:
                from django.core.mail import send_mail
                from django.conf import settings
                from django.urls import reverse
                
                # Get the base URL
                protocol = 'http'  # or 'https' in production
                domain = 'localhost:8000'  # Update this for production
                
                # For each author of the article
                for author in self.authors.all():
                    # Find active subscriptions for this author
                    subscriptions = NotificationSubscription.objects.filter(
                        full_name__iexact=author.full_name,
                        is_active=True
                    )
                    
                    # Generate the article URL
                    article_url = f'{protocol}://{domain}{reverse("article_detail", kwargs={"pk": self.pk})}'
                    
                    # Send email to each subscriber
                    for subscription in subscriptions:
                        print(f"Encontrada inscrição para {subscription.full_name} ({subscription.email})")
                        subject = f'Novo artigo disponível: {self.title}'
                        message = f"""
Olá {subscription.full_name},

Um novo artigo seu foi adicionado ao sistema PaperPaper:

Título: {self.title}
Evento: {self.edition.event.name}
Ano: {self.edition.year}
Autores: {self.authors_string}

Você pode visualizar o artigo em: {article_url}

Atenciosamente,
Equipe PaperPaper
                        """
                        
                        send_mail(
                            subject,
                            message,
                            settings.DEFAULT_FROM_EMAIL,
                            [subscription.email],
                            fail_silently=False
                        )
            except Exception as e:
                # Log the error but don't prevent article creation
                print(f"Error sending notification: {str(e)}")


class NotificationSubscription(models.Model):
    """Modelo para inscrições de notificações por email"""
    full_name = models.CharField(max_length=200, verbose_name="Nome Completo")
    email = models.EmailField(verbose_name="Email")
    is_active = models.BooleanField(default=True, verbose_name="Ativo")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")

    class Meta:
        verbose_name = "Inscrição de Notificação"
        verbose_name_plural = "Inscrições de Notificação"
        unique_together = ['full_name', 'email']

    def __str__(self):
        return f"{self.full_name} - {self.email}"


class BibtexImport(models.Model):
    """Modelo para rastrear importações de BibTeX"""
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Enviado por")
    bibtex_file = models.FileField(upload_to='imports/bibtex/', verbose_name="Arquivo BibTeX")
    zip_file = models.FileField(upload_to='imports/pdfs/', null=True, blank=True, verbose_name="Arquivo ZIP")
    total_entries = models.PositiveIntegerField(default=0, verbose_name="Total de entradas")
    successful_imports = models.PositiveIntegerField(default=0, verbose_name="Importações bem-sucedidas")
    failed_imports = models.PositiveIntegerField(default=0, verbose_name="Importações falhas")
    import_log = models.TextField(blank=True, verbose_name="Log de Importação")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")

    class Meta:
        verbose_name = "Importação BibTeX"
        verbose_name_plural = "Importações BibTeX"
        ordering = ['-created_at']

    def __str__(self):
        return f"Importação {self.id} - {self.created_at.strftime('%d/%m/%Y %H:%M')}"


def send_article_notifications(article):
    """Função auxiliar para enviar notificações"""
    try:
        from django.core.mail import send_mail
        from django.conf import settings
        from django.urls import reverse
        
        print(f"\nPreparando notificações para o artigo: {article.title}")
        
        # Get the site domain from Sites framework
        from django.contrib.sites.models import Site
        current_site = Site.objects.get_current()
        protocol = 'https' if not settings.DEBUG else 'http'
        
        # For each author of the article
        for author in article.authors.all():
            print(f"Verificando notificações para o autor: {author.full_name}")
            # Find active subscriptions for this author
            subscriptions = NotificationSubscription.objects.filter(
                full_name__iexact=author.full_name,
                is_active=True
            )
            
            print(f"Encontradas {subscriptions.count()} inscrições ativas")
            
            # Generate the article URL
            article_url = f'{protocol}://{current_site.domain}{reverse("article_detail", kwargs={"pk": article.pk})}'
            
            # Send email to each subscriber
            for subscription in subscriptions:
                print(f"Enviando email para {subscription.email}")
                subject = f'Novo artigo disponível: {article.title}'
                message = f"""
Olá {subscription.full_name},

Um novo artigo seu foi adicionado ao sistema PaperPaper:

Título: {article.title}
Evento: {article.edition.event.name}
Ano: {article.edition.year}
Autores: {article.authors_string}

Você pode visualizar o artigo em: {article_url}

Atenciosamente,
Equipe PaperPaper
                """
                
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [subscription.email],
                    fail_silently=False
                )
                print(f"Email enviado com sucesso para {subscription.email}")
    except Exception as e:
        print(f"Erro ao enviar notificação: {str(e)}")


@receiver(m2m_changed, sender=Article.authors.through)
def handle_article_authors_changed(sender, instance, action, **kwargs):
    """Handler para quando autores são adicionados a um artigo"""
    print(f"\nAutores m2m alterados: {action}")
    if action == "post_add":
        print("Autores foram adicionados, enviando notificações...")
        send_article_notifications(instance)
