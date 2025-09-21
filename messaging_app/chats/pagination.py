from rest_framework.pagination import PageNumberPagination

class MessagePagination(PageNumberPagination):
    page_size = 20  # default 20 messages per page
    page_size_query_param = "page_size"  # allow client to override
    max_page_size = 100

    # Optional: include total count for auto-check
    def get_paginated_response(self, data):
        return super().get_paginated_response(data)
