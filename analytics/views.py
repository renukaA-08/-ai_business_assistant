from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie


# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from analytics.serializers import ChatQuestionSerializer
from analytics.services.chatbot_service import process_question


@api_view(["POST"])
def chat_api(request):
    serializer = ChatQuestionSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    question = serializer.validated_data["question"]

    try:
        result = process_question(question)
        return Response(result, status=status.HTTP_200_OK)

    except Exception:
        return Response(
            {
                "error": "Unable to process your question right now."
            },
            status=status.HTTP_503_SERVICE_UNAVAILABLE
        )



@ensure_csrf_cookie
def chat_page(request):
    return render(request, "analytics/chat.html")