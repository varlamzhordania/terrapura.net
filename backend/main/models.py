from django.db import models
from django.utils.translation import gettext_lazy as _
from autoslug import AutoSlugField

from core.models import BaseModel


class Herb(BaseModel):
    name = models.CharField(
        max_length=255,
        verbose_name=_('Name'),
        help_text=_('Common name of the herb'),
        unique=True,
    )
    slug = AutoSlugField(
        populate_from='name',
        verbose_name=_('Slug'),
        unique=True,
        editable=True,
        help_text=_('Unique Slug of the herb'),
    )
    latin_name = models.CharField(
        max_length=255,
        verbose_name=_('Latin Name'),
        blank=True,
        null=True,
        help_text=_("Scientific (Latin) name of the herb"),
    )
    description = models.TextField(
        verbose_name=_('Description'),
        blank=True,
        null=True,
        help_text=_("General description and overview of the herb."),
    )
    dosage = models.CharField(
        max_length=255,
        verbose_name=_('Dosage'),
        blank=True,
        null=True,
        help_text=_("Typical or recommended dosage."),
    )
    ailments = models.ManyToManyField(
        "Ailment",
        verbose_name=_('Ailments'),
        blank=True,
        related_name="herbs",
        help_text=_("Ailments this herb is used to treat."),
    )
    side_effects = models.ManyToManyField(
        "SideEffect",
        verbose_name=_('Side Effects'),
        related_name='herbs',
        blank=True,
        help_text=_("Known side effects of this herb."),
    )
    sources = models.ManyToManyField(
        'Source',
        verbose_name=_('Sources'),
        blank=True,
        related_name='herbs',
        help_text=_("Sources or websites where this data was extracted from."),
    )
    tags = models.ManyToManyField(
        'Tag',
        verbose_name=_('Tags'),
        blank=True,
        related_name='herbs'
    )

    class Meta:
        verbose_name = _('Herb')
        verbose_name_plural = _('Herbs')
        ordering = ('name',)

    def __str__(self):
        return f"{self.name} ({self.latin_name})" if self.latin_name else self.name


class HerbPreparationStep(BaseModel):
    class TypeChoices(models.TextChoices):
        TEA = 'tea', _('Tea / Infusion')  # Steeping leaves/flowers in hot water
        DECOCTION = 'decoction', _('Decoction')  # Boiling roots/bark
        TINCTURE = 'tincture', _('Tincture')  # Alcohol-based extraction
        CAPSULE = 'capsule', _('Capsule')  # Powder in pill form
        POWDER = 'powder', _('Powder')  # Dried and ground herb
        EXTRACT = 'extract', _('Extract')  # Concentrated form (e.g. liquid or solid)
        OIL = 'oil', _('Infused Oil')  # Herb-infused carrier oils
        SALVE = 'salve', _('Salve / Ointment')  # Thick topical preparation
        SYRUP = 'syrup', _('Syrup')  # Herb with sugar/honey for oral use
        JUICE = 'juice', _('Juice')  # Fresh-pressed liquid from herb
        SMOKE = 'smoke', _('Smoke / Incense')  # Smoked or burned herb
        BATH = 'bath', _('Bath / Soak')  # Used in water for skin or relaxation
        INHALATION = 'inhalation', _('Inhalation / Steam')  # Breathed in for respiratory benefits
        PASTE = 'paste', _('Paste / Poultice')  # Crushed herb applied topically
        FERMENTED = 'fermented', _(
            'Fermented'
        )  # Herbs prepared via fermentation (e.g. in kombucha)
        OTHER = 'other', _('Other')  # Catch-all for rare or custom preparations

    herb = models.ForeignKey(
        Herb,
        verbose_name=_('Herb'),
        on_delete=models.CASCADE,
        related_name='preparation_steps',
    )
    name = models.CharField(
        max_length=255,
        verbose_name=_('Step Name'),
        help_text=_('Name or title of the preparation step.'),
    )
    description = models.TextField(
        verbose_name=_('Step Description'),
        blank=True,
        null=True,
        help_text=_('Detailed description of the preparation step.'),
    )
    duration = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text=_("Optional duration for this step, e.g., '10 minutes'.")
    )
    temperature = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text=_("Optional temperature, e.g., '100°C' or 'boiling'.")
    )
    type = models.CharField(
        max_length=20,
        verbose_name=_('Preparation Type'),
        choices=TypeChoices.choices,
        default=TypeChoices.OTHER,
        blank=True,
        null=True,
    )
    order = models.PositiveIntegerField(
        verbose_name=_('Step Order'),
        default=0,
        help_text=_('Order in which the preparation step should be followed.'),
    )

    class Meta:
        verbose_name = _('Preparation Step')
        verbose_name_plural = _('Preparation Steps')
        ordering = ('herb', 'order', 'name')
        unique_together = ('herb', 'name')

    def __str__(self):
        return f"{self.herb.name} - {self.name} ({self.get_type_display()})"


