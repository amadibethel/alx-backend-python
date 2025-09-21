from rest_framework.pagination import PageNumberPagination

class MessagePagination(PageNumberPagination):
    page_size = 20  # 20 messages per page
    page_size_query_param = "page_size"  # optional: allow client to override page size
    max_page_size = 100
