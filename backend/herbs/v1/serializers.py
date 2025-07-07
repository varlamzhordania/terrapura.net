from rest_framework import serializers

from herbs.models import (
    Category,
    Herb,
    HerbMedia,
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

from core.models import SEO_MODEL_FIELDS


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class HerbMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = HerbMedia
        fields = "__all__"


class HerbPreparationStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = HerbPreparationStep
        fields = "__all__"


class HerbWarningSerializer(serializers.ModelSerializer):
    class Meta:
        model = HerbWarning
        fields = "__all__"


class ScientificStudySerializer(serializers.ModelSerializer):
    class Meta:
        model = ScientificStudy
        fields = "__all__"


class AilmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ailment
        fields = "__all__"


class SideEffectSerializer(serializers.ModelSerializer):
    class Meta:
        model = SideEffect
        fields = "__all__"


class SymptomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Symptom
        fields = "__all__"


class IllnessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Illness
        fields = "__all__"


class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        fields = "__all__"


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"


class HerbSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField(many=False, read_only=True)
    ailments = serializers.StringRelatedField(many=True, read_only=True)
    tags = serializers.StringRelatedField(many=True, read_only=True)
    illnesses = serializers.StringRelatedField(many=True, read_only=True)
    symptoms = serializers.StringRelatedField(many=True, read_only=True)
    side_effects = serializers.StringRelatedField(many=True, read_only=True)
    medias = HerbMediaSerializer(many=True, read_only=True)

    class Meta:
        model = Herb
        fields = [
            'name',
            'slug',
            'latin_name',
            'description',
            'category',
            'dosage',
            'image_link',
            'ailments',
            'side_effects',
            'symptoms',
            'illnesses',
            'sources',
            'tags',
            'medias',
        ]


class HerbSEOSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=False, read_only=True)
    ailments = AilmentSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    illnesses = IllnessSerializer(many=True, read_only=True)
    symptoms = SymptomSerializer(many=True, read_only=True)
    side_effects = SideEffectSerializer(many=True, read_only=True)
    sources = SourceSerializer(many=True, read_only=True)
    medias = HerbMediaSerializer(many=True, read_only=True)
    warnings = HerbWarningSerializer(many=True, read_only=True)
    scientific_studies = ScientificStudySerializer(many=True, read_only=True)

    class Meta:
        model = Herb
        fields = [
                     'name',
                     'slug',
                     'latin_name',
                     'description',
                     'category',
                     'dosage',
                     'image_link',
                     'ailments',
                     'side_effects',
                     'symptoms',
                     'illnesses',
                     'sources',
                     'tags',
                     'medias',
                     'warnings',
                     'scientific_studies',
                 ] + SEO_MODEL_FIELDS
