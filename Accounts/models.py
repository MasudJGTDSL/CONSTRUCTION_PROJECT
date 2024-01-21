import os
from PIL import Image
from django.db import models
from datetime import date, datetime, time, timedelta
from . import choices
from uuid import uuid4

# from . import views
from django.urls import reverse
from .templatetags.mahimsoft_tags import intcomma_bd


def path_and_rename(instance, filename):
    upload_to = "ContractorsImage"
    ext = filename.split(".")[-1]
    # get filename
    if instance.pk:
        filename = "{}.{}".format(instance.pk, ext)
    else:
        # set filename as random string
        filename = "{}.{}".format(uuid4().hex, ext)
    # return the whole path to the file
    return os.path.join(upload_to, filename)


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
        ordering = (
            "ItemCode",
            "itemName",
        )

    def __str__(self):
        return f"{self.itemName} [Unit: {self.unit}]"


class ContractorType(models.Model):
    contractorType = models.CharField(
        max_length=100,
        blank=False,
        null=False,
    )

    def __str__(self):
        return self.contractorType


class Contractor(models.Model):
    dateOfJoin = models.DateField(default=datetime.now)
    contractor = models.CharField(max_length=100, blank=False, null=False)
    contractorType = models.ForeignKey(
        ContractorType,
        blank=False,
        null=False,
        related_name="Contr_Type",
        on_delete=models.CASCADE,
    )
    address = models.TextField(blank=True, null=True)
    NID = models.CharField(max_length=30, blank=True, null=True)
    TIN = models.CharField(max_length=50, blank=True, null=True)
    TelephoneNo = models.CharField(max_length=50, blank=True, null=True)
    Mobile = models.CharField(max_length=20, blank=True, null=True)
    Email = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(
        upload_to=path_and_rename,
        max_length=255,
        default="ContractorsImage/default.png",
        null=True,
        blank=True,
    )
    IsArchive = models.BooleanField(default=False)

    class Meta:
        ordering = ("contractor",)

    def save(self):
        super().save()
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

    def get_absolute_url(self):
        return f"/contractor/{str(self.id)}"

    def __str__(self):
        return self.contractor


