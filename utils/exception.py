# 自定义异常处理
from rest_framework.views import exception_handler
from rest_framework.views import Response
from rest_framework import status


# 将仅针对由引发的异常生成的响应调用异常处理程序。它不会用于视图直接返回的任何响应
def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is None:
        print('1234 = %s - %s - %s - %s' % (context['view'], context["request"].data, context['request'].method, exc))
        return Response({
            'message': '服务器错误'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR, exception=True)
    else:
        message = "success"
        # 这个循环是取第一个错误的提示用于渲染
        for index, value in enumerate(response.data):
            if index == 0:
                key = value
                value = response.data[key]
                if isinstance(value, str):
                    message = value
                else:
                    message = key + value[0]
        return Response({
            'message': message,
        }, status=response.status_code, exception=True)
