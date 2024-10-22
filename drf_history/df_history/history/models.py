from django.db import models

# Create your models here.


class HistoricalFigure(models.Model):
    id = models.AutoField(primary_key=True)
    given_names = models.CharField(max_length=255)
    family_name = models.CharField(max_length=255)
    birth_year = models.CharField(max_length=10, blank=True, null=True)
    death_year = models.CharField(max_length=10, blank=True, null=True)
    short_description = models.TextField()
    link = models.URLField(max_length=500, blank=True, null=True)
    biography_content = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'historical_figure'
        verbose_name = 'Historical figure information management'
        verbose_name_plural = 'Historical figure information management'

    def __str__(self):
        return f"{self.given_names} {self.family_name}"
