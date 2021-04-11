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

