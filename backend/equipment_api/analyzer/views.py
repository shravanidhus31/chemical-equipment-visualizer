from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Dataset
from .utils.csv_analyzer import analyze_csv

@api_view(['POST'])
def upload_csv(request):
    if 'file' not in request.FILES:
        return Response({"error": "No file uploaded"}, status=status.HTTP_400_BAD_REQUEST)

    file = request.FILES['file']

    summary = analyze_csv(file)

    dataset = Dataset.objects.create(
        filename=file.name,
        summary=summary
    )

    # keep only last 5 uploads
    if Dataset.objects.count() > 5:
        Dataset.objects.order_by('uploaded_at').first().delete()

    return Response({
        "message": "File uploaded successfully",
        "dataset_id": dataset.id,
        "summary": summary
    })
