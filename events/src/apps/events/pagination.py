from rest_framework.pagination import PageNumberPagination


class EventPagination(PageNumberPagination):
    page_size = 10
    page_query_param = "page_items"
    max_page_size = 50
