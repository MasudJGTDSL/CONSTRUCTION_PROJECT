from django.db import models

# Create your models here.

class ItemCode(models.Model):
    workSector = models.CharField(max_length=100, blank=False, null=False)

    class Meta:
        ordering = ('workSector',)

    def __str__(self):
        return self.workSector
 

class Item(models.Model):
    itemName = models.CharField(max_length=100, blank=False, null=False)
    unit = models.CharField(max_length=20, blank=False, null=False)
    ItemCode = models.ForeignKey(ItemCode, blank=False, null=False, on_delete=models.CASCADE)
        
