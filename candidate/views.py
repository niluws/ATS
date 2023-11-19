import os,requests,re
from bs4 import BeautifulSoup
from jdatetime import datetime as jdatetime
from jdatetime import datetime as jdatetime_datetime
from jdatetime import date as jdatetime_date
from jdatetime import timedelta as jdatetime_timedelta
from openpyxl import load_workbook
from django.contrib.sites.shortcuts import get_current_site
from django_filters.rest_framework import DjangoFilterBackend
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.mail import EmailMessage
from rest_framework import generics,filters
from rest_framework.response import Response

from authentication.permissions import IsSuperuserOrHR
from job.models import Requirement
from utils import config
from .serializers import ExcelFileSerializer,CandidateSerializer,ScoreSerializer,CandidateUpdateSerializer
from .models import CandidateModel,EducationModel,PreferencesModel,ExperiencesModel


class UploadExcelAPIView(generics.CreateAPIView):
    serializer_class = ExcelFileSerializer
    permission_classes=[IsSuperuserOrHR]

    def save_education(self, soup, candidate_id):
        for education in soup.select('div.card-header:-soup-contains("تحصیلی") + div.card-body div.list-group-item label.d-block'):
            education_text = education.get_text(strip=True).split('-')
            if education_text:
                new_education = EducationModel(
                    candidate_id=candidate_id,
                    level=education_text[0].strip(),
                    major=education_text[1].strip(),
                    university=education.find_next('div', class_='font-size-base').find('span').get_text(strip=True),
                    duration=re.sub(r'\s+', ' ', education.find_next('div', class_='font-size-base').find('span', class_='mr-3').text),
                )
            else: None
            new_education.save()
            
    def save_preferences(self, soup, candidate_id):
        output_dict = {}   
        for preference in soup.select('div.card-header:-soup-contains("ترجیحات") + div.card-body div.list-group-item label.d-block'):
            next_sibling = preference.find_next_sibling('div', class_='font-size-2xl vertical-align-middle color-grey-light-1')
            values = next_sibling.find_all('label', class_='font-size-base color-grey-dark-2 mh-1')
            key = re.sub(r'\s+', ' ', preference.get_text(strip=True).replace('\u200c', ' ').strip())
            value = [re.sub(r'\s+', ' ',val.get_text(strip=True).replace('\u200c', ' ').replace('\n', '')) for val in values]
            output_dict[key] = value

        new_preference = PreferencesModel(
            candidate_id=candidate_id,
            proviences=output_dict.get('استان های مورد نظر برای کار:'),
            job_category=output_dict.get('دسته بندی شغلی و زمینه کاری:'),
            job_level=output_dict.get('سطح ارشدیت در زمینه فعالیت:'),
            contracts_type=output_dict.get('نوع قراردادهای قابل قبول:'),
            salary=output_dict.get('حقوق مورد نظر:'),
            benefits=output_dict.get('مزایای شغلی مورد علاقه:') if 'مزایای شغلی مورد علاقه:' in output_dict else None
        )
        new_preference.save()

    def extract_languages(self, soup):
        language_element=soup.select('div.card-header:-soup-contains("زبان") + div.card-body div.list-group-item')
        return  [ re.sub(r'\s+',' ',language.find('label').get_text()) for language in language_element] if language_element else None

    def save_experiences(self, soup,candidate_id):
        for experience in soup.select('div.card-header:-soup-contains("سوابق شغلی") + div.card-body div.list-group-item'):
            title=experience.find('label').text
            company=experience.find('span').text
            start_at=re.sub(r'\s+',' ',experience.find('span',class_='mr-3').find('b').text)
            end_at=re.sub(r'\s+',' ',experience.find('span',class_='mr-3').find_all('b')[-1].text.strip())

            start_date = jdatetime.strptime(start_at, "%B %Y").date()
            if end_at == "حالا":
                end_date = jdatetime.now().date()
            else:
                end_date = jdatetime.strptime(end_at, "%B %Y").date()

            
            new_experience=ExperiencesModel(
                candidate_id=candidate_id,
                title=title or None,
                company=company or None,
                start_at=start_at or None,
                end_at=end_at or None,
                duration=(end_date - start_date).days
            )
            new_experience.save()

    def extract_skills(self, soup):
        skill_element= soup.select('div.card-header:-soup-contains("حرفه") + div.card-body div.font-size-2xl.vertical-align-middle.color-grey-light-1 label.font-size-base.color-grey-dark-2.mh-1')
        return  [skill.get_text(strip=True) for skill in skill_element] if  skill_element else None

    def extract_data(self, soup, label_text):
        label = soup.find('label', text=re.compile(label_text))
        if label:
            return re.sub(r'\s+',' ',label.find_next_sibling('span').get_text(strip=True))
        else:None

    def post(self, request, *args, **kwargs):
        uploaded_file = request.FILES.get('file')

        if not uploaded_file:
            
            return Response({'success': False, 'status': 400, 'error': 'No file uploaded'})
        file_name = default_storage.save(uploaded_file, uploaded_file)
        file_path = default_storage.path(file_name)

        try:
            workbook = load_workbook(file_path)
            worksheet = workbook.active
            new_user_count=0
            
            for row in worksheet.iter_rows(min_col=2, min_row=2):
                user_email = row[3].value

                if not user_email:
                    continue
                    
                exist_candidate = CandidateModel.objects.filter(email=user_email).exists()
                
                if not exist_candidate:

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
                                resume=ContentFile(resume_response.content, name=f"{row[0].value}/{row[1].value}.pdf") if resume_response else None,
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
                                languages=self.extract_languages(soup),
                            )

                            new_candidate.save()
                            self.save_preferences(soup,new_candidate.pk)
                            self.save_education(soup, new_candidate.pk)
                            self.save_experiences(soup, new_candidate.pk)
                            new_user_count+=1

                        except (KeyError, requests.RequestException):
                            os.remove(file_path)
                            return Response({'success': False, 'status': 422, 'error': 'Cannot access URL'})
        except Exception as e:
            return Response({'success': False, 'status': 500, 'error': f'Error processing file: {str(e)}'})
        finally:
            os.remove(file_path)
            return Response({'success': True, 'status': 200, 'message': f'{new_user_count} Data uploaded.'})


