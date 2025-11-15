"""
Testes de Unidade e Integração para a aplicação PaperPaper
"""
import unittest
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from unittest.mock import Mock, patch, MagicMock

from .models import Event, Edition, Article, Author, NotificationSubscription
from .views import (
    home, events_list, authors_list, search_articles,
    event_detail, edition_detail, author_detail, article_detail,
    notification_subscribe, process_bibtex_entry
)


class EventModelTests(TestCase):
    """Testes para o modelo Event"""

    def setUp(self):
        """Configuração para cada teste"""
        self.event = Event.objects.create(
            name='International Conference on Software Engineering',
            acronym='ICSE',
            promoting_entity='IEEE'
        )

    def test_event_creation(self):
        """Testa criação de um evento"""
        self.assertEqual(self.event.name, 'International Conference on Software Engineering')
        self.assertEqual(self.event.acronym, 'ICSE')
        self.assertEqual(self.event.promoting_entity, 'IEEE')

    def test_event_slug_generation(self):
        """Testa geração automática do slug"""
        self.assertEqual(self.event.slug, 'icse')

    def test_event_str_representation(self):
        """Testa representação em string do evento"""
        expected_str = f"{self.event.name} ({self.event.acronym})"
        self.assertEqual(str(self.event), expected_str)

    def test_event_unique_acronym(self):
        """Testa constraint de acronym único"""
        with self.assertRaises(Exception):
            Event.objects.create(
                name='Another Conference',
                acronym='ICSE',  # Duplicado
                promoting_entity='IEEE'
            )

    def test_event_absolute_url(self):
        """Testa geração de URL absoluta do evento"""
        expected_url = reverse('event_detail', kwargs={'slug': self.event.slug})
        self.assertEqual(self.event.get_absolute_url(), expected_url)


class EditionModelTests(TestCase):
    """Testes para o modelo Edition"""

    def setUp(self):
        """Configuração para cada teste"""
        self.event = Event.objects.create(
            name='ICSE',
            acronym='ICSE',
            promoting_entity='IEEE'
        )
        self.edition = Edition.objects.create(
            event=self.event,
            year=2024,
            location='Lisbon, Portugal'
        )

    def test_edition_creation(self):
        """Testa criação de uma edição"""
        self.assertEqual(self.edition.year, 2024)
        self.assertEqual(self.edition.location, 'Lisbon, Portugal')
        self.assertEqual(self.edition.event, self.event)

    def test_edition_str_representation(self):
        """Testa representação em string da edição"""
        expected_str = f"{self.event.acronym} {self.edition.year} - {self.edition.location}"
        self.assertEqual(str(self.edition), expected_str)

    def test_edition_unique_constraint(self):
        """Testa constraint de evento e ano únicos"""
        with self.assertRaises(Exception):
            Edition.objects.create(
                event=self.event,
                year=2024,  # Ano duplicado
                location='Another Location'
            )

    def test_edition_ordering(self):
        """Testa ordenação por ano decrescente"""
        Edition.objects.create(event=self.event, year=2023, location='Loc1')
        Edition.objects.create(event=self.event, year=2025, location='Loc2')
        
        editions = Edition.objects.all()
        self.assertEqual(editions[0].year, 2025)


class AuthorModelTests(TestCase):
    """Testes para o modelo Author"""

    def setUp(self):
        """Configuração para cada teste"""
        self.author = Author.objects.create(full_name='John Doe')

    def test_author_creation(self):
        """Testa criação de um autor"""
        self.assertEqual(self.author.full_name, 'John Doe')

    def test_author_slug_generation(self):
        """Testa geração automática do slug"""
        self.assertEqual(self.author.slug, 'john-doe')

    def test_author_str_representation(self):
        """Testa representação em string do autor"""
        self.assertEqual(str(self.author), 'John Doe')

    def test_author_unique_slug(self):
        """Testa constraint de slug único"""
        with self.assertRaises(Exception):
            Author.objects.create(full_name='John Doe')

    def test_author_absolute_url(self):
        """Testa geração de URL absoluta do autor"""
        expected_url = reverse('author_detail', kwargs={'slug': self.author.slug})
        self.assertEqual(self.author.get_absolute_url(), expected_url)