class HerbWarning(BaseModel):
    class TypeChoices(models.TextChoices):
        DEADLY = 'deadly', _('Deadly')  # Toxic/lethal if consumed
        TOXIC = 'toxic', _('Toxic')  # Harmful in certain doses or conditions
        ALLERGIC_REACTION = 'allergic', _('Allergic Reaction')  # May trigger allergies
        DRUG_INTERACTION = 'interaction', _('Drug Interaction')  # Interferes with medications
        PREGNANCY_RISK = 'pregnancy', _('Unsafe During Pregnancy')  # Not safe for pregnancy
        BREASTFEEDING_RISK = 'breastfeeding', _(
            'Unsafe During Breastfeeding'
        )  # Unsafe for nursing mothers
        LIVER_DAMAGE = 'liver', _('Liver Damage Risk')  # May harm the liver
        KIDNEY_DAMAGE = 'kidney', _('Kidney Damage Risk')  # May affect kidneys
        PHOTOSENSITIVITY = 'photosensitivity', _('Photosensitivity')  # Increases sun sensitivity
        BLOOD_PRESSURE = 'blood_pressure', _(
            'Blood Pressure Effect'
        )  # Affects BP (raises or lowers)
        BLEEDING_RISK = 'bleeding', _('Bleeding Risk')  # Increases bleeding risk
        CHILDREN_UNSAFE = 'children', _('Not Safe for Children')
        LONG_TERM_USE = 'long_term_use', _('Unsafe for Long-Term Use')
        UNKNOWN = 'unknown', _('Unknown')  # Safety profile not well understood
        GENERAL = 'general', _('General Warning')  # Catch-all or general caution

    herb = models.ForeignKey(
        Herb,
        verbose_name=_('Herb'),
        on_delete=models.CASCADE,
        related_name='warnings',
    )
    name = models.CharField(
        max_length=255,
        verbose_name=_('Warning Title'),
        help_text=_('Short title or type of warning'),
    )
    description = models.TextField(
        verbose_name=_('Warning Description'),
        blank=True,
        null=True,
        help_text=_('Detailed warning or caution.'),
    )
    type = models.CharField(
        max_length=20,
        verbose_name=_('Warning Type'),
        choices=TypeChoices.choices,
        default=TypeChoices.GENERAL,
        blank=True,
        null=True,
    )
    order = models.PositiveIntegerField(
        verbose_name=_('Warning Order'),
        default=0,
    )

    class Meta:
        verbose_name = _('Herb Warning')
        verbose_name_plural = _('Herb Warnings')
        ordering = ('herb', 'order', 'name')
        unique_together = ('herb', 'name')

    def __str__(self):
        return f"{self.herb.name} - {self.name} ({self.get_type_display()})"


class ScientificStudy(BaseModel):
    herb = models.ForeignKey(
        Herb,
        verbose_name=_('Herb'),
        on_delete=models.CASCADE,
        related_name='scientific_studies',
    )
    title = models.CharField(
        max_length=255,
        verbose_name=_('Study Title'),
    )
    description = models.TextField(
        verbose_name=_('Study Description'),
        blank=True,
        null=True,
        help_text=_('Study description.'),
    )
    doi = models.CharField(
        max_length=255,
        verbose_name=_('Study DOI'),
        blank=True,
        null=True,
    )
    pubmed_id = models.CharField(
        verbose_name=_('PubMed ID'),
        max_length=255,
        blank=True,
        null=True,
    )
    link = models.URLField(
        verbose_name=_('External Link'),
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = _('Scientific Study')
        verbose_name_plural = _('Scientific Studies')
        ordering = ('herb', 'title', 'created_at')

    def __str__(self):
        return f"{self.herb.name} - {self.title}"


class Ailment(BaseModel):
    name = models.CharField(
        max_length=255,
        verbose_name=_('Name'),
        unique=True,
    )
    slug = AutoSlugField(
        populate_from='name',
        verbose_name=_('Slug'),
        unique=True,
        editable=True,
        help_text=_('Unique Slug of the ailment'),
    )
    description = models.TextField(
        verbose_name=_('Description'),
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = _('Ailment')
        verbose_name_plural = _('Ailments')
        ordering = ('name', 'created_at')

    def __str__(self):
        return self.name


class SideEffect(BaseModel):
    name = models.CharField(
        max_length=255,
        verbose_name=_('Name'),
        unique=True,
    )
    slug = AutoSlugField(
        populate_from='name',
        verbose_name=_('Slug'),
        unique=True,
        editable=True,
        help_text=_('Unique Slug of the side effect'),
    )
    description = models.TextField(
        verbose_name=_('Description'),
        blank=True,
    )
    severity = models.CharField(
        max_length=255,
        verbose_name=_('Severity'),
        blank=True,
        null=True,
        help_text=_('Severity value.'),
    )

    class Meta:
        verbose_name = _('Side Effect')
        verbose_name_plural = _('Side Effects')
        ordering = ('name', 'created_at')

    def __str__(self):
        return self.name


class Source(BaseModel):
    name = models.CharField(
        max_length=255,
        verbose_name=_('Name'),
        help_text=_('Common name of the source'),
    )
    url = models.URLField(
        verbose_name=_('URL'),
        unique=True,
        help_text=_('Website URL of the source'),
    )
    description = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name=_('Source Description'),
    )

    class Meta:
        verbose_name = _('Source')
        verbose_name_plural = _('Source')
        ordering = ('name', 'created_at')

    def __str__(self):
        return f"{self.name} - {self.url}"


class Tag(BaseModel):
    name = models.CharField(
        max_length=100,
        verbose_name=_('Name'),
        unique=True,
        help_text=_('Common name of the tag'),
    )
    slug = AutoSlugField(
        populate_from='name',
        verbose_name=_('Slug'),
        unique=True,
        editable=True,
        help_text=_('Unique Slug of the tag'),
    )

    class Meta:
        verbose_name = _('Tag')
        verbose_name_plural = _('Tags')
        ordering = ('name', 'created_at')

    def __str__(self):
        return self.name
