from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.db.models import Q, Count
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import zipfile
import bibtexparser
import tempfile
import os
from .models import Event, Edition, Article, Author, NotificationSubscription, BibtexImport


def home(request):
    """Página inicial com estatísticas gerais"""
    context = {
        'events_count': Event.objects.count(),
        'articles_count': Article.objects.count(),
        'authors_count': Author.objects.count(),
        'recent_articles': Article.objects.select_related('edition__event').prefetch_related('authors')[:5]
    }
    return render(request, 'paperpaper/home.html', context)


def events_list(request):
    """Lista todos os eventos disponíveis"""
    events = Event.objects.all().prefetch_related('editions').order_by('name')
    context = {
        'events': events
    }
    return render(request, 'paperpaper/events_list.html', context)


def authors_list(request):
    """Lista todos os autores disponíveis"""
    authors = Author.objects.all().annotate(
        articles_count=Count('articles')
    ).order_by('full_name')
    
    # Paginação opcional
    paginator = Paginator(authors, 50)  # 50 autores por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'authors': page_obj,
        'is_paginated': paginator.num_pages > 1
    }
    return render(request, 'paperpaper/authors_list.html', context)


def search_articles(request):
    """Sistema de busca por artigos"""
    query = request.GET.get('q', '')
    search_type = request.GET.get('type', 'title')  # title, author, event
    
    results = []
    if query:
        if search_type == 'title':
            results = Article.objects.filter(
                title__icontains=query
            ).select_related('edition__event').prefetch_related('authors')
        elif search_type == 'author':
            results = Article.objects.filter(
                authors__full_name__icontains=query
            ).select_related('edition__event').prefetch_related('authors').distinct()
        elif search_type == 'event':
            results = Article.objects.filter(
                edition__event__name__icontains=query
            ).select_related('edition__event').prefetch_related('authors')
    
    context = {
        'query': query,
        'search_type': search_type,
        'results': results,
        'results_count': len(results)
    }
    return render(request, 'paperpaper/search.html', context)


def event_detail(request, slug):
    """Página do evento mostrando suas edições"""
    event = get_object_or_404(Event, slug=slug)
    editions = event.editions.all().order_by('-year')
    
    context = {
        'event': event,
        'editions': editions
    }
    return render(request, 'paperpaper/event_detail.html', context)


def edition_detail(request, slug, year):
    """Página da edição mostrando seus artigos"""
    event = get_object_or_404(Event, slug=slug)
    edition = get_object_or_404(Edition, event=event, year=year)
    articles = edition.articles.all().prefetch_related('authors').order_by('title')
    
    context = {
        'event': event,
        'edition': edition,
        'articles': articles
    }
    return render(request, 'paperpaper/edition_detail.html', context)


def author_detail(request, slug):
    """Página do autor mostrando seus artigos organizados por ano"""
    author = get_object_or_404(Author, slug=slug)
    
    # Artigos organizados por ano
    articles_by_year = {}
    articles = author.articles.select_related('edition__event').order_by('-edition__year', 'title')
    
    for article in articles:
        year = article.edition.year
        if year not in articles_by_year:
            articles_by_year[year] = []
        articles_by_year[year].append(article)
    
    context = {
        'author': author,
        'articles_by_year': articles_by_year,
        'total_articles': articles.count()
    }
    return render(request, 'paperpaper/author_detail.html', context)


def notification_subscribe(request):
    """Página para cadastro de notificações"""
    if request.method == 'POST':
        full_name = request.POST.get('full_name', '').strip()
        email = request.POST.get('email', '').strip()
        
        if full_name and email:
            subscription, created = NotificationSubscription.objects.get_or_create(
                full_name=full_name,
                email=email,
                defaults={'is_active': True}
            )
            
            if created:
                messages.success(request, 'Inscrição realizada com sucesso!')
            else:
                if not subscription.is_active:
                    subscription.is_active = True
                    subscription.save()
                    messages.success(request, 'Sua inscrição foi reativada!')
                else:
                    messages.info(request, 'Você já está inscrito para receber notificações.')
        else:
            messages.error(request, 'Por favor, preencha todos os campos.')
    
    return render(request, 'paperpaper/notification_subscribe.html')


@staff_member_required
def bibtex_import(request):
    """Interface para importação de artigos via BibTeX"""
    if request.method == 'POST':
        return handle_bibtex_upload(request)
    
    return render(request, 'paperpaper/bibtex_import.html')


