import markdown2
from django.shortcuts import redirect, render

from . import util
from .forms import EditEntryForm, NewEntryForm


def index(request):
    return render(request, 'encyclopedia/index.html', {
        'entries': util.list_entries()
    })


def entry(request, title):
    content = util.get_entry(title)
    if content is None:
        return render(request, 'encyclopedia/error.html', {
            'title': 'Page Not Found',
            'message': f'The requested entry "{title}" was not found.'
        }, status=404)

    html_content = markdown2.markdown(content)
    return render(request, 'encyclopedia/entry.html', {
        'title': title,
        'content': html_content,
    })


def search(request):
    query = request.GET.get('q', '').strip()
    entries = util.list_entries()

    if not query:
        return render(request, 'encyclopedia/search.html', {
            'query': query,
            'results': [],
        })

    for item in entries:
        if item.lower() == query.lower():
            return redirect('encyclopedia:entry', title=item)

    results = [item for item in entries if query.lower() in item.lower()]
    return render(request, 'encyclopedia/search.html', {
        'query': query,
        'results': results,
    })


def new_page(request):
    if request.method == 'POST':
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title'].strip()
            content = form.cleaned_data['content']

            if any(existing.lower() == title.lower() for existing in util.list_entries()):
                return render(request, 'encyclopedia/new.html', {
                    'form': form,
                    'error': 'An entry with this title already exists.'
                })

            util.save_entry(title, content)
            return redirect('encyclopedia:entry', title=title)
    else:
        form = NewEntryForm()

    return render(request, 'encyclopedia/new.html', {
        'form': form
    })


def edit_page(request, title):
    existing_content = util.get_entry(title)
    if existing_content is None:
        return render(request, 'encyclopedia/error.html', {
            'title': 'Page Not Found',
            'message': f'Cannot edit "{title}" because it does not exist.'
        }, status=404)

    if request.method == 'POST':
        form = EditEntryForm(request.POST)
        if form.is_valid():
            util.save_entry(title, form.cleaned_data['content'])
            return redirect('encyclopedia:entry', title=title)
    else:
        form = EditEntryForm(initial={'content': existing_content})

    return render(request, 'encyclopedia/edit.html', {
        'title': title,
        'form': form,
    })


def random_page(request):
    title = util.get_random_entry()
    if title is None:
        return render(request, 'encyclopedia/error.html', {
            'title': 'No Entries',
            'message': 'There are no entries available yet.'
        }, status=404)
    return redirect('encyclopedia:entry', title=title)


# to catch all Routes when DEBUG=False
def route_not_found(request):
    return render(request, "encyclopedia/error.html", {
        "title": "Page Not Found",
        "message": "The page you requested does not exist."
    }, status=404)


# Django handler 404
def custom_404(request, exception):
    return render(request, "encyclopedia/error.html", {
        "title": "Page Not Found",
        "message": "The page you requested does not exist."
    }, status=404)