from rest_framework.views import APIView
from rest_framework.response import Response
from ..proofreader import proofread_text


class ProofreadAPIView(APIView):
    def get(self, request, *args, **kwargs):
        lang = kwargs.get('lang', 'akl')
        text = request.GET.get("text")

        if text:
            data = proofread_text(text, lang=lang, max_suggestions=3)
            return Response(data)
        else:
            return Response({"error": "Text parameter is required."}, status=400)