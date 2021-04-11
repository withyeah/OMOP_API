from django.db import models

# Create your models here.
class Person(models.Model):
    gender_concept_id = models.IntegerField()
    year_of_birth = models.IntegerField()
    month_of_birth = models.IntegerField()
    day_of_birth = models.IntegerField()
    birth_datetime = models.DateTimeField()
    race_concept_id = models.IntegerField()
    ethnicity_concept_id = models.IntegerField()
    location_id = models.BigIntegerField()
    provider_id = models.BigIntegerField()
    care_site_id = models.BigIntegerField()
    person_source_value = models.CharField(max_length=50)
    gender_source_value = models.CharField(max_length=50)
    gender_source_concept_id = models.IntegerField()
    race_source_value = models.CharField(max_length=50)
    race_source_concept_id = models.IntegerField()
    ethnicity_source_value = models.CharField(max_length=50)
    ethnicity_source_concept_id = models.IntegerField()

    def __str__(self):
        return self.pk


class VisitOccurrence(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    visit_concept_id = models.IntegerField()
    visit_start_date = models.DateField()
    visit_start_datetime = models.DateTimeField()
    visit_end_date = models.DateField()
    visit_end_datetime = models.DateTimeField()
    visit_type_concept_id = models.IntegerField()
    provider_id = models.BigIntegerField()
    care_site_id = models.BigIntegerField()
    visit_source_value = models.CharField(max_length=50)
    visit_source_concept_id = models.IntegerField()
    admitted_from_concept_id = models.IntegerField()
    admitted_from_source_value = models.CharField(max_length=50)
    discharge_to_source_value = models.CharField(max_length=50)
    discharge_to_concept_id = models.IntegerField()
    preceding_visit_occurrence_id = models.BigIntegerField()

    def __str__(self):
        return self.pk


class ConditionOccurrence(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    visit_occurrence = models.ForeignKey(VisitOccurrence, on_delete=models.CASCADE)
    condition_concept_id = models.IntegerField()
    condition_start_date = models.DateField()
    condition_start_datetime = models.DateTimeField()
    condition_end_date = models.DateField()
    condition_end_datetime = models.DateTimeField()
    condition_type_concept_id = models.IntegerField()
    condition_status_concept_id = models.IntegerField()
    stop_reason = models.CharField(max_length=20)
    provider_id = models.BigIntegerField()
    visit_detail_id = models.BigIntegerField()
    condition_source_value = models.CharField(max_length=50)
    condition_source_concept_id = models.IntegerField()
    condition_status_source_value = models.CharField(max_length=50)

    def __str__(self):
        return self.pk


class DrugExposure(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    visit_occurrence = models.ForeignKey(VisitOccurrence, on_delete=models.CASCADE)
    drug_concept_id = models.IntegerField()
    drug_exposure_start_date = models.DateField()
    drug_exposure_start_datetime = models.DateTimeField()
    drug_exposure_end_date = models.DateField()
    drug_exposure_end_datetime = models.DateTimeField()
    verbatim_end_date = models.DateField()
    drug_type_concept_id = models.IntegerField()
    stop_reason = models.CharField(max_length=20)
    refills = models.IntegerField()
    quantity = models.IntegerField()
    days_supply = models.IntegerField()
    sig = models.TextField()
    route_concept_id = models.IntegerField()
    lot_number = models.CharField(max_length=50)
    provider_id = models.BigIntegerField()
    visit_detail_id = models.BigIntegerField()
    drug_source_value = models.CharField(max_length=50)
    drug_source_concept_id = models.IntegerField()
    route_source_value = models.CharField(max_length=50)
    dose_unit_source_value = models.CharField(max_length=50)

    def __str__(self):
        return self.pk


class Concept(models.Model):
    concept_name = models.CharField(max_length=255)
    domain_id = models.CharField(max_length=20)
    vocabulary_id = models.CharField(max_length=20)
    concept_class_id = models.CharField(max_length=20)
    standard_concept = models.CharField(max_length=1)
    concept_code = models.CharField(max_length=50)
    valid_start_date = models.DateField()
    valid_end_date = models.DateField()
    invalid_reason = models.CharField(max_length=1)

    def __str__(self):
        return self.concept_name


class Death(models.Model):
    person = models.OneToOneField(Person, on_delete=models.CASCADE)
    death_date = models.DateField()
    death_datetime = models.DateTimeField()
    death_type_concept_id = models.IntegerField()
    cause_concept_id = models.BigIntegerField()
    cause_source_value = models.IntegerField()
    cause_source_concept_id = models.BigIntegerField()

    def __str__(self):
        return self.pk





