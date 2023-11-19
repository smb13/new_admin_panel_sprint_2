from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Q
from django.http import JsonResponse
from django.views.generic.detail import BaseDetailView
from django.views.generic.list import BaseListView

from movies.models import Filmwork, FilmworkPerson


class MoviesApiMixin:
    model = Filmwork
    http_method_names = ['get']
    queryset = Filmwork.objects.all().prefetch_related('genres', 'person')

    def get_queryset(self):
        genres = ArrayAgg('genres__name', distinct=True)
        actors = ArrayAgg('persons__full_name', distinct=True,
                          filter=Q(filmworkperson__role=FilmworkPerson.Role.ACTOR))
        directors = ArrayAgg('persons__full_name', distinct=True,
                             filter=Q(filmworkperson__role=FilmworkPerson.Role.DIRECTOR))
        writers = ArrayAgg('persons__full_name', distinct=True,
                           filter=Q(filmworkperson__role=FilmworkPerson.Role.WRITER))
        return (self.queryset.values('id', 'title', 'description', 'creation_date', 'rating', 'type').
                annotate(genres=genres, actors=actors, directors=directors, writers=writers))

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(context)


class MoviesListApi(MoviesApiMixin, BaseListView):
    paginate_by = 50

    def get_context_data(self, *, object_list=None, **kwargs):
        queryset = self.get_queryset()
        title = self.request.GET.get('title', None)
        genres = self.request.GET.get('genres', None)
        if title is not None:
            queryset = self.get_queryset().filter(title__icontains=title)
        if genres is not None:
            queryset = self.get_queryset().filter(genres__icontains=genres)
        self.paginate_by = self.request.GET.get('paginate_by', self.paginate_by)
        paginator, page, queryset, is_paginated = self.paginate_queryset(
            queryset,
            self.paginate_by
        )
        return {'count': paginator.count,
                'total_pages': paginator.num_pages,
                'prev': page.number - 1 if page.number > 1 else None,
                'next': page.number + 1 if page.number < paginator.num_pages else None,
                'results': list(queryset),
                }


class MoviesDetailApi(MoviesApiMixin, BaseDetailView):

    def get_context_data(self, **kwargs):
        queryset = self.get_queryset().get(id=self.kwargs['pk'])
        return queryset
