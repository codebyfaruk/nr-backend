from django.db import models

# Create your models here.
class LabelTemplate(models.Model):
    name = models.CharField(max_length=100)
    total_width = models.FloatField(null=True, blank=True, verbose_name="Total Width (mm)")
    total_height = models.FloatField(null=True, blank=True, verbose_name="Total Height (mm)")
    labels_across = models.IntegerField(null=True, blank=True,default=1, verbose_name="Labels Across")
    label_width = models.FloatField(null=True, blank=True,verbose_name="Label Width (mm)")
    label_height = models.FloatField(null=True, blank=True,verbose_name="Label Height (mm)")
    gap_left = models.FloatField(null=True, blank=True, verbose_name="Left Gap (mm)")
    gap_right = models.FloatField(null=True, blank=True, verbose_name="Right Gap (mm)")
    gap_top = models.FloatField(null=True, blank=True, verbose_name="Top Gap (mm)")
    gap_bottom = models.FloatField(null=True, blank=True, verbose_name="Bottom Gap (mm)")

    # Rounded Corner Options
    round_top_left = models.FloatField(null=True, blank=True, verbose_name="Top-Left Corner Radius (mm)")
    round_top_right = models.FloatField(null=True, blank=True, verbose_name="Top-Right Corner Radius (mm)")
    round_bottom_left = models.FloatField(null=True, blank=True, verbose_name="Bottom-Left Corner Radius (mm)")
    round_bottom_right = models.FloatField(null=True, blank=True, verbose_name="Bottom-Right Corner Radius (mm)")
    is_default = models.BooleanField(default=False)
    is_billing = models.BooleanField(default=False)
    is_billing_default = models.BooleanField(default=False)

    def __str__(self):
        return self.name
