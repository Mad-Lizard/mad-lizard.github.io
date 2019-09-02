from recovery.models import Post, Athlet, Article
from django.views import generic
from itertools import chain

class SearchResultsView(generic.ListView):
    model = Post, Article, Athlet
    template_name = 'web_recovery/search_results.html'

    class Meta:
        app_label = 'web_recovery'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['count'] = self.count or 0
        context['query'] = self.request.GET.get('q')
        return context

    def get_queryset(self):
        request = self.request
        query = request.GET.get('q', None)

        if query is not None:
            post_results = Post.objects.search(query)
            article_results = Article.objects.search(query)
            athlet_results = Athlet.objects.search(query)

            # combine querysets
            queryset_chain = chain(
                    post_results,
                    article_results,
                    athlet_results
            )
            qs = sorted(queryset_chain,
                        key=lambda instance: instance.pk,
                        reverse=True)
            self.count = len(qs) # since qs is actually a list
            return qs
        return Post.objects.none()