class ArticleModelTests(TestCase):
    """Testes para o modelo Article"""

    def setUp(self):
        """Configuração para cada teste"""
        self.event = Event.objects.create(name='ICSE', acronym='ICSE', promoting_entity='IEEE')
        self.edition = Edition.objects.create(event=self.event, year=2024, location='Lisbon')
        self.author1 = Author.objects.create(full_name='John Doe')
        self.author2 = Author.objects.create(full_name='Jane Smith')
        self.article = Article.objects.create(
            title='A Study on Software Engineering',
            edition=self.edition,
            start_page=1,
            end_page=15
        )
        self.article.authors.add(self.author1, self.author2)

    def test_article_creation(self):
        """Testa criação de um artigo"""
        self.assertEqual(self.article.title, 'A Study on Software Engineering')
        self.assertEqual(self.article.start_page, 1)
        self.assertEqual(self.article.end_page, 15)

    def test_article_pages_range_property(self):
        """Testa propriedade de range de páginas"""
        self.assertEqual(self.article.pages_range, "1--15")

    def test_article_authors_list_property(self):
        """Testa propriedade de lista de autores"""
        authors_list = self.article.authors_list
        self.assertEqual(len(authors_list), 2)
        self.assertIn('John Doe', authors_list)
        self.assertIn('Jane Smith', authors_list)

    def test_article_authors_string_property(self):
        """Testa propriedade de string de autores"""
        authors_string = self.article.authors_string
        self.assertIn('John Doe', authors_string)
        self.assertIn('Jane Smith', authors_string)

    def test_article_slug_generation(self):
        """Testa geração automática do slug"""
        self.assertIsNotNone(self.article.slug)
        self.assertIn('study', self.article.slug.lower())

    def test_article_absolute_url(self):
        """Testa geração de URL absoluta do artigo"""
        expected_url = reverse('article_detail', kwargs={'pk': self.article.pk})
        self.assertEqual(self.article.get_absolute_url(), expected_url)

    def test_article_pages_range_empty(self):
        """Testa propriedade pages_range quando não há páginas"""
        article_no_pages = Article.objects.create(
            title='Another Article',
            edition=self.edition
        )
        self.assertEqual(article_no_pages.pages_range, "")


class HomeViewTests(TestCase):
    """Testes para a view home"""

    def setUp(self):
        """Configuração para cada teste"""
        self.client = Client()

    def test_home_view_status_code(self):
        """Testa código de status HTTP da página inicial"""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_home_view_template(self):
        """Testa template usado pela view home"""
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, 'paperpaper/home.html')

    def test_home_view_context_keys(self):
        """Testa presença de chaves obrigatórias no contexto"""
        response = self.client.get(reverse('home'))
        context = response.context
        
        self.assertIn('events_count', context)
        self.assertIn('articles_count', context)
        self.assertIn('authors_count', context)
        self.assertIn('recent_articles', context)

    def test_home_view_statistics_accuracy(self):
        """Testa precisão das estatísticas na página inicial"""
        # Criar dados de teste
        event = Event.objects.create(name='ICSE', acronym='ICSE', promoting_entity='IEEE')
        edition = Edition.objects.create(event=event, year=2024, location='Lisbon')
        author = Author.objects.create(full_name='John Doe')
        article = Article.objects.create(title='Test Article', edition=edition)
        article.authors.add(author)

        response = self.client.get(reverse('home'))
        context = response.context

        self.assertEqual(context['events_count'], 1)
        self.assertEqual(context['articles_count'], 1)
        self.assertEqual(context['authors_count'], 1)

    def test_home_view_recent_articles_limit(self):
        """Testa que apenas 5 artigos recentes são exibidos"""
        event = Event.objects.create(name='ICSE', acronym='ICSE', promoting_entity='IEEE')
        edition = Edition.objects.create(event=event, year=2024, location='Lisbon')

        # Criar 10 artigos
        for i in range(10):
            Article.objects.create(title=f'Article {i}', edition=edition)

        response = self.client.get(reverse('home'))
        context = response.context

        self.assertEqual(len(context['recent_articles']), 5)


