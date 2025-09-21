from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class MessagePagination(PageNumberPagination):
    page_size = 20  # 20 messages per page
    page_size_query_param = "page_size"  # optional: client can override
    max_page_size = 100

    # Include total count in response (ensures page.paginator.count)
    def get_paginated_response(self, data):
        return Response({
            "count": self.page.paginator.count,  # total messages
            "next": self.get_next_link(),
            "previous": self.get_previous_link(),
            "results": data,
        })