class ContractorBillSubmission(models.Model):
    dateOfBillSubmission = models.DateField(default=datetime.now)
    description = models.CharField(max_length=200, blank=True, null=True, default="")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    remarks = models.TextField(blank=True, null=True)
    contractor = models.ForeignKey(
        Contractor,
        blank=False,
        null=False,
        related_name="contractor_bill",
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f"{self.contractor}, {self.description}, Bill No.{self.pk}, Bill Amount: {intcomma_bd(self.amount)}, Date: {self.dateOfBillSubmission.strftime('%d %b %Y')}"


class ContractorBillPayment(models.Model):
    dateOfTransaction = models.DateField(default=datetime.now)
    labor_fooding = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    voucherNo = models.CharField(max_length=100, blank=False, null=False, default="")
    remarks = models.CharField(max_length=200, blank=False, null=False, default="")
    bill = models.ForeignKey(
        ContractorBillSubmission,
        blank=False,
        null=False,
        related_name="bill_submission",
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f"{self.bill}, Paid Amount: {intcomma_bd(self.amount)}, Date: {self.dateOfTransaction.strftime('%d-%b-%Y')}"


class CreditPurchase(models.Model):
    dateOfPurchase = models.DateField(default=datetime.now)
    seller = models.CharField(max_length=150, blank=False, null=False, default="")
    address = models.CharField(max_length=250, blank=False, null=False, default="")
    description = models.CharField(max_length=250, blank=False, null=False, default="")
    mobile = models.CharField(max_length=20, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    remarks = models.CharField(max_length=250, blank=False, null=False, default="")

    class Meta:
        ordering = ("-dateOfPurchase",)

    def get_absolute_url(self):
        return f"/credit_purchase_update/{str(self.id)}"  #! Done Pending ==========

    def __str__(self):
        return f"{self.seller}, {self.description}, Date: {(self.dateOfPurchase).strftime('%d-%b-%Y')}, Amount: {intcomma_bd(self.amount)}"


class CreditPurchasePayment(models.Model):
    dateOfTransaction = models.DateField(default=datetime.now)
    seller = models.ForeignKey(
        CreditPurchase,
        blank=False,
        null=False,
        related_name="Seller",
        on_delete=models.CASCADE,
    )
    item = models.ForeignKey(
        Item,
        blank=False,
        null=False,
        related_name="Item",
        on_delete=models.CASCADE,
    )
    description = models.CharField(max_length=250, blank=False, null=False, default="")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    voucherNo = models.CharField(max_length=100, blank=False, null=False, default="")
    remarks = models.CharField(max_length=250, blank=False, null=False, default="")

    class Meta:
        ordering = ("-dateOfTransaction",)

    def get_absolute_url(self):
        return f"/credit_purchase_payment_update/{str(self.id)}"  #! Done Pending ==========

    def __str__(self):
        return f"{self.seller}, Date: {(self.dateOfTransaction).strftime('%d-%b-%Y')}, Amount: {intcomma_bd(self.amount)}"


class Expenditure(models.Model):
    dateOfTransaction = models.DateField(default=datetime.now)
    item = models.ForeignKey(
        Item,
        blank=False,
        null=False,
        related_name="Expenditure_Item",
        on_delete=models.CASCADE,
    )
    description = models.CharField(max_length=200, blank=True, null=True, default="")
    unit = models.CharField(max_length=100, blank=False, null=False, default="LS")
    rate = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    voucherNo = models.CharField(max_length=100, blank=False, null=False, default="")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    contractor_bill_payment = models.ForeignKey(
        ContractorBillPayment,
        blank=True,
        null=True,
        related_name="contractor_bill",
        on_delete=models.CASCADE,
    )
    credit_purchase_payment = models.ForeignKey(
        CreditPurchasePayment,
        blank=True,
        null=True,
        related_name="CreditPurchasePayment",
        on_delete=models.CASCADE,
    )
    remarks = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ("-dateOfTransaction",)

    def get_absolute_url(self):
        return f"/expenditure_update/{str(self.id)}"

    def __str__(self):
        return f"Date: {(self.dateOfTransaction).strftime('%d-%b-%Y')}, {self.description}, Sector: {self.item}, Quantity:{self.quantity} {self.unit}, Amount: {intcomma_bd(self.amount)}"


class Shareholder(models.Model):
    dateOfJoin = models.DateField(default=datetime.now)
    shareholderName = models.CharField("Name", max_length=100)
    address = models.CharField("Address", max_length=300, blank=True, null=True)
    email = models.EmailField("Email", max_length=300, blank=True, null=True)
    mobile = models.CharField("Mobile No.", max_length=20, blank=True, null=True)
    nid = models.CharField("NID No.", max_length=20, blank=True, null=True)
    numberOfFlat = models.DecimalField(
        "Number of Flats", max_digits=4, decimal_places=2
    )
    image = models.ImageField(
        upload_to="ShareholdersImage/",
        max_length=255,
        default="ShareholdersImage/default.png",
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ("-numberOfFlat",)

    def save(self):
        super().save()
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

    def get_absolute_url(self):
        return f"/shareholder/{str(self.id)}"

    def __str__(self):
        return self.shareholderName


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
        return f"{self.shareholder}: Amount:{intcomma_bd(self.amount)}, Date:{self.dateOfTransaction}"

    def get_absolute_url(self):
        return f"/get_shareholder_deposit_info/{str(self.shareholder)}"


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
        return f"{self.item}, Quantity:{self.quantity}{self.unit}, Amount:{intcomma_bd(self.amount)}"


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
    user = models.CharField(max_length=200, default="")
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


class TargetedAmount(models.Model):
    inputDate = models.DateField(default=datetime.now)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        ordering = ("-inputDate",)

    def __str__(self):
        return f"Targeted Amount: {intcomma_bd(self.amount)} | Date: {self.inputDate.strftime('%d %b %Y')}"
