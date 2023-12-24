from django.core.validators import MaxValueValidator, MinValueValidator
import datetime

ContractorType = (
    ("CIV", "Civil"),
    ("ELE", "Electrical"),
    ("SAN", "Sanitary"),
    ("CAR", "Carpenter"),
    ("THA", "Thai and Glass"),
    ("PLU", "Plumber"),
    ("OTH", "Other"),
)


modeOfDeposit = (
    ("CASH", "Cash"),
    ("CHEQ", "Cheque"),
    ("OTHE", "Other"),
)

YesNo = (
    ("Y", "Yes"),
    ("N", "No"),
)


ActiveInactive = (
    ("A", "Active"),
    ("I", "Inactive"),
)


def current_year():
    return datetime.date.today().year


def max_value_current_year(value):
    return MaxValueValidator(current_year())(value)


# class MyModel(models.Model):
#     year = models.IntegerField(_('year'), validators=[
#                                MinValueValidator(2010), max_value_current_year])


# class MyForm(forms.ModelForm):
#     year = forms.TypedChoiceField(
#         coerce=int, choices=year_choices, initial=current_year)
