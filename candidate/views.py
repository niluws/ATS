import os,requests,uuid,re
from bs4 import BeautifulSoup
# from PyPDF2 import PdfFileReader
from openpyxl import load_workbook
from django.core.files.base import ContentFile
from rest_framework import generics,filters
from rest_framework.response import Response
from authentication.permissions import IsSuperuserOrHR
from .serializers import ExcelFileSerializer,CandidateSerializer
from .models import ExcelFileModel,CandidateModel,EducationModel,PreferencesModel


class UploadExcelAPIView(generics.CreateAPIView):
    serializer_class = ExcelFileSerializer
    # permission_classes=[IsSuperuserOrHR]

    def save_education(self, soup, candidate_id):
        for education in soup.select('div.card-header:-soup-contains("تحصیلی") + div.card-body div.list-group-item label.d-block'):
            education_text = education.get_text(strip=True).split('-')
            if education_text:
                new_education = EducationModel(
                    candidate_id=candidate_id,
                    level=education_text[0].strip(),
                    major=education_text[1].strip(),
                    university=education.find_next('div', class_='font-size-base').find('span').get_text(strip=True),
                    duration=re.sub(r'\s+', '', education.find_next('div', class_='font-size-base').find('span', class_='mr-3').text),
                )
            else: None
            new_education.save()
            
    def save_preferences(self, soup, candidate_id):
        output_dict = {}
        for preference in soup.select('div.card-header:-soup-contains("ترجیحات") + div.card-body div.list-group-item label.d-block'):
            next_sibling = preference.find_next_sibling('div', class_='font-size-2xl vertical-align-middle color-grey-light-1')
            values = next_sibling.find_all('label', class_='font-size-base color-grey-dark-2 mh-1')
            key = re.sub(r'\s+', ' ', preference.get_text(strip=True).replace('\u200c', '').strip())
            value = [val.text.replace('\u200c', '').split() for val in values]
            output_dict[key] = value

        new_preference = PreferencesModel(
            candidate_id=candidate_id,
            proviences=output_dict.get('استانهای مورد نظر برای کار:'),
            job_category=output_dict.get('دستهبندی شغلی و زمینه کاری:'),
            job_level=output_dict.get('سطح ارشدیت در زمینه فعالیت:'),
            contracts_type=output_dict.get('نوع قراردادهای قابل قبول:'),
            salary=output_dict.get('حقوق مورد نظر:'),
            benefits=output_dict.get('مزایای شغلی مورد علاقه:') if 'مزایای شغلی مورد علاقه:' in output_dict else None
        )
        new_preference.save()

    def extract_languages(self, soup):
        return  [ re.sub(r'\s+',' ',language.find('label').get_text()) for language in soup.select('div.card-header:-soup-contains("زبان") + div.card-body div.list-group-item')] if soup.select('div.card-header:-soup-contains("زبان") + div.card-body div.list-group-item') else None

    def extract_experiences(self, soup):
        return  [label.get_text(strip=True) for label in soup.select('div.card-header:-soup-contains("سوابق شغلی") + div.card-body div.list-group-item label.d-block')] or None

    def extract_skills(self, soup):
        return  [skill.get_text(strip=True) for skill in soup.select('div.card-header:-soup-contains("حرفه") + div.card-body div.font-size-2xl.vertical-align-middle.color-grey-light-1 label.font-size-base.color-grey-dark-2.mh-1')] if  soup.select('div.card-header:-soup-contains("حرفه") + div.card-body div.font-size-2xl.vertical-align-middle.color-grey-light-1 label.font-size-base.color-grey-dark-2.mh-1') else None

        
    def extract_data(self, soup, label_text):
        label = soup.find('label', text=re.compile(label_text))
        return label.find_next_sibling('span').get_text(strip=True) if label else None

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
            

            for row in worksheet.iter_rows(min_col=2, min_row=2):
                user_email = row[3].value

                if not user_email:
                    continue
                    
                exist_candidate = CandidateModel.objects.filter(email=user_email).exists()

                if not exist_candidate:
                    # continue

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
                                resume=ContentFile(resume_response.content, name=f"{row[0].value}/{row[1].value}_{row[2].value}.pdf") if resume_response else None,
                                job_status=self.extract_data(soup, 'وضعیت اشتغال'),
                                last_company=self.extract_data(soup, 'شرکت'),
                                education_level=self.extract_data(soup, 'تحصیلی'),
                                province=self.extract_data(soup, 'استان'),
                                location=self.extract_data(soup, 'آدرس محل'),
                                marital=self.extract_data(soup, 'تاهل'),
                                birthdate=self.extract_data(soup, 'سال تولد'),
                                gender=self.extract_data(soup, 'جنسیت'),
                                military_service_status=self.extract_data(soup, 'وضعیت خدمت'),
                                about=soup.find('p', class_='u-textJustify').get_text() if soup.find('p', class_='u-textJustify') else None,
                                skills=self.extract_skills(soup),
                                experiences=self.extract_experiences(soup),
                                languages=self.extract_languages(soup),
                            )


                            new_candidate.save()
                            self.save_preferences(soup,new_candidate.pk)
                            self.save_education(soup, new_candidate.pk)



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