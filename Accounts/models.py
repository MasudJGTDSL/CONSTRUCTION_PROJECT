from django.db import models
from datetime import date, datetime, time, timedelta
from . import choices

# Create your models here.


class ItemCode(models.Model):
    workSector = models.CharField(max_length=100, blank=False, null=False)

    class Meta:
        ordering = ("workSector",)

    def __str__(self):
        return self.workSector


class Item(models.Model):
    itemName = models.CharField(max_length=100, blank=False, null=False)
    unit = models.CharField(max_length=20, blank=False, null=False)
    ItemCode = models.ForeignKey(
        ItemCode,
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name="ItemCode",
    )

    class Meta:
        ordering = ("itemName",)

    def __str__(self):
        return self.itemName


class Shareholder(models.Model):
    shareholderName = models.CharField(max_length=100)
    numberOfFlat = models.DecimalField(max_digits=4, decimal_places=2)

    class Meta:
        ordering = ("-numberOfFlat",)

    def __str__(self):
        return self.shareholderName


class Contractor(models.Model):
    contractor = models.CharField(max_length=100, blank=False, null=False)
    contractorType = models.CharField(
        max_length=3,
        blank=False,
        null=False,
        choices=choices.ContractorType,
        default="OTH",
    )
    address = models.TextField(blank=True, null=True)
    image = models.ImageField(blank=True, null=True, upload_to="media")

    class Meta:
        ordering = ("contractor",)

    def __str__(self):
        return self.contractor


class Expenditure(models.Model):
    dateOfTransaction = models.DateField(default=datetime.now)
    item = models.ForeignKey(
        Item,
        blank=False,
        null=False,
        related_name="Expenditure",
        on_delete=models.CASCADE,
    )
    description = models.TextField(blank=True, null=True)
    unit = models.CharField(max_length=100, blank=False, null=False, default="LS")
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    voucherNo = models.CharField(max_length=100, blank=False, null=False, default="")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    remarks = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ("-dateOfTransaction",)

    def __str__(self):
        return f"{self.item}, Quantity:{self.quantity}{self.unit}, Ampunt:{self.amount}"


class ShareholderDeposit(models.Model):
    dateOfTransaction = models.DateField(default=datetime.now)
    modeOfDeposit = models.CharField(
        max_length=4,
        blank=False,
        null=False,
        choices=choices.modeOfDeposit,
        default="OTHE",
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    remarks = models.TextField(blank=True, null=True)
    shareholder = models.ForeignKey(
        Shareholder,
        blank=False,
        null=False,
        related_name="ShareholderDeposit",
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering = ("-dateOfTransaction",)

    def __str__(self):
        return f"{self.shareholder}, Quantity:{self.amount}, Ampunt:{self.dateOfTransaction}"

    class ContractorBill(models.Model):
        dateOfTransaction = models.DateField(default=datetime.now)
        amount = models.DecimalField(max_digits=10, decimal_places=2)
        remarks = models.TextField(blank=True, null=True)
        contractor = models.ForeignKey(
            Contractor,
            blank=False,
            null=False,
            related_name="ContractorBill",
            on_delete=models.CASCADE,
        )

        def __str__(self):
            return f"{self.contractor}, Quantity:{self.amount}, Ampunt:{self.dateOfTransaction}"


class OfficeItemCode(models.Model):
    Sector = models.CharField(max_length=100, blank=False, null=False)

    class Meta:
        ordering = ("Sector",)

    def __str__(self):
        return self.Sector


class OfficeItem(models.Model):
    itemName = models.CharField(max_length=100, blank=False, null=False)
    unit = models.CharField(max_length=20, blank=False, null=False)
    officeitem = models.ForeignKey(
        OfficeItemCode,
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name="officeitem",
    )

    class Meta:
        ordering = ("itemName",)

    def __str__(self):
        return self.itemName


class OfficeExpenditure(models.Model):
    dateOfTransaction = models.DateField(default=datetime.now)
    item = models.ForeignKey(
        Item,
        blank=False,
        null=False,
        related_name="office_expenditure",
        on_delete=models.CASCADE,
    )
    description = models.TextField(blank=True, null=True)
    unit = models.CharField(max_length=100, blank=False, null=False, default="LS")
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    voucherNo = models.CharField(max_length=100, blank=False, null=False, default="")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    remarks = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ("-dateOfTransaction",)

    def __str__(self):
        return f"{self.item}, Quantity:{self.quantity}{self.unit}, Ampunt:{self.amount}"


class UserLoggedinRecord(models.Model):
    visitorIP = models.CharField("visitorIP", max_length=200, blank=True, null=True)
    # ip_address = models.CharField("visitorIP",max_length=200, blank=True, null=True)
    country = models.CharField(max_length=200, blank=True, null=True)
    country_code = models.CharField(max_length=200, blank=True, null=True)
    continent = models.CharField(max_length=200, blank=True, null=True)
    continent_code = models.CharField(max_length=200, blank=True, null=True)
    city = models.CharField(max_length=200, blank=True, null=True)
    county = models.CharField(max_length=200, blank=True, null=True)
    region = models.CharField(max_length=200, blank=True, null=True)
    region_code = models.CharField(max_length=200, blank=True, null=True)
    timezone = models.CharField(max_length=200, blank=True, null=True)
    owner = models.CharField(max_length=200, blank=True, null=True)
    longitude = models.CharField(max_length=200, blank=True, null=True)
    latitude = models.CharField(max_length=200, blank=True, null=True)
    currency = models.CharField(max_length=200, blank=True, null=True)
    languages = models.CharField(max_length=200, blank=True, null=True)
    visitCount = models.IntegerField("Visitor Count", default=0, blank=True, null=True)
    visitDateTime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.visitorIP
    

class UserLoggedinFailed(models.Model):
    visitorIP = models.CharField("visitorIP", max_length=200, blank=True, null=True)
    # ip_address = models.CharField("visitorIP",max_length=200, blank=True, null=True)
    country = models.CharField(max_length=200, blank=True, null=True)
    country_code = models.CharField(max_length=200, blank=True, null=True)
    continent = models.CharField(max_length=200, blank=True, null=True)
    continent_code = models.CharField(max_length=200, blank=True, null=True)
    city = models.CharField(max_length=200, blank=True, null=True)
    county = models.CharField(max_length=200, blank=True, null=True)
    region = models.CharField(max_length=200, blank=True, null=True)
    region_code = models.CharField(max_length=200, blank=True, null=True)
    timezone = models.CharField(max_length=200, blank=True, null=True)
    owner = models.CharField(max_length=200, blank=True, null=True)
    longitude = models.CharField(max_length=200, blank=True, null=True)
    latitude = models.CharField(max_length=200, blank=True, null=True)
    currency = models.CharField(max_length=200, blank=True, null=True)
    languages = models.CharField(max_length=200, blank=True, null=True)
    visitCount = models.IntegerField("Visitor Count", default=0, blank=True, null=True)
    user = models.CharField(max_length=200, default="")
    password = models.CharField(max_length=200, default="")
    visitDateTime = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.visitorIP
