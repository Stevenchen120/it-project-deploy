from django.shortcuts import render
from django.http import JsonResponse, Http404
from .models import HistoricalFigure
from .serializers import HistorySerializer

from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import mixins
from rest_framework import viewsets
from django_filters import rest_framework as filters
from django.db.models import Q
# Create your views here.
# @api_view(['GET','POST'])
# def history_list(request):
#     if request.method=='GET':
#         histories=HistoricalFigure.objects.all()
#         serializer= HistoryListSerializer(histories,many=True)
#         return Response(serializer.data,status=status.HTTP_200_OK)
#     elif request.method == "POST":
#         serializer = HistoryListSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class HistoryDetail(APIView):
#     def get(self, request, pk):
#         try:
#             history = HistoricalFigure.objects.get(pk=pk)
#         except:
#             raise Http404
#         serializer = HistoryDetailSerializer(history)
#         return Response(serializer.data)

# class HistoryList(generics.ListCreateAPIView):
#     queryset=HistoricalFigure.objects.all()
#     serializer_class = HistoryListSerializer

# class HistoryDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset=HistoricalFigure.objects.all()
#     serializer_class = HistoryDetailSerializer


class HistoricalFilter(filters.FilterSet):
    search = filters.CharFilter(method='multi_field_search')
    category = filters.CharFilter(method='filter_by_category')
    birth_year = filters.CharFilter(method='filter_by_birth_year')
    death_year = filters.CharFilter(method='filter_by_death_year')
    occupation = filters.CharFilter(method='filter_by_occupation')

    class Meta:
        model = HistoricalFigure
        fields = ['id', 'given_names', 'family_name',
                  'birth_year', 'death_year', 'short_description']

    def multi_field_search(self, queryset, name, value):

        filter_param = self.data.get('filter')
        # Check which filter is applied and modify the queryset accordingly
        if filter_param == 'birth':
            return queryset.filter(birth_year__icontains=value)
        elif filter_param == 'death':
            return queryset.filter(death_year__icontains=value)
        elif filter_param == 'family':
            return queryset.filter(family_name__icontains=value)
        elif filter_param == 'givenName':
            return queryset.filter(given_names__icontains=value)
        elif filter_param == 'occupation':
            return queryset.filter(short_description__icontains=value)
        else:
            # Default behavior (general search across multiple fields)
            return queryset.filter(
                Q(given_names__icontains=value) |
                Q(family_name__icontains=value) |
                Q(birth_year__icontains=value) |
                Q(death_year__icontains=value) |
                Q(short_description__icontains=value)
            )

    def filter_by_category(self, queryset, name, value):
        letter = self.request.GET.get('category')
        if letter:
            return queryset.filter(Q(given_names__istartswith=letter) | Q(family_name__istartswith=letter))

    def filter_by_birth_year(self, queryset, name, value):
        birth_year = self.request.GET.get('birth_year')
        if birth_year:
            birth_year_range = birth_year.split('-')
            if len(birth_year_range) == 2:
                start_year = birth_year_range[0]
                end_year = birth_year_range[1]
                queryset = queryset.filter(
                    birth_year__gte=start_year, birth_year__lte=end_year)
        return queryset

    def filter_by_death_year(self, queryset, name, value):
        death_year = self.request.GET.get('death_year')
        if death_year:
            death_year_range = death_year.split('-')
            if len(death_year_range) == 2:
                start_year = death_year_range[0]
                end_year = death_year_range[1]
                queryset = queryset.filter(
                    death_year__gte=start_year, death_year__lte=end_year)
        return queryset

    def filter_by_occupation(self, queryset, name, value):
        occupation = self.request.GET.get('occupation')
        if occupation:
            return queryset.filter(short_description__icontains=occupation)


class HistoryViewSet(viewsets.ModelViewSet):
    queryset = HistoricalFigure.objects.all()
    serializer_class = HistorySerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = HistoricalFilter
