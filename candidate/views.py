import os,requests
from bs4 import BeautifulSoup
from openpyxl import load_workbook
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

            wb = load_workbook(file_path)

            ws = wb.active
            

            for row in ws.iter_rows(min_col=2,min_row=2):
                email=CandidateModel.objects.filter(email=row[3].value).first()
                hyperlink = row[5].hyperlink


                if email:
                    continue
                else:
                    if hyperlink is not None:
                        response = requests.get(hyperlink.target)
                        online_resume = BeautifulSoup(response.text, 'html.parser')
                        download_link = online_resume.find('a', {'class': 'btn btn-default'})['href']

                        print(download_link)
                        candidate = CandidateModel(
                                name=row[1].value,
                                job=row[0].value,
                                phone_number=row[2].value,
                                email=row[3].value,
                                request_date=row[4].value,
                                link=hyperlink.target
                            )
                        candidate.save()
                        
            
            os.remove(file_path)
            return Response({"message": "Data uploaded successfully"})

            
        else:
            return Response({'message': 'No file uploaded'})


class CandidateListAPIView(generics.ListAPIView):
    queryset=CandidateModel.objects.all()
    serializer_class=CandidateSerializer
    filter_backends = [filters.SearchFilter,filters.OrderingFilter]
    search_fields = ['job']
    ordering_fields = ['request_date']
    permission_classes=[IsSuperuserOrHR]