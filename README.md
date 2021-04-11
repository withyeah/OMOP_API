[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![python](https://img.shields.io/badge/Python-3.8.8-1f425f)](https://www.python.org/)
[![django](https://img.shields.io/badge/django-3.2-092e20)](https://www.djangoproject.com/)

# OMOP API 가이드

[TOc]

## Tools

> pyenv == 1.2.26
>
> pgadmin4 == 5.1
>
> vscode == 1.55.1
>
> macOS == 11.2.3

<br>

## ERD

https://www.erdcloud.com/d/6JveQxBkK8PHyFBtY

<br>

## Guide

1. git clone

   ```bash
   $ git clone https://github.com/withyeah/OMOP_API.git
   ```

2. 가상환경 생성 및 실행

   ```bash
   $ python -m venv venv
   
   # macOS
   $ source venv/bin/activate
   
   # windows
   $ source venv/Scripts/activate
   ```

3. 패키지 설치

   ```bash
   $ pip install -r requirements.txt
   ```

4. run server

   ```bash
   $ python manage.py runserver
   ```

<br>

## API SWAGGER

> http://127.0.0.1:8000/api/v1/swagger/

<br>

## TO DO

### 1번문제 : 연령대(10세 단위)별 방문 수

- datetime 모듈 사용

  - ```python
    from datetime import datetime
    
    current_time = datetime.now()
    person_time_list = Person.objects.values('birth_datetime')
    ```

    1. person_time_list를 for문 순회
    2. current_time을 이용해 각 person의 현재 나이 계산
    3. 각 나이별 조건문을 이용해서 나이대에 해당하는 딕셔너리로 누적합

### 2번 문제 : concept_id들의 정보를 얻을 수 있는 API

키워드 검색 기능, pagination 포함

- 키워드 검색 기능

  - [drf generic filtering document](https://www.django-rest-framework.org/api-guide/filtering/#generic-filtering)

  - ```python
    # settings.py
    REST_FRAMEWORK = {
        'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend']
    }
    ```

    ```python
    # views.py
    class ConceptList(generics.ListAPIView):
        queryset = Concept.objects.all()
        serializer_class = ConceptSerializer
        filter_backends = [DjangoFilterBackend]
        filterset_fields = ['concept_name']
    ```

- pagination

  - [drf pagination document](https://www.django-rest-framework.org/api-guide/pagination/#pagination)

  - ```python
    # settings.py
    REST_FRAMEWORK = {
        'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
        'PAGE_SIZE': 100
    }
    ```

    ```python
    # paginators.py
    class PatientsSetPagination(PageNumberPagination):
        page_size = 100
        page_size_query_param = 'page_size'
        max_page_size = 1000
    ```

    ```python
    # views.py
    from .paginators import PatientsSetPagination
    
    @api_view(['GET'])
    def patient_view(request):
    
        paginator = PatientsSetPagination()
        paginator.page_size = 10
        patient_objects = Person.objects.all()
        result_page = paginator.paginate_queryset(patient_objects, request)
        serializer = PersonSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
    ```


<br>

### 3번 문제 : 각 테이블의 row를 조회하는 API

concept id와 concept name 매칭, pagination, 키워드 검색

- concept id와 concept name 매칭

