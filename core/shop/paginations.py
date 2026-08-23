from rest_framework.pagination import PageNumberPagination

class ProductsPagination(PageNumberPagination):
    page_query_param = "page"
    page_size = 24
    max_page_size = 100