class EventsListViewTests(TestCase):
    """Testes para a view events_list"""

    def setUp(self):
        """Configuração para cada teste"""
        self.client = Client()
        self.event1 = Event.objects.create(name='ICSE', acronym='ICSE', promoting_entity='IEEE')
        self.event2 = Event.objects.create(name='FSE', acronym='FSE', promoting_entity='ACM')

    def test_events_list_status_code(self):
        """Testa código de status HTTP da lista de eventos"""
        response = self.client.get(reverse('events_list'))
        self.assertEqual(response.status_code, 200)

    def test_events_list_template(self):
        """Testa template usado pela view events_list"""
        response = self.client.get(reverse('events_list'))
        self.assertTemplateUsed(response, 'paperpaper/events_list.html')

    def test_events_list_context(self):
        """Testa contexto da view events_list"""
        response = self.client.get(reverse('events_list'))
        context = response.context
        
        self.assertIn('events', context)
        self.assertEqual(len(context['events']), 2)

    def test_events_list_ordering(self):
        """Testa ordenação alfabética dos eventos"""
        response = self.client.get(reverse('events_list'))
        events = response.context['events']
        
        self.assertEqual(events[0].name, 'FSE')
        self.assertEqual(events[1].name, 'ICSE')


class SearchArticlesViewTests(TestCase):
    """Testes para a view search_articles"""

    def setUp(self):
        """Configuração para cada teste"""
        self.client = Client()
        self.event = Event.objects.create(name='ICSE', acronym='ICSE', promoting_entity='IEEE')
        self.edition = Edition.objects.create(event=self.event, year=2024, location='Lisbon')
        self.author = Author.objects.create(full_name='John Doe')
        
        self.article = Article.objects.create(
            title='Software Engineering Practices',
            edition=self.edition
        )
        self.article.authors.add(self.author)

    def test_search_articles_status_code(self):
        """Testa código de status HTTP da busca"""
        response = self.client.get(reverse('search_articles'))
        self.assertEqual(response.status_code, 200)

    def test_search_articles_template(self):
        """Testa template usado pela view search_articles"""
        response = self.client.get(reverse('search_articles'))
        self.assertTemplateUsed(response, 'paperpaper/search.html')

    def test_search_articles_by_title(self):
        """Testa busca de artigos por título"""
        response = self.client.get(reverse('search_articles'), {'q': 'Engineering', 'type': 'title'})
        context = response.context

        self.assertIn('results', context)
        self.assertEqual(len(context['results']), 1)
        self.assertEqual(context['results'][0].title, 'Software Engineering Practices')

    def test_search_articles_by_author(self):
        """Testa busca de artigos por autor"""
        response = self.client.get(reverse('search_articles'), {'q': 'John', 'type': 'author'})
        context = response.context

        self.assertEqual(len(context['results']), 1)
        self.assertEqual(list(context['results'][0].authors.all()), [self.author])

    def test_search_articles_by_event(self):
        """Testa busca de artigos por evento"""
        response = self.client.get(reverse('search_articles'), {'q': 'ICSE', 'type': 'event'})
        context = response.context

        self.assertEqual(len(context['results']), 1)

    def test_search_articles_empty_query(self):
        """Testa busca com query vazia"""
        response = self.client.get(reverse('search_articles'), {'q': ''})
        context = response.context

        self.assertEqual(len(context['results']), 0)

    def test_search_articles_no_results(self):
        """Testa busca sem resultados"""
        response = self.client.get(reverse('search_articles'), {'q': 'NonExistent', 'type': 'title'})
        context = response.context

        self.assertEqual(len(context['results']), 0)


class AuthorsListViewTests(TestCase):
    """Testes para a view authors_list"""

    def setUp(self):
        """Configuração para cada teste"""
        self.client = Client()
        self.author1 = Author.objects.create(full_name='Alice Smith')
        self.author2 = Author.objects.create(full_name='Bob Johnson')

    def test_authors_list_status_code(self):
        """Testa código de status HTTP da lista de autores"""
        response = self.client.get(reverse('authors_list'))
        self.assertEqual(response.status_code, 200)

    def test_authors_list_template(self):
        """Testa template usado pela view authors_list"""
        response = self.client.get(reverse('authors_list'))
        self.assertTemplateUsed(response, 'paperpaper/authors_list.html')

    def test_authors_list_context(self):
        """Testa contexto da view authors_list"""
        response = self.client.get(reverse('authors_list'))
        context = response.context

        self.assertIn('authors', context)
        self.assertIn('is_paginated', context)
        self.assertIn('query', context)

    def test_authors_list_search_filter(self):
        """Testa filtro de busca na lista de autores"""
        response = self.client.get(reverse('authors_list'), {'q': 'Alice'})
        context = response.context
        authors = list(context['authors'])

        self.assertEqual(len(authors), 1)
        self.assertEqual(authors[0].full_name, 'Alice Smith')

    def test_authors_list_pagination(self):
        """Testa paginação da lista de autores"""
        # Criar 60 autores para testar paginação (50 por página)
        for i in range(60):
            Author.objects.create(full_name=f'Author {i:03d}')

        response = self.client.get(reverse('authors_list'))
        context = response.context

        self.assertTrue(context['is_paginated'])
        self.assertEqual(len(context['authors']), 50)


