from rest_framework.pagination import PageNumberPagination


class ChatBotPaginator(PageNumberPagination):
    """
    This is the paginator class that allows pagination for any query.
    This pagination is performed to ensure the query are optimized for large amount of data
    So that neither the backend nor the frontend face any performance issues.
    """
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 100000
