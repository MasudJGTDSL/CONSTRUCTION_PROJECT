from django import forms
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import calendar
from django.db.models import (
    Case,
    CharField,
    Count,
    DecimalField,
    DurationField,
    ExpressionWrapper,
    F,
    FloatField,
    IntegerField,
    OuterRef,
    Q,
    Subquery,
    Sum,
    Value,
    When,
)
from django.db.models.functions import Cast, Coalesce, Concat, Extract, Round, Trunc
from .models import (
    Shareholder,
    Expenditure,
    ContractorType,
    Contractor,
    ItemCode,
    Item,
    ContractorBillSubmission,
    ContractorBillPayment,
    ShareholderDeposit,
    TargetedAmount,
    CreditPurchase,
    CreditPurchasePayment,
    IncomeSector,
    IncomeItem,
    Income,
)
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Reset, HTML


class TargetedAmountForm(forms.ModelForm):
    class Meta:
        model = TargetedAmount
        fields = "__all__"
        labels = {
            "amount": "Targeted Amount:",
            "inputDate": "Date:",
        }

        widgets = {
            "dateOfJoin": forms.DateInput(
                format=("%Y-%m-%d"),
                attrs={"class": "", "placeholder": "Select Date", "type": "date"},
            ),
        }

    def __init__(self, *args, **kwargs):
        super(TargetedAmountForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.attrs["autocomplete"] = "off"
        self.helper.layout = Layout(
            Row(
                Column("inputDate", css_class="form-group col-2 me-2 mb-0"),
                Column("amount", css_class="form-group col-2 mb-0"),
                css_class="form-row",
            ),
            HTML("<div class='d-flex justify-content-end mb-1'>"),
            Submit("submit", "Submit", css_class="btn btn-success me-2 mb-0"),
            Reset("reset", "Reset", css_class="btn btn-danger me-0 mb-0"),
            HTML("</div>"),
        )


class ContractorTypeForm(forms.ModelForm):
    class Meta:
        model = ContractorType
        fields = "__all__"
        labels = {
            "contractorType": "Contractor Type:",
        }


class ItemCodeForm(forms.ModelForm):
    class Meta:
        model = ItemCode
        fields = "__all__"
        labels = {
            "workSector": "Work Sector:",
        }


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = "__all__"
        labels = {
            "ItemCode": "Item Code:",
            "itemName": "Item Name:",
            "unit": "Unit:",
        }

    def __init__(self, *args, **kwargs):
        super(ItemForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.attrs["autocomplete"] = "off"
        self.helper.layout = Layout(
            Row(
                Column("ItemCode", css_class="form-group col-4 me-5 mb-0"),
                Column("itemName", css_class="form-group col-5 me-4 mb-0"),
                Column("unit", css_class="form-group col me-4  mb-0"),
                css_class="form-row",
            ),
            HTML("<div class='d-flex justify-content-end mb-1'>"),
            Submit("submit", "Submit", css_class="btn btn-success me-2 mb-0"),
            Reset("reset", "Reset", css_class="btn btn-danger me-0 mb-0"),
            HTML("</div>"),
        )


class ShareholderForm(forms.ModelForm):
    class Meta:
        model = Shareholder
        fields = "__all__"
        labels = {
            "dateOfJoin": "Date of Join:",
            "shareholderName": "Name:",
            "address": "Address:",
            "mobile": "Mobile:",
            "email": "Email:",
            "nid": "NID:",
            "numberOfFlat": "Nos. of Flat:",
            "image": "Shareholder's Photo:",
        }
        widgets = {
            "dateOfJoin": forms.DateInput(
                format=("%Y-%m-%d"),
                attrs={"class": "", "placeholder": "Select Date", "type": "date"},
            ),
        }

    def __init__(self, *args, **kwargs):
        super(ShareholderForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.attrs["autocomplete"] = "off"
        self.helper.layout = Layout(
            Row(
                Column("dateOfJoin", css_class="form-group col-2 me-2 mb-0"),
                Column("shareholderName", css_class="form-group col-2 mb-0"),
                Column("address", css_class="form-group col ms-2 me-2 mb-0"),
                Column("mobile", css_class="form-group col-2 me-4 mb-0"),
                css_class="form-row",
            ),
            Row(
                Column("email", css_class="form-group col-2 me-2 mb-0"),
                Column("nid", css_class="form-group col-2 me-2 mb-0"),
                Column("numberOfFlat", css_class="form-group col-1 me-2 mb-0"),
                Column("image", css_class="form-group col me-4 mb-0"),
                css_class="form-row",
            ),
            HTML("<div class='d-flex justify-content-end mb-1' id ='button_div'>"),
            Submit("submit", "Submit", css_class="btn btn-success me-2 mb-0"),
            Reset("reset", "Reset", css_class="btn btn-danger me-0 mb-0"),
            HTML("</div>"),
        )


class ContractorForm(forms.ModelForm):
    class Meta:
        model = Contractor
        fields = "__all__"
        labels = {
            "dateOfJoin": "Date of Join:",
            "contractor": "Name of The Firm:",
            "contractorType": "Contractor Type:",
            "address": "Address:",
            "NID": "NID:",
            "TIN": "TIN:",
            "TelephoneNo": "Telephone No:",
            "Mobile": "Mobile:",
            "Email": "Email:",
            "image": "Photo:",
        }
        widgets = {
            "dateOfJoin": forms.DateInput(
                format=("%Y-%m-%d"),
                attrs={"class": "", "placeholder": "Select Date", "type": "date"},
            ),
            "address": forms.Textarea(attrs={"rows": 2, "cols": 15}),
        }


class ContractorBillSubmissionForm(forms.ModelForm):
    class Meta:
        model = ContractorBillSubmission
        fields = "__all__"
        labels = {
            "contractor": "Contractor:",
            "dateOfBillSubmission": "Date:",
            "description": "Description:",
            "amount": "Amount:",
            "remarks": "Remarks:",
        }
        widgets = {
            "dateOfBillSubmission": forms.DateInput(
                format=("%Y-%m-%d"),
                attrs={"class": "", "placeholder": "Select Date", "type": "date"},
            ),
            "remarks": forms.Textarea(attrs={"rows": 2, "cols": 15}),
        }

    def __init__(self, *args, **kwargs):
        super(ContractorBillSubmissionForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.fields["contractor"].queryset = Contractor.objects.filter(IsArchive=False)
        self.helper.form_method = "post"
        self.helper.attrs["autocomplete"] = "off"
        self.helper.layout = Layout(
            Row(
                Column("contractor", css_class="form-group col-3 me-4 mb-0"),
                Column(
                    "dateOfBillSubmission", css_class="form-group col-2 ms-3 me-2 mb-0"
                ),
                Column("description", css_class="form-group col ms-2 me-2 mb-0"),
                Column("amount", css_class="form-group col-1 ms-2 me-4 mb-0"),
                css_class="form-row",
            ),
            Row(
                Column("remarks", css_class="form-group col me-4 mb-0"),
                css_class="form-row",
            ),
            HTML("<div class='d-flex justify-content-end mb-1'>"),
            Submit("submit", "Submit", css_class="btn btn-success me-2 mb-0"),
            Reset("reset", "Reset", css_class="btn btn-danger me-0 mb-0"),
            HTML("</div>"),
        )


class ContractorBillPaymentModelForm(forms.ModelForm):
    class Meta:
        model = ContractorBillPayment
        fields = "__all__"
        labels = {
            "bill": "Bill:",
            "dateOfTransaction": "Date:",
            "amount": "Amount:",
            "labor_fooding": "Labor Fooding:",
            "voucherNo": "Voucher No:",
            "remarks": "Remarks:",
        }
        widgets = {
            "dateOfTransaction": forms.DateInput(
                format=("%Y-%m-%d"),
                attrs={"class": "", "placeholder": "Select Date", "type": "date"},
            ),
        }


class ContractorBillPaymentForm(ContractorBillPaymentModelForm):
    qrySetItem = Item.objects.only("itemName").filter(ItemCode_id=8).distinct()
    item = forms.ModelChoiceField(
        queryset=qrySetItem,
        label="Item:",
    )

    def __init__(self, *args, **kwargs):
        super(ContractorBillPaymentForm, self).__init__(*args, **kwargs)
        qs = ContractorBillSubmission.objects.values("id").annotate(
            sum_amount=Sum(F("bill_submission__amount")),
            amount=F("amount"),
        )
        query_set = ContractorBillSubmission.objects.filter(
            id__in=(
                qs.filter(amount__gt=Coalesce(F("sum_amount"), 0)).values_list("id")
            )
        )

        self.fields["bill"].queryset = query_set
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.attrs["autocomplete"] = "off"
        self.helper.layout = Layout(
            Row(
                Column("bill", css_class="form-group col-3 me-4 mb-0"),
                Column(
                    "dateOfTransaction", css_class="form-group col-2 ms-3 me-2 mb-0"
                ),
                Column("item", css_class="form-group col-1 ms-2 me-4 mb-0"),
                Column("amount", css_class="form-group col-1 ms-3 me-2 mb-0"),
                Column("labor_fooding", css_class="form-group col ms-2 me-4 mb-0"),
                css_class="form-row",
            ),
            Row(
                Column(
                    "voucherNo", css_class="form-group col-3 ms-2 ps-1 pe-3 me-4 mb-0"
                ),
                Column("remarks", css_class="form-group col ms-2 me-4 mb-0"),
                css_class="form-row",
            ),
            HTML("<div class='d-flex justify-content-end mb-1' id ='button_div'>"),
            Submit("submit", "Submit", css_class="btn btn-success me-2 mb-0"),
            Reset("reset", "Reset", css_class="btn btn-danger me-0 mb-0"),
            HTML("</div>"),
        )


class CreditPurchaseForm(forms.ModelForm):
    class Meta:
        model = CreditPurchase
        fields = "__all__"
        labels = {
            "dateOfPurchase": "Date",
            "seller ": "Seller:",
            "address ": "Address:",
            "description ": "Description:",
            "mobile ": "Mobile:",
            "email ": "Email:",
            "amount ": "Amount:",
            "remarks ": "Remarks:",
        }
        widgets = {
            "dateOfPurchase": forms.DateInput(
                format=("%Y-%m-%d"),
                attrs={"class": "", "placeholder": "Select Date", "type": "date"},
            ),
        }

    def __init__(self, *args, **kwargs):
        super(CreditPurchaseForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.attrs["autocomplete"] = "off"
        self.helper.layout = Layout(
            Row(
                Column("seller", css_class="form-group col-3 me-2 mb-0"),
                Column("address", css_class="form-group col-4 me-2 mb-0"),
                Column("mobile", css_class="form-group col-2 me-2 mb-0"),
                Column("email", css_class="form-group col me-4 mb-0"),
                css_class="form-row",
            ),
            Row(
                Column("dateOfPurchase", css_class="form-group col-2 me-2 mb-0"),
                Column("description", css_class="form-group col-3 me-2 mb-0"),
                Column("amount", css_class="form-group col-1 me-2 mb-0"),
                Column("remarks", css_class="form-group col me-4 mb-0"),
                css_class="form-row",
            ),
            HTML("<div class='d-flex justify-content-end mb-1'>"),
            Submit("submit", "Submit", css_class="btn btn-success me-2 mb-0"),
            Reset("reset", "Reset", css_class="btn btn-danger me-0 mb-0"),
            HTML("</div>"),
        )


class CreditPurchasePaymentForm(forms.ModelForm):
    QrySetItemCode = ItemCode.objects.only("workSector").distinct()
    ItemCode = forms.ModelChoiceField(
        queryset=QrySetItemCode, label="Work Sector:", required=False
    )

    class Meta:
        model = CreditPurchasePayment
        fields = "__all__"
        labels = {
            "seller": "Seller:",
            "dateOfTransaction": "Date:",
            "description": "Description:",
            "amount": "Amount:",
            "voucherNo": "Voucher:",
            "remarks": "Remarks:",
            "item": "Item",
        }
        widgets = {
            "dateOfTransaction": forms.DateInput(
                format=("%Y-%m-%d"),
                attrs={"class": "", "placeholder": "Select Date", "type": "date"},
            ),
        }

    def __init__(self, *args, **kwargs):
        super(CreditPurchasePaymentForm, self).__init__(*args, **kwargs)
        qs = CreditPurchase.objects.values("id").annotate(
            sum_amount=Sum(F("Seller__amount")),
            amount=F("amount"),
        )
        query_set = CreditPurchase.objects.filter(
            id__in=(
                qs.filter(amount__gt=Coalesce(F("sum_amount"), 0)).values_list("id")
            )
        )

        self.fields["seller"].queryset = query_set
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.attrs["autocomplete"] = "off"
        self.helper.layout = Layout(
            Row(
                Column("seller", css_class="form-group col-3 me-4 mb-0"),
                Column(
                    "dateOfTransaction", css_class="form-group col-2 ms-3 me-2 mb-0"
                ),
                Column("ItemCode", css_class="form-group col-2 ms-2 me-4 mb-0"),
                Column("item", css_class="form-group col ms-3 me-5 mb-0"),
                css_class="form-row",
            ),
            Row(
                Column("description", css_class="form-group col-3 me-3 pe-2 mb-0"),
                Column("amount", css_class="form-group col-1 ms-4 ps-3 pe-1 me-4 mb-0"),
                Column(
                    "voucherNo", css_class="form-group col-1 ms-2 ps-1 pe-3 me-2 mb-0"
                ),
                Column("remarks", css_class="form-group col ms-1 me-4 mb-0"),
                css_class="form-row",
            ),
            HTML("<div class='d-flex justify-content-end mb-1' id ='button_div'>"),
            Submit("submit", "Submit", css_class="btn btn-success me-2 mb-0"),
            Reset("reset", "Reset", css_class="btn btn-danger me-0 mb-0"),
            HTML("</div>"),
        )


class ExpenditureModelForm(forms.ModelForm):
    class Meta:
        model = Expenditure
        fields = [field.name for field in Expenditure._meta.get_fields()]

        widgets = {
            "dateOfTransaction": forms.DateInput(
                format=("%Y-%m-%d"),
                attrs={"class": "", "placeholder": "Select Date", "type": "date"},
            ),
            "remarks": forms.Textarea(attrs={"rows": 1, "cols": 8}),
        }
        labels = {
            "dateOfTransaction": "Date:",
            "item": "Item:",
            "description": "Description:",
            "unit": "Unit:",
            "quantity": "quantity:",
            "rate": "Rate:",
            "amount": "Amount:",
            "voucherNo": "Voucher No:",
            "remarks": "Remarks:",
        }


class ExpenditureForm(ExpenditureModelForm):
    QrySetItemCode = ItemCode.objects.only("workSector").distinct()
    ItemCode = forms.ModelChoiceField(
        queryset=QrySetItemCode, label="Work Sector:", required=False
    )

    def __init__(self, *args, **kwargs):
        super(ExpenditureForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.attrs["autocomplete"] = "off"
        self.helper.layout = Layout(
            Row(
                Column("dateOfTransaction", css_class="form-group col-2 me-2 mb-0"),
                Column("ItemCode", css_class="form-group col-2 me-4 mb-0"),
                Column("item", css_class="form-group col ms-2 me-5 mb-0"),
                css_class="form-row",
            ),
            Row(
                Column("description", css_class="form-group col-3 me-2  mb-0"),
                Column("unit", css_class="form-group col-1 me-2 ms-0  mb-0"),
                Column("quantity", css_class="form-group col-1 me-2 mb-0"),
                Column("rate", css_class="form-group col-1 me-2 mb-0"),
                Column("amount", css_class="form-group col-1 ms-0 me-2  mb-0"),
                Column("voucherNo", css_class="form-group col me-4 ms-0  mb-0"),
                # Column("remarks", css_class="form-group col me-4 mb-0"),
                css_class="form-row",
            ),
            Row(
                Column("remarks", css_class="form-group col me-4 mb-0"),
                css_class="form-row",
            ),
            HTML("<div class='d-flex justify-content-end mb-1' id='button_div'>"),
            Submit("submit", "Submit", css_class="btn btn-success me-2 mb-0"),
            Reset("reset", "Reset", css_class="btn btn-danger me-0 mb-0"),
            HTML("</div>"),
        )


class SendMailForm(forms.Form):
    email_id = forms.CharField(required=False)
    email_cc = forms.EmailField(required=False)
    email_bcc = forms.EmailField(required=False)
    subject = forms.CharField(
        max_length=200,
        help_text="<code class='text-muted'>You Must have a subject.</code>",
    )
    msg = forms.CharField(widget=forms.Textarea, required=False)
    attachment = forms.FileField(required=False)


class ChartForm(forms.Form):
    start = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))
    end = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))


class ShareholderDepositForm(forms.ModelForm):
    class Meta:
        model = ShareholderDeposit
        fields = "__all__"
        labels = {
            "shareholder": "Shareholder:",
            "dateOfTransaction": "Date:",
            "modeOfDeposit": "Mode:",
            "amount": "Amount:",
            "remarks": "Remarks:",
        }
        widgets = {
            "dateOfTransaction": forms.DateInput(
                format=("%Y-%m-%d"),
                attrs={"class": "", "placeholder": "Select Date", "type": "date"},
            ),
            "remarks": forms.Textarea(attrs={"rows": 2, "cols": 15}),
        }

    def __init__(self, *args, **kwargs):
        super(ShareholderDepositForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.attrs["autocomplete"] = "off"
        self.helper.layout = Layout(
            Row(
                Column("shareholder", css_class="form-group col-3 me-4 mb-0"),
                Column(
                    "dateOfTransaction", css_class="form-group col-2 ms-3 me-2 mb-0"
                ),
                Column("modeOfDeposit", css_class="form-group col-1 ms-2 me-4 mb-0"),
                Column("amount", css_class="form-group col ms-3 me-4 mb-0"),
                css_class="form-row",
            ),
            Row(
                Column("remarks", css_class="form-group col me-4 mb-0"),
                css_class="form-row",
            ),
            HTML("<div class='d-flex justify-content-end mb-1' id='button_div'>"),
            Submit("submit", "Submit", css_class="btn btn-success me-2 mb-0"),
            Reset("reset", "Reset", css_class="btn btn-danger me-0 mb-0"),
            HTML("</div>"),
        )


class IncomeSectorForm(forms.ModelForm):
    class Meta:
        model = IncomeSector
        fields = "__all__"
        labels = {
            "incomeSector": "Income Sector:",
        }


class IncomeItemForm(forms.ModelForm):
    class Meta:
        model = IncomeItem
        fields = "__all__"
        labels = {
            "incomeSector": "Income Sector:",
            "itemName": "Item Name:",
            "unit": "Unit:",
        }

    def __init__(self, *args, **kwargs):
        super(IncomeItemForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.attrs["autocomplete"] = "off"
        self.helper.layout = Layout(
            Row(
                Column("incomeSector", css_class="form-group col-4 me-5 mb-0"),
                Column("itemName", css_class="form-group col-5 me-4 mb-0"),
                Column("unit", css_class="form-group col me-4  mb-0"),
                css_class="form-row",
            ),
            HTML("<div class='d-flex justify-content-end mb-1'>"),
            Submit("submit", "Submit", css_class="btn btn-success me-2 mb-0"),
            Reset("reset", "Reset", css_class="btn btn-danger me-0 mb-0"),
            HTML("</div>"),
        )


# TODO: ============================
class IncomeModelForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = [field.name for field in Income._meta.get_fields()]

        widgets = {
            "dateOfTransaction": forms.DateInput(
                format=("%Y-%m-%d"),
                attrs={"class": "", "placeholder": "Select Date", "type": "date"},
            ),
            "remarks": forms.Textarea(attrs={"rows": 1, "cols": 8}),
        }
        labels = {
            "dateOfTransaction": "Date:",
            "incomeItem": "Income Item:",
            "description": "Description:",
            "unit": "Unit:",
            "quantity": "quantity:",
            "rate": "Rate:",
            "amount": "Amount:",
            "voucherNo": "Voucher No:",
            "remarks": "Remarks:",
        }


class IncomeForm(IncomeModelForm):
    QrySetIncomeSector = IncomeSector.objects.only("incomeSector").distinct()
    incomeSector = forms.ModelChoiceField(
        queryset=QrySetIncomeSector, label="Income Sector:", required=False
    )

    def __init__(self, *args, **kwargs):
        super(IncomeForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.attrs["autocomplete"] = "off"
        self.helper.layout = Layout(
            Row(
                Column("dateOfTransaction", css_class="form-group col-2 me-2 mb-0"),
                Column("incomeSector", css_class="form-group col-2 me-4 mb-0"),
                Column("incomeItem", css_class="form-group col ms-2 me-5 mb-0"),
                css_class="form-row",
            ),
            Row(
                Column("description", css_class="form-group col-4 me-2  mb-0"),
                Column("unit", css_class="form-group col-1 me-2 ms-0  mb-0"),
                Column("quantity", css_class="form-group col-1 me-2 mb-0"),
                Column("rate", css_class="form-group col-1 me-2 mb-0"),
                Column("amount", css_class="form-group col-1 ms-0 me-2  mb-0"),
                Column("voucherNo", css_class="form-group col me-4 ms-0  mb-0"),
                # Column("remarks", css_class="form-group col me-4 mb-0"),
                css_class="form-row",
            ),
            Row(
                Column("remarks", css_class="form-group col me-4 mb-0"),
                css_class="form-row",
            ),
            HTML("<div class='d-flex justify-content-end mb-1' id='button_div'>"),
            Submit("submit", "Submit", css_class="btn btn-success me-2 mb-0"),
            Reset("reset", "Reset", css_class="btn btn-danger me-0 mb-0"),
            HTML("</div>"),
        )
