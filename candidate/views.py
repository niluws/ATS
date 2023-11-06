import os
from openpyxl import load_workbook
from rest_framework import generics
from rest_framework.response import Response
from .serializers import ExcelFileSerializer
from .models import ExceFileModel,CandidateModel
class Upload_Resume(generics.CreateAPIView):
    serializer_class=ExcelFileSerializer

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

                if email:
                    continue
                else:
                    candidate = CandidateModel(
                            name=row[1].value,
                            job=row[0].value,
                            phone_number=row[2].value,
                            email=row[3].value,
                            request_date=row[4].value,
                            link=str(row[5].hyperlink.target)
                        )
                
                    candidate.save()
                    os.remove(file_path)
                    
                    return Response({"message": "Data uploaded successfully"})
            os.remove(file_path)
            return Response({"message": "Data already exist"})
            
        else:
            return Response({'message': 'No file uploaded'})