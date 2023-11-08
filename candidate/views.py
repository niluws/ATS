import os,requests,uuid
from bs4 import BeautifulSoup
from openpyxl import load_workbook
from django.core.files.base import ContentFile
from rest_framework import generics,filters
from rest_framework.response import Response
from .serializers import ExcelFileSerializer,CandidateSerializer
from .models import ExceFileModel,CandidateModel
from authentication.permissions import IsSuperuserOrHR


    
class UploadExcelAPIView(generics.CreateAPIView):
    serializer_class=ExcelFileSerializer
    permission_classes=[IsSuperuserOrHR]

    def post(self, request, *args, **kwargs):
        uploaded_file = request.FILES.get('file')
        
        if uploaded_file:
            excel_file = ExceFileModel(file=uploaded_file)
            excel_file.save()
            file_path = excel_file.file.path

            workbook = load_workbook(file_path)

            worksheet = workbook.active
            new_user_count=0

            for row in worksheet.iter_rows(min_col=2,min_row=2):
                user=CandidateModel.objects.filter(email=row[3].value).first()
                hyperlink = row[5].hyperlink

                if user:
                    continue
                else:
                    if hyperlink is not None:
                        new_user_count += 1
                        response = requests.get(hyperlink.target)
                        online_resume = BeautifulSoup(response.text, 'html.parser')
                        url = online_resume.find('a', {'class': 'btn btn-default'})['href']

                        response = requests.get(url)
                        
                        candidate = CandidateModel(
                                name=row[1].value,
                                job=row[0].value,
                                phone_number=row[2].value,
                                email=row[3].value,
                                request_date=row[4].value,
                                resume= ContentFile(response.content, name=f"{uuid.uuid4()}.pdf"),
                            )
                        candidate.save()

                    
            os.remove(file_path)
            return Response({"message": f"Data uploaded successfully. {new_user_count} new users."})

            
        else:
            return Response({'message': 'No file uploaded'})


class CandidateListAPIView(generics.ListAPIView):
    queryset=CandidateModel.objects.all()
    serializer_class=CandidateSerializer
    filter_backends = [filters.SearchFilter,filters.OrderingFilter]
    search_fields = ['job']
    ordering_fields = ['request_date']
    permission_classes=[IsSuperuserOrHR]