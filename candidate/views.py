import os,requests,uuid,re
from bs4 import BeautifulSoup
# from PyPDF2 import PdfFileReader
from openpyxl import load_workbook
from django.core.files.base import ContentFile
from rest_framework import generics,filters
from rest_framework.response import Response
from authentication.permissions import IsSuperuserOrHR
from .serializers import ExcelFileSerializer,CandidateSerializer
from .models import ExcelFileModel,CandidateModel


class UploadExcelAPIView(generics.CreateAPIView):
    serializer_class = ExcelFileSerializer
    permission_classes=[IsSuperuserOrHR]

    def post(self, request, *args, **kwargs):
        uploaded_file = request.FILES.get('file')

        if not uploaded_file:
            return Response({'success': False, 'status': 400, 'error': 'No file uploaded'})

        excel_file = ExcelFileModel(file=uploaded_file)
        excel_file.save()
        file_path = excel_file.file.path

        try:
            workbook = load_workbook(file_path)
            worksheet = workbook.active

            user_emails = set()

            for row in worksheet.iter_rows(min_col=2, min_row=2):
                user_email = row[3].value

                if user_email not in user_emails:
                    user_emails.add(user_email)
                    existing_candidate = CandidateModel.objects.filter(email=user_email).exists()

                    if not existing_candidate:
                        hyperlink = row[5].hyperlink

                        if hyperlink is not None:
                            try:
                                response = requests.get(hyperlink.target)
                                soup = BeautifulSoup(response.text, 'html.parser')
                                url = soup.find(lambda tag: tag.name == 'a' and 'دانلود' in tag.get_text(strip=True))['href']
                                resume_response = requests.get(url)
                            
                                new_candidate = CandidateModel(
                                    name=row[1].value,
                                    job=row[0].value,
                                    phone_number=row[2].value,
                                    email=user_email,
                                    request_date=row[4].value,
                                    resume=ContentFile(resume_response.content, name=f"{row[0].value}/{row[1].value + row[2].value}.pdf"),
                                    job_status=soup.find('label', text=re.compile('وضعیت اشتغال')).find_next_sibling('span').get_text(strip=True),
                                    last_company=re.sub(r'\s+', ' ', soup.find('label', text=re.compile('آخرین')).find_next_sibling('span').get_text(strip=True).strip()),                                    education_level=soup.find('label', text=re.compile('تحصیلی')).find_next_sibling('span').get_text(strip=True),
                                    province=soup.find('label', text=re.compile('استان')).find_next_sibling('span').get_text(strip=True),
                                    location=soup.find('label', text=re.compile('آدرس محل')).find_next_sibling('span').get_text(strip=True),
                                    marital=soup.find('label', text=re.compile('تاهل')).find_next_sibling('span').get_text(strip=True),
                                    birthdate=soup.find('label', text=re.compile('سال تولد')).find_next_sibling('span').get_text(strip=True),
                                    gender=soup.find('label', text=re.compile('جنسیت')).find_next_sibling('span').get_text(strip=True),
                                    military_service_status=soup.find('label', text=re.compile('وضعیت خدمت')).find_next_sibling('span').get_text(strip=True),
                                )                                                     
                                new_candidate.save()                        
                            except (KeyError, requests.RequestException):
                                os.remove(file_path)
                                return Response({'success': False, 'status': 422, 'error': 'Cannot access URL'})

        except Exception as e:
            return Response({'success': False, 'status': 500, 'error': f'Error processing file: {str(e)}'})
        finally:
            os.remove(file_path)

            return Response({'success': True, 'status': 200, 'message': 'Data uploaded successfully.'})
    
class CandidateListAPIView(generics.ListAPIView):
    queryset=CandidateModel.objects.all()
    serializer_class=CandidateSerializer
    filter_backends = [filters.SearchFilter,filters.OrderingFilter]
    search_fields = ['job']
    ordering_fields = ['request_date']
    permission_classes=[IsSuperuserOrHR]