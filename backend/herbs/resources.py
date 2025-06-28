from import_export import resources
from .models import (
    Herb,
    HerbPreparationStep,
    HerbWarning,
    ScientificStudy,
    Ailment,
    SideEffect,
    Symptom,
    Illness,
    Source,
    Tag,
)


class HerbResource(resources.ModelResource):
    class Meta:
        model = Herb


class HerbPreparationStepResource(resources.ModelResource):
    class Meta:
        model = HerbPreparationStep


class HerbWarningResource(resources.ModelResource):
    class Meta:
        model = HerbWarning


class ScientificStudyResource(resources.ModelResource):
    class Meta:
        model = ScientificStudy


class AilmentResource(resources.ModelResource):
    class Meta:
        model = Ailment


class SideEffectResource(resources.ModelResource):
    class Meta:
        model = SideEffect


class SymptomResource(resources.ModelResource):
    class Meta:
        model = Symptom


class IllnessResource(resources.ModelResource):
    class Meta:
        model = Illness


class SourceResource(resources.ModelResource):
    class Meta:
        model = Source


class TagResource(resources.ModelResource):
    class Meta:
        model = Tag
