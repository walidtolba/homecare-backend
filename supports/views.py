from rest_framework.views import Response
from rest_framework.views import APIView
from .serializers import CreateSupportMessageSerializer

class SupportMessageView(APIView):
    def post(self, request):
        print('got it')
        serializer = CreateSupportMessageSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.validated_data)