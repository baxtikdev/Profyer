from rest_framework import mixins, status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from .models import Page, Category, UserAnswer, Question, Option
from .paginator import CustomPagination
from .serializer import ServiceSerializer, PageSerializer, CategorySerializer, UserAnswerSerializer, GetAnswerSerializer
from users.models import Service, Country, UserVote
from django.conf import settings
from .tasks import add_ans
import pandas as pd


class ServiceAPIView(mixins.ListModelMixin, mixins.CreateModelMixin, GenericViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

    def create(self, request, *args, **kwargs):
        q = request.query_params.get('q')
        if q is not None and q in ['client', 'specialist', 'country']:
            make_questions(q)

        return Response(status=status.HTTP_200_OK)


def make_questions(type):
    from .dict_json import client, specialist, country
    Languages = ['ru', 'lt', 'uk', 'nl', 'es']
    if type == 'country':
        for c in country:
            ct = Country.objects.create(name=c['en']['name'])
            for lp in Languages:
                ct.set_current_language(language_code=lp)
                ct.name = c[lp]['name']
                ct.save()
        return
    elif type == 'client':
        data = client.get('translations')
    elif type == 'specialist':
        data = specialist.get('translations')
    for i in ['page1', 'page2', 'page3']:
        page = Page.objects.create(name=i)
        for part in data.get(i):
            for l in Languages:
                page.set_current_language(language_code=l)
                page.name = i
                page.save()

            category = Category.objects.create(page=page, name=part['category_name']['en']['name'])
            cat = part['category_name']
            for lp in Languages:
                if not cat[lp]['name']:
                    continue
                category.set_current_language(language_code=lp)
                category.name = cat[lp]['name']
                category.save()
            category = category

            for question in part['questions']:
                ques = Question.objects.create(category=category, type=question['type'], base=question['base'],
                                               text=question['question']['en']['text'])

                for lp in Languages:
                    if not question['question'][lp]['text']:
                        continue
                    ques.set_current_language(language_code=lp)
                    ques.text = question['question'][lp]['text']
                    ques.save()

                try:
                    for option in question['options']:
                        op = Option.objects.create(question=ques, text=option['en']['name'])

                        for opl in Languages:
                            if not option[opl]['name']:
                                continue
                            op.set_current_language(language_code=opl)
                            op.text = option[opl]['name']
                            op.save()
                except:
                    pass


class PageAPIView(mixins.ListModelMixin, GenericViewSet):
    queryset = Page.objects.all()
    serializer_class = PageSerializer
    pagination_class = CustomPagination


class QuestionAPIView(mixins.ListModelMixin, GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class UserAnswerAPIView(mixins.CreateModelMixin, GenericViewSet):
    queryset = UserAnswer.objects.all()
    serializer_class = UserAnswerSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        add_ans.delay(serializer.data)
        return Response(status=status.HTTP_200_OK)


class GetAnswerAPIView(mixins.CreateModelMixin, GenericViewSet):
    queryset = UserAnswer.objects.all()
    serializer_class = GetAnswerSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data.get('data')

        voteduser = UserVote.objects.get(id=data.get('user_id'))
        result = []
        for i in data.get('answers'):
            question = Question.objects.get(id=i.get('question_id'))
            # ans = UserAnswer.objects.create(user_id=data.get('user_id'), question=question)
            option_text = ''
            for j in i.get('options'):
                if question.type == 'SERVICES':
                    option = Service.objects.get(id=j)
                    option_text += f'{option.name}\n'
                    continue
                elif question.type == 'COUNTRY':
                    option = Country.objects.get(id=j)
                    option_text += f'{option.name}\n'
                    continue
                elif question.type == 'PERCENT':
                    # voteduser.percent = i.get('percent')
                    # voteduser.save()
                    option_text = f"{i.get('percent')} " + option_text
                    break
                elif question.type == 'NUMBER':
                    option_text = i.get('number')
                    break
                elif question.type == 'AGE':
                    option_text = i.get('age')
                    break
                else:
                    option = Option.objects.get(id=j)
                    option_text += f'{option.text}\n'
                    # ans.answer.add(option)
                    # ans.save()
            result.append({'Question': question.text, 'Option': option_text})

        file_url = f'{settings.BASE_DIR}/media/{voteduser.email}.xlsx'
        pd.DataFrame(result).to_excel(file_url)
        voteduser.file_url = file_url
        voteduser.save()
        return Response(status=status.HTTP_200_OK)
