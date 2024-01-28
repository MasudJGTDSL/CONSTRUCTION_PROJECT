from datetime import datetime
from django.utils import timezone
from django.db.models import (
    F,
    Sum,
    Count,
    Q,
    Case,
    When,
    Value,
    ExpressionWrapper,
    Func,
    DateTimeField,
    DateField,
    IntegerField,
    CharField,
    DecimalField,
    Subquery,
    OuterRef,
    DurationField,
    FloatField,
)
from django.db.models.functions import Cast, Round, Concat, Coalesce, Extract, Trunc
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML, CSS
import tempfile
from dateutil.relativedelta import relativedelta
import calendar
from .models import *
from CONSTRUCTION_PROJECT.settings.context_processors import company_info_settings


def contractorDetails(request, pk):
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = (
        "inline; attachment; filename=contractorReport"
        + str(datetime.now().strftime("%Y%m%d"))
        + ".pdf"
    )
    response["Content-Transfer-Encoding"] = "binary"
    # For Data -------------
    contractor_table = Contractor.objects.values(
        "dateOfJoin",
        "contractor",
        "contractorType__contractorType",
        "address",
        "NID",
        "TIN",
        "TelephoneNo",
        "Mobile",
        "Email",
        "image",
    ).get(id=pk)

    data = {}
    data = data | contractor_table
    data = data | company_info_settings(request)
    # For Data End -------------
    html_string = render_to_string(
        "accounts/reports/contractor_details.html", {"data": data}
    )
    html = HTML(string=html_string, base_url=request.build_absolute_uri())

    resultfile = html.write_pdf()

    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(resultfile)
        output.flush()
        output.seek(0)
        response.write(output.read())
    return response


def shareholderDetails(request, pk):
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = (
        "inline; attachment; filename=contractorReport"
        + str(datetime.now().strftime("%Y%m%d"))
        + ".pdf"
    )
    response["Content-Transfer-Encoding"] = "binary"
    # For Data -------------
    shareholder_table = Shareholder.objects.values().get(id=pk)

    data = {}
    data = data | shareholder_table
    data = data | company_info_settings(request)
    # For Data End -------------
    html_string = render_to_string(
        "accounts/reports/shareholder_details.html", {"data": data}
    )
    html = HTML(string=html_string, base_url=request.build_absolute_uri())

    resultfile = html.write_pdf()

    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(resultfile)
        output.flush()
        output.seek(0)
        response.write(output.read())
    return response


def expenditureSummaryReport(request):
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = (
        "inline; attachment; filename=expenditureSummaryReport"
        + str(datetime.now().strftime("%Y%m%d"))
        + ".pdf"
    )
    response["Content-Transfer-Encoding"] = "binary"

    # For Data -------------
    def get_queryset():
        qs = Expenditure.objects.values(
            "item__ItemCode__workSector",
            "item__itemName",
        ).annotate(
            sum_amount=Round(Sum(F("amount")), 0),
            sum_quantity=Round(Sum(F("quantity")), 0),
            unit=F("item__unit"),
        )
        subquery_work_sector_sum = (
            Expenditure.objects.filter(
                item__ItemCode__workSector=OuterRef("item__ItemCode__workSector")
            )
            .values("item__ItemCode__workSector")
            .annotate(
                worksector_sum=Coalesce(
                    Sum(F("amount")), 0, output_field=DecimalField()
                )
            )
        )
        qs = qs.annotate(
            worksector_sum=Subquery(subquery_work_sector_sum.values("worksector_sum")),
        )
        data = {}
        data = data | {"expenditure": qs}
        data = data | company_info_settings(request)
        grand_total = Expenditure.objects.aggregate(Sum("amount"))
        data["grand_total"] = grand_total
        return {"data": data}

    # For Data End -------------
    html_string = render_to_string(
        "accounts/reports/expenditure_summarized_list.html", get_queryset()
    )
    html = HTML(string=html_string, base_url=request.build_absolute_uri())

    resultfile = html.write_pdf()

    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(resultfile)
        output.flush()
        output.seek(0)
        response.write(output.read())
    return response


def expenditureDetailsReport(request):
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = (
        "inline; attachment; filename=expenditureDetailsReport"
        + str(datetime.now().strftime("%Y%m%d"))
        + ".pdf"
    )
    response["Content-Transfer-Encoding"] = "binary"

    # For Data -------------
    qs = Expenditure.objects.select_related("item__ItemCode").all()

    subquery_sum = (
        Expenditure.objects.filter(
            item_id=OuterRef("item__id"),
            item__ItemCode=OuterRef("item__ItemCode__id"),
        )
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

    #! --------------------------------------
    data = {}
    data = data | {"expenditure": qs}
    data = data | company_info_settings(request)
    grand_total = Expenditure.objects.aggregate(Sum("amount"))
    data["grand_total"] = grand_total
    # For Data End -------------

    html_string = render_to_string(
        "accounts/reports/expenditure_details_list.html", {"data": data}
    )
    html = HTML(string=html_string, base_url=request.build_absolute_uri())

    resultfile = html.write_pdf()

    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(resultfile)
        output.flush()
        output.seek(0)
        response.write(output.read())
    return response