class ScoreOnlineResume(generics.ListAPIView):
    queryset = CandidateModel.objects.all()
    serializer_class = ScoreSerializer

    def get_object(self,candidate_id):
        education_queryset=EducationModel.objects.filter(candidate_id=candidate_id)
        return education_queryset
    #TODO just score to candidates who have no score
    def calculate_skill_score(self, candidate):
        
        requirement = Requirement.objects.all()
        
        education=self.get_object(candidate.id)  
                
        total_score = 0

        for req in requirement:
            en=req.en_title
            fa=req.fa_title
            
            for edu in education:                
                if en in edu.level or fa in edu.level or en in edu.major or fa in edu.major:
                    total_score += req.score
                    
                    break
            
            for skill in candidate.languages,candidate.skills:
                en=req.en_title
                fa=req.fa_title
                if skill is not None:

                    if en.lower() in ''.join(skill).lower() or fa in ''.join(skill).lower():
                        total_score += req.score  
                        break

        return total_score
    
    def get(self, request, *args, **kwargs):
        candidates = self.get_queryset()
        for candidate in candidates:
            skill_score = self.calculate_skill_score(candidate)
            candidate.score = skill_score
            candidate.save()
            if candidate.score is None:
                if candidate.score >= 2:
                    print('accepted:Send Interview Invitation date')
                #     EmailMessage(f'Interview Invitation - {candidate.job}', 'Scheduled Interview: [Date] at [Time]',
                #                  config.EMAIL_HOST_USER, [candidate.email]).send()
                else:
                    print('rejected')
                #     EmailMessage(f'Your resume rejected', 'Hello, we may reach out to you again in the future',
                #                  config.EMAIL_HOST_USER, [candidate.email]).send()

        serializer = ScoreSerializer(candidates, many=True)

        return Response(serializer.data, status=200)

class CandidateListAPIView(generics.ListAPIView):
    queryset=CandidateModel.objects.all()
    serializer_class=CandidateSerializer
    filter_backends = [filters.SearchFilter,filters.OrderingFilter]
    search_fields = ['job']
    ordering_fields = ['request_date']
    permission_classes=[IsSuperuserOrHR]

class CandidateUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset=CandidateModel.objects.all()
    serializer_class=CandidateUpdateSerializer

    def perform_update(self, serializer):
        candidate = serializer.instance
        
        resume = serializer.validated_data.get('resume')
        if resume:
            jalali_update_date = jdatetime_datetime.fromgregorian(datetime=candidate.update_at)
            formatted_update_date = jalali_update_date.strftime('%Y_%m_%d_%H_%M')
         
            file_path = f"{candidate.job}/{candidate.name}_{formatted_update_date}.pdf"

            candidate.resume.save(file_path, resume, save=True)

    
    
class OldCandidateInvitationAPIView(generics.ListAPIView):
    queryset=CandidateModel.objects.all()
    serializer_class=CandidateSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('job', )

    def get(self, request, *args, **kwargs):
        job_param = request.GET.get('job', '')
        candidates = CandidateModel.objects.filter(job=job_param)
        current_site = get_current_site(self.request)
        for candidate in candidates:
            self.send_invitation_email(candidate, job_param,current_site,candidate.id)

        return self.list(request, *args, **kwargs)
    
    def send_invitation_email(self, candidate, job_param,current_site,candidate_id):
        print(f'Hello {candidate.name} Please consider updating your resume and applying for {job_param} position if you are interested Click on the following link to apply:http://{current_site.domain}/candidate/candidate_update/{candidate_id}',)
        
        # EmailMessage('Job Opportunity Update',
        #             f'Hello {candidate.name} \n'/
        #             f'Please consider updating your resume and applying for {job_param} position if you are interested.\n '\
        #             'Click on the following link to apply:',
        #             config.EMAIL_HOST_USER, [candidate.email]).send()



