from rest_framework.pagination import PageNumberPagination, CursorPagination
from rest_framework.response import Response

class PatientSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000


class LinkHeaderPagination(CursorPagination):    
    def paginate_queryset(self, queryset, request, view=None):
        try:
            self.count = queryset.count()
        except (AttributeError, TypeError):
            self.count = len(queryset)
        return super().paginate_queryset(queryset, request, view=None)
    
    def get_paginated_response(self, data):
        next_url = self.get_next_link()
        previous_url = self.get_previous_link()
        headers = {}
        if next_url is not None:
            headers['XNextLink'] = next_url
        if previous_url is not None:
            headers['XPrevLink'] = previous_url
        if self.count is not None:
            headers['XTotal-Count'] = self.count

        return Response(data, headers=headers)