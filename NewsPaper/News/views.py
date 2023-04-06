from django.shortcuts import render
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView, TemplateView
from django.core.paginator import Paginator
from .filters import ArticleFilter
from .models import Article
from .forms import ArticleForm
from django.contrib.auth.mixins import PermissionRequiredMixin
from .utils import send_email
from django.shortcuts import redirect


class ArticleList(ListView):
    model = Article
    template_name = 'News/news.html'
    context_object_name = 'article'
    ordering = ['-id']
    paginate_by = 1


class ArticleSearch(ListView):
    model = Article
    template_name = 'News/search.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = ArticleFilter(self.request.GET, queryset=self.get_queryset())
        return context


class ArticleDetail(DetailView):
    template_name = 'News/newsdetail.html'
    queryset = Article.objects.all()
   

class AddArticle(CreateView, PermissionRequiredMixin):
    template_name = 'News/addnews.html'
    form_class = ArticleForm
    permission_required = 'News.add_article'

    def create_article(request):
        if request.method == 'POST':
            form = ArticleForm(request.POST)
            if form.is_valid():
                article = form.save(commit=False)
                article.save()
                article.send_notification_email()
                return redirect(article.get_absolute_url())
        else:
            form = ArticleForm()
        return render(request, 'email/create_article.html', {'form': form})
    
    
class ArticleUpdateView(UpdateView, PermissionRequiredMixin):
    template_name = 'News/article_update.html'
    form_class = ArticleForm
    permission_required = 'News.change_article'
 
    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Article.objects.get(pk=id)
 

class ArticleDeleteView(DeleteView):
    template_name = 'News/article_delete.html'
    queryset = Article.objects.all()
    success_url = '/news/'
