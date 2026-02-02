from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import Dataset
from .serializers import DatasetSerializer
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

    if Dataset.objects.count() > 5:
        Dataset.objects.order_by('uploaded_at').first().delete()

    return Response({
        "message": "File uploaded successfully",
        "dataset_id": dataset.id,
        "summary": summary
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_summary(request, dataset_id):
    dataset = get_object_or_404(Dataset, id=dataset_id)
    return Response(dataset.summary)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_history(request):
    datasets = Dataset.objects.order_by('-uploaded_at')[:5]
    serializer = DatasetSerializer(datasets, many=True)
    return Response(serializer.data)
