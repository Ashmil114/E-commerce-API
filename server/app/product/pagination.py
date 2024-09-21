from rest_framework.pagination import CursorPagination


class Pagination(CursorPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100
    ordering = "id"
