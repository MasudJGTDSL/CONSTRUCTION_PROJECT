from django import forms
from .models import Shareholder, Expenditure


class ExpenditureForm(forms.ModelForm):
    class Meta:
        model = Expenditure
        fields = (
            "dateOfTransaction",
            "item",
            "description",
            "unit",
            "quantity",
            "rate",
            "amount",
            "voucherNo",
            "remarks",
        )

        widgets = {
            "dateOfTransaction": forms.DateInput(
                format=("%Y-%m-%d"),
                attrs={"class": "", "placeholder": "Select Date", "type": "date"},
            ),
        }
        labels = {
            # 'FDRNoJG':'FDR Number (JG):',
            "dateOfTransaction": "Transaction Date:",
            # 'FDRAccount':'FDR Account:',
            "item": "Item:",
            "description": "Description:",
            "unit": "Unit:",
            # 'AcFrom':'Account Code From:',
            "quantity": "quantity:",
            "rate": "Rate:",
            "amount": "Amount:",
            "voucherNo": "Voucher No:",
            "remarks": "Remarks:",
        }


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

    # def __init__(self, *args, **kwargs):
    #     super(SendMailForm, self).__init__(*args, **kwargs)  # populates the post
    #     qs = Shareholder.objects.values_list("email")
    #     print(qs)
    #     self.fields["email_id"].queryset = qs


class ChartForm(forms.Form):
    start = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))
    end = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))
