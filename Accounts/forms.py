from django import forms
from .models import (
    Shareholder,
    Expenditure,
    ContractorType,
    Contractor,
    ItemCode,
    Item,
    ContractorBill,
    ShareholderDeposit,
    TargetedAmount,
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
            "Email": "Email:",
            "nid": "NID:",
            "numberOfFlat": "Numbers of Flat:",
            "image": "Photo:",
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
                Column("address", css_class="form-group col ms-2 me-4 mb-0"),
                css_class="form-row",
            ),
            Row(
                Column("mobile", css_class="form-group col-1 me-2 mb-0"),
                Column("nid", css_class="form-group col-1 me-2 mb-0"),
                Column("numberOfFlat", css_class="form-group col-2 me-2 mb-0"),
                Column("image", css_class="form-group col me-4 mb-0"),
                css_class="form-row",
            ),
            HTML("<div class='d-flex justify-content-end mb-1'>"),
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


class ContractorBillForm(forms.ModelForm):
    class Meta:
        model = ContractorBill
        fields = "__all__"
        labels = {
            "contractor": "Contractor:",
            "dateOfTransaction": "Date:",
            "amount": "Amount:",
            "labor_fooding": "Labor Fooding:",
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
        super(ContractorBillForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.attrs["autocomplete"] = "off"
        self.helper.layout = Layout(
            Row(
                Column("contractor", css_class="form-group col-3 me-4 mb-0"),
                Column(
                    "dateOfTransaction", css_class="form-group col-2 ms-3 me-2 mb-0"
                ),
                Column("amount", css_class="form-group col-1 ms-2 me-2 mb-0"),
                Column("labor_fooding", css_class="form-group col ms-2 me-4 mb-0"),
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
        queryset=QrySetItemCode,
        label="Work Sector:",
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
            HTML("<div class='d-flex justify-content-end mb-1'>"),
            Submit("submit", "Submit", css_class="btn btn-success me-2 mb-0"),
            Reset("reset", "Reset", css_class="btn btn-danger me-0 mb-0"),
            HTML("</div>"),
        )


class SendMailForm(forms.Form):
    email_id = forms.EmailField()
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
            HTML("<div class='d-flex justify-content-end mb-1'>"),
            Submit("submit", "Submit", css_class="btn btn-success me-2 mb-0"),
            Reset("reset", "Reset", css_class="btn btn-danger me-0 mb-0"),
            HTML("</div>"),
        )
