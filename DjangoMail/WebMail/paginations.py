from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class MyFormatResultsSetPagination(PageNumberPagination):
    '''
    分页器：继承PageNumberPagination，使用相关属性并重写函数。
    '''
    page_size_query_param = "pageSize"
    page_query_param = 'pageIndex'
    page_size = 5
    max_page_size = 10

    """
    自定义分页方法
    """
    def get_paginated_response(self, data):
        """
        设置返回内容格式
        """
        return Response({
            'data': data,
            'pagination': self.page.paginator.count,
            'pageSize': self.page.paginator.per_page,
            'pageIndex': self.page.start_index() // self.page.paginator.per_page + 1
        })
