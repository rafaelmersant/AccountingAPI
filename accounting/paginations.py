from rest_framework.pagination import PageNumberPagination


class EntryListPagination(PageNumberPagination):
    def get_page_size(self, request):
        start_date = request.query_params.get('start_date', None)
        church = request.query_params.get('church', None)
        person = request.query_params.get('person', None)
        dashboard = request.query_params.get('dashboard', None)

        if church is not None or person is not None or \
            start_date is not None or dashboard is not None:
            return 9000000
        else:
            return 20


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 10


class StandardResultsSetPaginationAdmin(PageNumberPagination):
    page_size = 15
    page_size_query_param = 'page_size'
    max_page_size = 15


class StandardResultsSetPaginationMedium(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 20


class StandardResultsSetPaginationHigh(PageNumberPagination):
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 50


class StandardResultsSetPaginationLevelHighest(PageNumberPagination):
    page_size = 200
    page_size_query_param = 'page_size'
    max_page_size = 200