@staff_member_required
def handle_bibtex_upload(request):
    """Processa upload de arquivo BibTeX e ZIP com PDFs"""
    bibtex_file = request.FILES.get('bibtex_file')
    zip_file = request.FILES.get('zip_file')
    
    if not bibtex_file:
        messages.error(request, 'Arquivo BibTeX é obrigatório.')
        return redirect('bibtex_import')
    
    # Criar registro de importação
    import_record = BibtexImport.objects.create(
        uploaded_by=request.user,
        bibtex_file=bibtex_file,
        zip_file=zip_file
    )
    
    try:
        # Processar BibTeX
        bibtex_content = bibtex_file.read().decode('utf-8')
        bib_database = bibtexparser.loads(bibtex_content)
        
        import_record.total_entries = len(bib_database.entries)
        
        # Extrair PDFs do ZIP se fornecido
        pdf_files = {}
        if zip_file:
            with zipfile.ZipFile(zip_file, 'r') as zip_ref:
                for file_info in zip_ref.filelist:
                    if file_info.filename.endswith('.pdf'):
                        pdf_name = os.path.splitext(file_info.filename)[0]
                        pdf_files[pdf_name] = zip_ref.read(file_info.filename)
        
        log_messages = []
        successful_imports = 0
        failed_imports = 0
        
        for entry in bib_database.entries:
            try:
                result = process_bibtex_entry(entry, pdf_files)
                if result['success']:
                    successful_imports += 1
                    log_messages.append(f"✓ {entry.get('title', 'Sem título')}")
                else:
                    failed_imports += 1
                    log_messages.append(f"✗ {entry.get('title', 'Sem título')}: {result['error']}")
            except Exception as e:
                failed_imports += 1
                log_messages.append(f"✗ {entry.get('title', 'Sem título')}: {str(e)}")
        
        # Atualizar registro de importação
        import_record.successful_imports = successful_imports
        import_record.failed_imports = failed_imports
        import_record.import_log = '\n'.join(log_messages)
        import_record.save()
        
        messages.success(
            request, 
            f'Importação concluída: {successful_imports} sucessos, {failed_imports} falhas.'
        )
        
    except Exception as e:
        messages.error(request, f'Erro ao processar arquivo: {str(e)}')
    
    return redirect('bibtex_import')


def process_bibtex_entry(entry, pdf_files):
    """Processa uma entrada individual do BibTeX"""
    try:
        # Validar campos obrigatórios
        required_fields = ['title', 'author', 'booktitle', 'year']
        for field in required_fields:
            if field not in entry or not entry[field].strip():
                return {'success': False, 'error': f'Campo obrigatório ausente: {field}'}
        
        # Encontrar ou criar evento baseado no booktitle
        booktitle = entry['booktitle']
        event = None
        
        # Tentar encontrar evento existente baseado no booktitle
        for existing_event in Event.objects.all():
            if existing_event.name.lower() in booktitle.lower() or existing_event.acronym.lower() in booktitle.lower():
                event = existing_event
                break
        
        if not event:
            # Criar evento genérico se não encontrado
            event = Event.objects.create(
                name=booktitle,
                acronym=booktitle[:10],
                promoting_entity="Importado via BibTeX"
            )
        
        # Encontrar ou criar edição
        year = int(entry['year'])
        location = entry.get('location', 'Local não informado')
        edition, _ = Edition.objects.get_or_create(
            event=event,
            year=year,
            defaults={'location': location}
        )
        
        # Processar autores
        authors_names = [name.strip() for name in entry['author'].replace(' and ', ',').split(',')]
        authors = []
        for author_name in authors_names:
            if author_name:
                author, _ = Author.objects.get_or_create(full_name=author_name)
                authors.append(author)
        
        # Criar artigo
        article = Article.objects.create(
            title=entry['title'],
            edition=edition,
            start_page=entry.get('pages', '').split('--')[0] if entry.get('pages') else None,
            end_page=entry.get('pages', '').split('--')[1] if '--' in entry.get('pages', '') else None,
            bibtex_key=entry.get('ID', '')
        )
        
        # Adicionar autores ao artigo
        article.authors.set(authors)
        
        # Adicionar PDF se disponível
        bibtex_key = entry.get('ID', '')
        if bibtex_key in pdf_files:
            # Salvar PDF
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
                temp_file.write(pdf_files[bibtex_key])
                temp_file_path = temp_file.name
            
            with open(temp_file_path, 'rb') as pdf_file:
                article.pdf_file.save(
                    f"{bibtex_key}.pdf",
                    pdf_file,
                    save=True
                )
            
            os.unlink(temp_file_path)
        
        # Enviar notificações
        send_notifications_for_article(article)
        
        return {'success': True}
        
    except Exception as e:
        return {'success': False, 'error': str(e)}


def send_notifications_for_article(article):
    """Envia notificações por email para autores cadastrados"""
    for author in article.authors.all():
        # Buscar inscrições ativas para este autor
        subscriptions = NotificationSubscription.objects.filter(
            full_name__iexact=author.full_name,
            is_active=True
        )
        
        for subscription in subscriptions:
            try:
                subject = f'Novo artigo disponível: {article.title}'
                message = f"""
Olá {subscription.full_name},

Um novo artigo seu foi adicionado ao sistema PaperPaper:

Título: {article.title}
Evento: {article.edition.event.name}
Ano: {article.edition.year}
Autores: {article.authors_string}

Você pode visualizar o artigo em: {article.get_absolute_url()}

Atenciosamente,
Equipe PaperPaper
                """
                
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [subscription.email],
                    fail_silently=True
                )
            except Exception:
                pass  # Falhas de email não devem interromper o processo
