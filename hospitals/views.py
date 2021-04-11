from django.core import serializers
from django.db.models import Count, Max, Q
from django.http.response import HttpResponse
from django.shortcuts import get_list_or_404, render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Concept, Death, Person, VisitOccurrence
from .serializers import PersonSerializer, VisitOccurrenceSerializer

# Create your views here.

@api_view(['GET'])
def patients_list(request):
    queryset = get_list_or_404(Person)
    patients_count = queryset.count()

    male = Concept.objects.get(concept_name='MALE').concept_id
    female = Concept.objects.get(concept_name='FEMALE').concept_id
    gender_male_count = Person.objects.filter(gender_concept_id=male).count()
    gender_female_count = Person.objects.filter(gender_concept_id=female).count()

    race_data = {}
    ethnicity_data = {}

    for person in queryset.iterator():
        race = Concept.objects.get(concept_id=person.race_concept_id).concept_name
        race_data[race] = race_data.get(race, 0) + 1

        ethnicity = Concept.objects.get(
            concept_id=person.ethnicity_concept_id
        ).concept_name
        ethnicity_data[ethnicity] = ethnicity_data.get(ethnicity, 0) + 1

    death_count = Death.objects.count()

    data = {
        'patients_count': patients_count,
        'patients_gender_count': {
            'male': gender_male_count,
            'female': gender_female_count,
        },
        'race_data': race_data,
        'ethnicity_data': ethnicity_data,
        'patients_death_count': death_count,
    }
    return Response(data)


@api_view(['GET'])
def visits_list(request):
    queryset = get_list_or_404(VisitOccurrence)

    visit_type_data = {}
    visit_gender_data = {}
    visit_race_data = {}
    visit_ethnicity_data = {}

    for visit in queryset.iterator():
        visit_type = Concept.objects.get(concept_id=visit.visit_concept_id).concept_name
        visit_type_data[visit_type] = visit_type_data.get(visit_type, 0) + 1

        gender = Person.objects.get(person_id=visit.person_id).gender_concept_id
        visit_gender = Concept.objects.get(concept_id=gender).concept_name
        visit_gender_data[visit_gender] = visit_gender_data.get(visit_gender, 0) + 1

        race = Person.objects.get(person_id=visit.person_id).race_concept_id
        visit_race = Concept.objects.get(concept_id=race).concept_name
        visit_race_data[visit_race] = visit_race_data.get(visit_race, 0) + 1

        ethnicity = Person.objects.get(person_id=visit.person_id).ethnicity_concept_id
        visit_ethnicity = Concept.objects.get(concept_id=ethnicity).concept_name
        visit_ethnicity_data[visit_ethnicity] = (
            visit_ethnicity_data.get(visit_ethnicity, 0) + 1
        )

    data = {
        'visit_type_count': visit_type_data,
        'visit_gender_count': visit_gender_data,
        'visit_race_count': visit_race_data,
        'visit_ethnicity_count': visit_ethnicity_data,
    }

    return Response(data)
