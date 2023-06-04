from rest_framework.views import Response
from rest_framework.views import APIView
from django.core.mail import send_mail


from backend import settings
from .serializers import SupportMessageSerializer
from .models import SupportMessage

class AskSupportView(APIView):
    def post(self, request):
        serializer = SupportMessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.validated_data)
        return Response({'error': "Can't add message"}, status=400)

class AnswerSupportView(APIView):
    def get(self, request):
        messages = SupportMessage.objects.all()
        serializer = SupportMessageSerializer(instance=messages, many=True)
        return Response(serializer.data)
    
    def delete(self, request, id):
        message = SupportMessage.objects.filter(id=id)
        message.delete()
        return Response({'id': id})
    
    def post(self, request, id):
        message = SupportMessage.objects.filter(id=id).first()
        content = request.data['content']
        subject = f'Replay to "{message.title}"'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = (message.email,)
        send_mail( subject, content, email_from, recipient_list )
        message.delete()
        return Response({'id': id})