class EventDetailViewTests(TestCase):
    """Testes para a view event_detail"""

    def setUp(self):
        """Configuração para cada teste"""
        self.client = Client()
        self.event = Event.objects.create(name='ICSE', acronym='ICSE', promoting_entity='IEEE')
        self.edition1 = Edition.objects.create(event=self.event, year=2024, location='Lisbon')
        self.edition2 = Edition.objects.create(event=self.event, year=2023, location='Melbourne')

    def test_event_detail_status_code(self):
        """Testa código de status HTTP da página de evento"""
        response = self.client.get(self.event.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_event_detail_template(self):
        """Testa template usado pela view event_detail"""
        response = self.client.get(self.event.get_absolute_url())
        self.assertTemplateUsed(response, 'paperpaper/event_detail.html')

    def test_event_detail_context(self):
        """Testa contexto da view event_detail"""
        response = self.client.get(self.event.get_absolute_url())
        context = response.context

        self.assertIn('event', context)
        self.assertIn('editions', context)
        self.assertEqual(context['event'], self.event)

    def test_event_detail_editions_ordering(self):
        """Testa ordenação decrescente por ano"""
        response = self.client.get(self.event.get_absolute_url())
        editions = list(response.context['editions'])

        self.assertEqual(editions[0].year, 2024)
        self.assertEqual(editions[1].year, 2023)

    def test_event_detail_not_found(self):
        """Testa erro 404 para evento inexistente"""
        response = self.client.get(reverse('event_detail', kwargs={'slug': 'nonexistent'}))
        self.assertEqual(response.status_code, 404)


class EditionDetailViewTests(TestCase):
    """Testes para a view edition_detail"""

    def setUp(self):
        """Configuração para cada teste"""
        self.client = Client()
        self.event = Event.objects.create(name='ICSE', acronym='ICSE', promoting_entity='IEEE')
        self.edition = Edition.objects.create(event=self.event, year=2024, location='Lisbon')
        self.author = Author.objects.create(full_name='John Doe')
        
        self.article1 = Article.objects.create(title='Article A', edition=self.edition)
        self.article2 = Article.objects.create(title='Article B', edition=self.edition)
        self.article1.authors.add(self.author)

    def test_edition_detail_status_code(self):
        """Testa código de status HTTP da página de edição"""
        response = self.client.get(self.edition.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_edition_detail_template(self):
        """Testa template usado pela view edition_detail"""
        response = self.client.get(self.edition.get_absolute_url())
        self.assertTemplateUsed(response, 'paperpaper/edition_detail.html')

    def test_edition_detail_context(self):
        """Testa contexto da view edition_detail"""
        response = self.client.get(self.edition.get_absolute_url())
        context = response.context

        self.assertIn('event', context)
        self.assertIn('edition', context)
        self.assertIn('articles', context)

    def test_edition_detail_articles_count(self):
        """Testa quantidade de artigos na edição"""
        response = self.client.get(self.edition.get_absolute_url())
        articles = list(response.context['articles'])

        self.assertEqual(len(articles), 2)

    def test_edition_detail_not_found(self):
        """Testa erro 404 para edição inexistente"""
        response = self.client.get(
            reverse('edition_detail', kwargs={'slug': self.event.slug, 'year': 9999})
        )
        self.assertEqual(response.status_code, 404)


class AuthorDetailViewTests(TestCase):
    """Testes para a view author_detail"""

    def setUp(self):
        """Configuração para cada teste"""
        self.client = Client()
        self.author = Author.objects.create(full_name='John Doe')
        
        # Criar eventos e edições
        self.event = Event.objects.create(name='ICSE', acronym='ICSE', promoting_entity='IEEE')
        self.edition1 = Edition.objects.create(event=self.event, year=2024, location='Lisbon')
        self.edition2 = Edition.objects.create(event=self.event, year=2023, location='Melbourne')
        
        # Criar artigos
        self.article1 = Article.objects.create(title='Article 2024', edition=self.edition1)
        self.article2 = Article.objects.create(title='Article 2023', edition=self.edition2)
        
        self.article1.authors.add(self.author)
        self.article2.authors.add(self.author)

    def test_author_detail_status_code(self):
        """Testa código de status HTTP da página de autor"""
        response = self.client.get(self.author.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_author_detail_template(self):
        """Testa template usado pela view author_detail"""
        response = self.client.get(self.author.get_absolute_url())
        self.assertTemplateUsed(response, 'paperpaper/author_detail.html')

    def test_author_detail_context(self):
        """Testa contexto da view author_detail"""
        response = self.client.get(self.author.get_absolute_url())
        context = response.context

        self.assertIn('author', context)
        self.assertIn('articles_by_year', context)
        self.assertIn('total_articles', context)

    def test_author_detail_articles_by_year_organization(self):
        """Testa organização de artigos por ano"""
        response = self.client.get(self.author.get_absolute_url())
        articles_by_year = response.context['articles_by_year']

        self.assertIn(2024, articles_by_year)
        self.assertIn(2023, articles_by_year)
        self.assertEqual(len(articles_by_year[2024]), 1)

    def test_author_detail_total_articles_count(self):
        """Testa contagem total de artigos do autor"""
        response = self.client.get(self.author.get_absolute_url())
        context = response.context

        self.assertEqual(context['total_articles'], 2)


class ArticleDetailViewTests(TestCase):
    """Testes para a view article_detail"""

    def setUp(self):
        """Configuração para cada teste"""
        self.client = Client()
        self.event = Event.objects.create(name='ICSE', acronym='ICSE', promoting_entity='IEEE')
        self.edition = Edition.objects.create(event=self.event, year=2024, location='Lisbon')
        self.author = Author.objects.create(full_name='John Doe')
        
        self.article = Article.objects.create(
            title='Software Engineering Practices',
            edition=self.edition,
            start_page=1,
            end_page=20
        )
        self.article.authors.add(self.author)

    def test_article_detail_status_code(self):
        """Testa código de status HTTP da página de artigo"""
        response = self.client.get(self.article.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_article_detail_template(self):
        """Testa template usado pela view article_detail"""
        response = self.client.get(self.article.get_absolute_url())
        self.assertTemplateUsed(response, 'paperpaper/article_detail.html')

    def test_article_detail_context(self):
        """Testa contexto da view article_detail"""
        response = self.client.get(self.article.get_absolute_url())
        context = response.context

        self.assertIn('article', context)
        self.assertEqual(context['article'], self.article)

    def test_article_detail_not_found(self):
        """Testa erro 404 para artigo inexistente"""
        response = self.client.get(reverse('article_detail', kwargs={'pk': 9999}))
        self.assertEqual(response.status_code, 404)


class NotificationSubscriptionModelTests(TestCase):
    """Testes para o modelo NotificationSubscription"""

    def setUp(self):
        """Configuração para cada teste"""
        self.subscription = NotificationSubscription.objects.create(
            full_name='John Doe',
            email='john@example.com',
            is_active=True
        )

    def test_subscription_creation(self):
        """Testa criação de uma subscrição"""
        self.assertEqual(self.subscription.full_name, 'John Doe')
        self.assertEqual(self.subscription.email, 'john@example.com')
        self.assertTrue(self.subscription.is_active)

    def test_subscription_str_representation(self):
        """Testa representação em string da subscrição"""
        expected_str = f"{self.subscription.full_name} - {self.subscription.email}"
        self.assertEqual(str(self.subscription), expected_str)

    def test_subscription_unique_constraint(self):
        """Testa constraint de name e email únicos"""
        with self.assertRaises(Exception):
            NotificationSubscription.objects.create(
                full_name='John Doe',
                email='john@example.com'
            )


class NotificationSubscribeViewTests(TestCase):
    """Testes para a view notification_subscribe"""

    def setUp(self):
        """Configuração para cada teste"""
        self.client = Client()

    def test_notification_subscribe_get_status_code(self):
        """Testa código de status HTTP (GET) da página de subscrição"""
        response = self.client.get(reverse('notification_subscribe'))
        self.assertEqual(response.status_code, 200)

    def test_notification_subscribe_template(self):
        """Testa template usado pela view notification_subscribe"""
        response = self.client.get(reverse('notification_subscribe'))
        self.assertTemplateUsed(response, 'paperpaper/notification_subscribe.html')

    def test_notification_subscribe_post_creates_subscription(self):
        """Testa criação de subscrição via POST"""
        data = {
            'full_name': 'John Doe',
            'email': 'john@example.com'
        }
        response = self.client.post(reverse('notification_subscribe'), data)

        # Verifica se a subscrição foi criada
        self.assertTrue(
            NotificationSubscription.objects.filter(
                full_name='John Doe',
                email='john@example.com'
            ).exists()
        )

    def test_notification_subscribe_post_activates_inactive(self):
        """Testa reativação de subscrição inativa"""
        # Criar subscrição inativa
        subscription = NotificationSubscription.objects.create(
            full_name='Jane Smith',
            email='jane@example.com',
            is_active=False
        )

        data = {
            'full_name': 'Jane Smith',
            'email': 'jane@example.com'
        }
        response = self.client.post(reverse('notification_subscribe'), data)

        # Verifica se a subscrição foi reativada
        subscription.refresh_from_db()
        self.assertTrue(subscription.is_active)

    def test_notification_subscribe_post_missing_fields(self):
        """Testa POST com campos faltando"""
        data = {
            'full_name': 'John Doe'
            # email faltando
        }
        response = self.client.post(reverse('notification_subscribe'), data)

        # Verifica que a subscrição não foi criada
        self.assertFalse(
            NotificationSubscription.objects.filter(
                full_name='John Doe'
            ).exists()
        )

class SendArticleNotificationsTests(TestCase):
    """Testes para a função send_article_notifications"""

    def setUp(self):
        """Configuração para cada teste"""
        self.event = Event.objects.create(
            name='ICSE',
            acronym='ICSE',
            promoting_entity='IEEE'
        )
        self.edition = Edition.objects.create(
            event=self.event,
            year=2024,
            location='Lisbon'
        )
        self.author = Author.objects.create(full_name='John Doe')
        self.article = Article.objects.create(
            title='Test Article',
            edition=self.edition
        )
        self.article.authors.add(self.author)

    @patch('django.core.mail.send_mail')  # Changed: patch where send_mail is imported FROM
    def test_send_notification_to_active_subscriber(self, mock_send_mail):
        """Testa envio de notificação para assinante ativo"""
        from paperpaper.models import send_article_notifications
        
        # Criar assinatura ativa
        subscription = NotificationSubscription.objects.create(
            full_name='John Doe',
            email='john@example.com',
            is_active=True
        )

        # Chamar a função
        send_article_notifications(self.article)

        # Verificar que send_mail foi chamado
        self.assertTrue(mock_send_mail.called)
        self.assertEqual(mock_send_mail.call_count, 1)

    @patch('django.core.mail.send_mail')  # Changed
    def test_notification_email_subject(self, mock_send_mail):
        """Testa assunto do email de notificação"""
        from paperpaper.models import send_article_notifications
        
        NotificationSubscription.objects.create(
            full_name='John Doe',
            email='john@example.com',
            is_active=True
        )

        send_article_notifications(self.article)

        # Verificar o assunto do email
        call_args = mock_send_mail.call_args
        subject = call_args[0][0]  # Primeiro argumento
        self.assertIn('Novo artigo disponível', subject)
        self.assertIn('Test Article', subject)

    @patch('django.core.mail.send_mail')  # Changed
    def test_notification_email_content(self, mock_send_mail):
        """Testa conteúdo do email de notificação"""
        from paperpaper.models import send_article_notifications
        
        NotificationSubscription.objects.create(
            full_name='John Doe',
            email='john@example.com',
            is_active=True
        )

        send_article_notifications(self.article)

        # Verificar o conteúdo do email
        call_args = mock_send_mail.call_args
        message = call_args[0][1]  # Segundo argumento
        
        self.assertIn('John Doe', message)
        self.assertIn('Test Article', message)
        self.assertIn('ICSE', message)
        self.assertIn('2024', message)

    @patch('django.core.mail.send_mail')  # Changed
    def test_notification_email_recipient(self, mock_send_mail):
        """Testa destinatário do email"""
        from paperpaper.models import send_article_notifications
        
        NotificationSubscription.objects.create(
            full_name='John Doe',
            email='john@example.com',
            is_active=True
        )

        send_article_notifications(self.article)

        # Verificar destinatário
        call_args = mock_send_mail.call_args
        recipients = call_args[0][3]  # Quarto argumento (lista de emails)
        
        self.assertEqual(len(recipients), 1)
        self.assertIn('john@example.com', recipients)

    @patch('django.core.mail.send_mail')  # Changed
    def test_no_notification_for_inactive_subscriber(self, mock_send_mail):
        """Testa que notificação NÃO é enviada para assinante inativo"""
        from paperpaper.models import send_article_notifications
        
        # Criar assinatura inativa
        NotificationSubscription.objects.create(
            full_name='John Doe',
            email='john@example.com',
            is_active=False
        )

        send_article_notifications(self.article)

        # Verificar que send_mail NÃO foi chamado
        self.assertFalse(mock_send_mail.called)

    @patch('django.core.mail.send_mail')  # Changed
    def test_multiple_notifications_for_multiple_authors(self, mock_send_mail):
        """Testa envio de notificações para múltiplos autores"""
        from paperpaper.models import send_article_notifications
        
        # Adicionar segundo autor
        author2 = Author.objects.create(full_name='Jane Smith')
        self.article.authors.add(author2)

        # Criar assinaturas para ambos autores
        NotificationSubscription.objects.create(
            full_name='John Doe',
            email='john@example.com',
            is_active=True
        )
        NotificationSubscription.objects.create(
            full_name='Jane Smith',
            email='jane@example.com',
            is_active=True
        )

        send_article_notifications(self.article)

        # Verificar que send_mail foi chamado 2 vezes
        self.assertEqual(mock_send_mail.call_count, 2)

    @patch('django.core.mail.send_mail')  # Changed
    def test_notification_with_case_insensitive_matching(self, mock_send_mail):
        """Testa correspondência case-insensitive de nomes de autores"""
        from paperpaper.models import send_article_notifications
        
        # Criar assinatura com nome em caixa diferente
        NotificationSubscription.objects.create(
            full_name='JOHN DOE',  # Maiúsculas
            email='john@example.com',
            is_active=True
        )

        send_article_notifications(self.article)

        # Verificar que send_mail foi chamado (apesar da diferença de caixa)
        self.assertTrue(mock_send_mail.called)

    @patch('django.core.mail.send_mail', side_effect=Exception('SMTP Error'))  # Changed
    def test_notification_handles_email_error_gracefully(self, mock_send_mail):
        """Testa que erros de email são tratados sem quebrar o sistema"""
        from paperpaper.models import send_article_notifications
        
        NotificationSubscription.objects.create(
            full_name='John Doe',
            email='john@example.com',
            is_active=True
        )

        # Não deve lançar exceção
        try:
            send_article_notifications(self.article)
        except Exception:
            self.fail("send_article_notifications raised Exception unexpectedly!")

    @patch('django.core.mail.send_mail')
    def test_notification_includes_article_url(self, mock_send_mail):
        """Testa que a notificação inclui URL do artigo"""
        from paperpaper.models import send_article_notifications
        
        NotificationSubscription.objects.create(
            full_name='John Doe',
            email='john@example.com',
            is_active=True
        )

        send_article_notifications(self.article)

        # Verificar que a URL está no corpo do email
        call_args = mock_send_mail.call_args
        message = call_args[0][1]
        
        # Verify the message contains a link to view the article
        self.assertIn('Você pode visualizar o artigo em:', message)
        self.assertIn(f'/articles/{self.article.pk}/', message)

class ProcessBibtexEntryTests(TestCase):
    """Testes para a função process_bibtex_entry"""

    def setUp(self):
        """Configuração para cada teste"""
        self.valid_entry = {
            'ID': 'doe2024study',
            'title': 'A Study on Software Engineering',
            'author': 'John Doe and Jane Smith',
            'booktitle': 'ICSE 2024',
            'year': '2024',
            'location': 'Lisbon'
        }

        self.event = Event.objects.create(
            name='ICSE',
            acronym='ICSE',
            promoting_entity='IEEE'
        )

    def test_process_bibtex_entry_success(self):
        """Testa processamento bem-sucedido de entrada BibTeX"""
        result = process_bibtex_entry(self.valid_entry, {})

        self.assertTrue(result['success'])
        self.assertTrue(Article.objects.filter(bibtex_key='doe2024study').exists())

    def test_process_bibtex_entry_creates_article(self):
        """Testa criação de artigo a partir de entrada BibTeX"""
        result = process_bibtex_entry(self.valid_entry, {})

        article = Article.objects.get(bibtex_key='doe2024study')
        self.assertEqual(article.title, 'A Study on Software Engineering')

    def test_process_bibtex_entry_creates_authors(self):
        """Testa criação de autores a partir de entrada BibTeX"""
        result = process_bibtex_entry(self.valid_entry, {})

        article = Article.objects.get(bibtex_key='doe2024study')
        authors = list(article.authors.all())

        self.assertEqual(len(authors), 2)
        self.assertTrue(any(a.full_name == 'John Doe' for a in authors))
        self.assertTrue(any(a.full_name == 'Jane Smith' for a in authors))

    def test_process_bibtex_entry_missing_title(self):
        """Testa falha ao processar entrada sem título"""
        entry = self.valid_entry.copy()
        del entry['title']

        result = process_bibtex_entry(entry, {})

        self.assertFalse(result['success'])
        self.assertIn('Título', result['error'])

    def test_process_bibtex_entry_missing_author(self):
        """Testa falha ao processar entrada sem autor"""
        entry = self.valid_entry.copy()
        del entry['author']

        result = process_bibtex_entry(entry, {})

        self.assertFalse(result['success'])

    def test_process_bibtex_entry_invalid_year(self):
        """Testa falha ao processar entrada com ano inválido"""
        entry = self.valid_entry.copy()
        entry['year'] = 'abc'

        result = process_bibtex_entry(entry, {})

        self.assertFalse(result['success'])

    def test_process_bibtex_entry_year_out_of_range(self):
        """Testa falha ao processar entrada com ano fora do intervalo"""
        entry = self.valid_entry.copy()
        entry['year'] = '1800'

        result = process_bibtex_entry(entry, {})

        self.assertFalse(result['success'])
        self.assertIn('Ano inválido', result['error'])

    def test_process_bibtex_entry_with_existing_event(self):
        """Testa processamento com evento existente"""
        result = process_bibtex_entry(self.valid_entry, {})

        article = Article.objects.get(bibtex_key='doe2024study')
        self.assertEqual(article.edition.event, self.event)

    def test_process_bibtex_entry_creates_new_event(self):
        """Testa criação de novo evento se não existir"""
        entry = self.valid_entry.copy()
        entry['booktitle'] = 'Unknown Conference 2024'

        result = process_bibtex_entry(entry, {})

        self.assertTrue(result['success'])
        self.assertTrue(Event.objects.filter(name='Unknown Conference 2024').exists())


class EventCreateViewTests(TestCase):
    """Testes para a view event_create (deve retornar erro)"""

    def setUp(self):
        """Configuração para cada teste"""
        self.client = Client()

    def test_event_create_redirects(self):
        """Testa que a criação de evento retorna redirecionamento"""
        response = self.client.get(reverse('event_create'))
        self.assertEqual(response.status_code, 302)

    def test_event_create_redirects_to_events_list(self):
        """Testa redirecionamento para lista de eventos"""
        response = self.client.get(reverse('event_create'), follow=True)
        self.assertRedirects(response, reverse('events_list'))


class EventEditViewTests(TestCase):
    """Testes para a view event_edit (deve retornar erro)"""

    def setUp(self):
        """Configuração para cada teste"""
        self.client = Client()
        self.event = Event.objects.create(name='ICSE', acronym='ICSE', promoting_entity='IEEE')

    def test_event_edit_redirects(self):
        """Testa que a edição de evento retorna redirecionamento"""
        response = self.client.get(reverse('event_edit', kwargs={'slug': self.event.slug}))
        self.assertEqual(response.status_code, 302)


class EventDeleteViewTests(TestCase):
    """Testes para a view event_delete (deve retornar erro)"""

    def setUp(self):
        """Configuração para cada teste"""
        self.client = Client()
        self.event = Event.objects.create(name='ICSE', acronym='ICSE', promoting_entity='IEEE')

    def test_event_delete_redirects(self):
        """Testa que a deleção de evento retorna redirecionamento"""
        response = self.client.get(reverse('event_delete', kwargs={'slug': self.event.slug}))
        self.assertEqual(response.status_code, 302)


if __name__ == '__main__':
    unittest.main()
