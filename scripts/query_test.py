from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from CONSTRUCTION_PROJECT.settings.construction_project_tags import *
from django.core import serializers
import json
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.views.generic import (
    TemplateView,
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.contrib import messages
from django.views import generic

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
from django.core.mail import EmailMessage

from Accounts.forms import (
    SendMailForm,
    ChartForm,
    ExpenditureForm,
    ContractorTypeForm,
    ContractorForm,
    ItemCodeForm,
    ItemForm,
    ContractorBillForm,
    ShareholderDepositForm,
    ShareholderForm,
)
import plotly.express as px
from Accounts.models import (
    Item,
    ItemCode,
    Shareholder,
    ShareholderDeposit,
    Expenditure,
    ContractorType,
    Contractor,
    ContractorBill,
    ShareholderDeposit,
    Shareholder,
)


def run():
    qs = Expenditure.objects.all()
    subquery_sum = (
        Expenditure.objects.filter(item_id=OuterRef("item__id"), item__ItemCode=OuterRef("item__ItemCode__id"))
        .values(
            "item__ItemCode__workSector",
            "item__itemName",
        )
        .annotate(
            sum_amount=Round(Sum(F("amount")), 0),
            sum_quantity=Round(Sum(F("quantity")), 0),
            units=F("item__unit"),
        )
    )

    qs = qs.annotate(

        work_sector=Subquery(subquery_sum.values("item__ItemCode__workSector")),
        item_name=Subquery(subquery_sum.values("item__itemName")),
        sum_amount=Subquery(subquery_sum.values("sum_amount")),
        sum_quantity=Subquery(subquery_sum.values("sum_quantity")),
        units=Subquery(subquery_sum.values("units")),
    )
    subquery_work_sector_sum = (
        Expenditure.objects.filter(
            item__ItemCode__workSector=OuterRef("item__ItemCode__workSector")
        )
        .values("item__ItemCode__workSector")
        .annotate(
            worksector_sum=Coalesce(Sum(F("amount")), 0, output_field=DecimalField())
        )
    )
    qs = qs.annotate(
        worksector_sum=Subquery(subquery_work_sector_sum.values("worksector_sum")),
    ).order_by("work_sector", "item_name", "-dateOfTransaction")
    print(qs.query)

    print(qs[0])
