# Generated by Django 5.1.5 on 2025-01-29 16:31

import django.db.models.deletion
import edudata.models
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="School",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("school_id", models.IntegerField(unique=True)),
                ("school_name", models.CharField(max_length=500)),
                (
                    "school_type",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("BOARDING", "Boarding School"),
                            ("DAY", "Day School"),
                            ("BOTH", "Boarding and Day School"),
                        ],
                        max_length=100,
                        null=True,
                    ),
                ),
                (
                    "school_level",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("KINDERGARTEN", "Kindergarten"),
                            ("PRIMARY", "Primary School"),
                            ("SECONDARY", "Secondary School"),
                            ("COMBINED", "Combined School"),
                            ("TVET", "Technical and Vocational"),
                            ("TERTIARY", "Tertiary Institution"),
                            ("UNIVERSITY", "University"),
                            ("COLLEGE", "College"),
                            ("INSTITUTE", "Institute"),
                            ("OTHER", "Other"),
                        ],
                        max_length=100,
                        null=True,
                    ),
                ),
                (
                    "school_gender",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("M", "Boys Only"),
                            ("F", "Girls Only"),
                            ("MF", "Mixed Gender"),
                        ],
                        default="MF",
                        max_length=100,
                        null=True,
                    ),
                ),
                (
                    "school_ownership",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("PUBLIC", "Public School"),
                            ("PRIVATE", "Private School"),
                            ("GOVT_AIDED", "Government Aided"),
                            ("RELIGIOUS", "Religious Institution"),
                            ("INTERNATIONAL", "International School"),
                            ("OTHER", "Other"),
                        ],
                        max_length=100,
                        null=True,
                    ),
                ),
                (
                    "average_rating",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=3, null=True
                    ),
                ),
                ("review_count", models.IntegerField(default=0)),
                ("school_description", models.TextField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name="AlumniNetwork",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("notable_alumni", models.JSONField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "school",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="edudata.school"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="AdmissionPolicy",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "admission_policy",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("OPEN", "Open Admission"),
                            ("SELECTIVE", "Selective Admission"),
                            ("MERIT", "Merit Based"),
                            ("INTERVIEW", "Interview Required"),
                            ("EXAM", "Entrance Examination"),
                            ("OTHER", "Other"),
                        ],
                        max_length=100,
                        null=True,
                    ),
                ),
                (
                    "discipline_policy",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("STRICT", "Strict"),
                            ("MODERATE", "Moderate"),
                            ("LENIENT", "Lenient"),
                            ("SELF", "Self-Disciplined"),
                            ("OTHER", "Other"),
                        ],
                        max_length=100,
                        null=True,
                    ),
                ),
                ("parental_engagement", models.CharField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "school",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="edudata.school"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="SchoolContact",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "phone_number",
                    models.CharField(blank=True, max_length=13, null=True),
                ),
                ("email", models.EmailField(blank=True, max_length=254, null=True)),
                ("website", models.URLField(blank=True, null=True)),
                ("social_media", models.JSONField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "school",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="edudata.school"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="SchoolFees",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("currency", models.CharField(blank=True, max_length=100, null=True)),
                (
                    "amount",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=10, null=True
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "school",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="edudata.school"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="SchoolGovernmentData",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("government_supported", models.BooleanField(default=False)),
                ("registration_date", models.DateField(blank=True, null=True)),
                ("inspection_record", models.JSONField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "school",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="edudata.school"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="SchoolImage",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        upload_to=edudata.models.SchoolImage.school_image_path
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "school",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="images",
                        to="edudata.school",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="SchoolLocation",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("province", models.CharField(blank=True, max_length=50, null=True)),
                ("district", models.CharField(blank=True, max_length=50, null=True)),
                ("sector", models.CharField(blank=True, max_length=50, null=True)),
                ("cell", models.CharField(blank=True, max_length=50, null=True)),
                ("village", models.CharField(blank=True, max_length=50, null=True)),
                ("address", models.CharField(blank=True, max_length=500, null=True)),
                ("latitude", models.FloatField(blank=True, null=True)),
                ("longitude", models.FloatField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "school",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="edudata.school"
                    ),
                ),
            ],
        ),
    ]
