from django.urls import path
from .views import ArticleList, ArticleDetail, ArticleSearch, AddArticle, ArticleUpdateView, ArticleDeleteView


urlpatterns = [
    path('', ArticleList.as_view()),
    path('<int:pk>', ArticleDetail.as_view(), name='article_detail'),
    path('search/', ArticleSearch.as_view()),
    path('add/', AddArticle.as_view(), name='article_add'),
    path('<int:pk>/article_update/', ArticleUpdateView.as_view(), name='article_update'),
    path('<int:pk>/article_delete/', ArticleDeleteView.as_view(), name='article_delete'),
]