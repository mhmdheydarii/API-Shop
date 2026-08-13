from rest_framework.pagination import PageNumberPagination

class AdminOrdersPagination(PageNumberPagination):
    page_query_param = "page"
    page_size = 1
    max_page_size = 100