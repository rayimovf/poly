from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status
from utils.render_response import render_data

class CustomPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response(
            render_data(data={
                "links": {
                    "next": self.get_next_link(),
                    "previous": self.get_previous_link(),
                },
                "count": self.page.paginator.count,
                "total_size": self.page.paginator.num_pages,
                "current_page": self.page.number,
                "results": data
            },
                success='true'
            ),
            status=status.HTTP_200_OK,
        )