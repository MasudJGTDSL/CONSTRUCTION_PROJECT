from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from django.core.mail import EmailMessage
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
from django.http import HttpResponse, HttpResponseRedirect
from django.template.response import TemplateResponse
from django.urls import reverse
from django.template.loader import render_to_string
from weasyprint import HTML, CSS
import tempfile
from dateutil.relativedelta import relativedelta
import calendar
from .models import *
from CONSTRUCTION_PROJECT.settings.context_processors import company_info_settings

company_info = company_info_settings("request")


@login_required
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
    data = data | company_info
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


@login_required
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
    data = data | company_info
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


@login_required
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
        data = data | company_info
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


@login_required
def expenditureDetailsReport(request):
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = (
        "inline; attachment; filename=expenditureDetailsReport"
        + str(datetime.now().strftime("%Y%m%d"))
        + ".pdf"
    )
    response["Content-Transfer-Encoding"] = "binary"

    # For Data -------------
    from_date = request.GET.get("fromdate")
    to_date = request.GET.get("todate")

    qs = Expenditure.objects.select_related("item__ItemCode").all()
    if from_date:
        qs = qs.filter(dateOfTransaction__gte=from_date)

    if to_date:
        qs = qs.filter(dateOfTransaction__lte=to_date)

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
        qs.filter(item__ItemCode__workSector=OuterRef("item__ItemCode__workSector"))
        .values("item__ItemCode__workSector")
        .annotate(
            worksector_sum=Coalesce(Sum(F("amount")), 0, output_field=DecimalField())
        )
    )

    if from_date or to_date:
        qs = qs.annotate(
            worksector_sum=Subquery(subquery_work_sector_sum.values("worksector_sum")),
        ).order_by("work_sector", "dateOfTransaction")
    else:
        qs = qs.annotate(
            worksector_sum=Subquery(subquery_work_sector_sum.values("worksector_sum")),
        ).order_by("work_sector", "item_name", "-dateOfTransaction")

    #! --------------------------------------
    data = {}
    data = data | {"expenditure": qs}
    data = data | company_info

    if from_date:
        data["fromdate"] = datetime.strptime(from_date, "%Y-%m-%d")
    if to_date:
        data["todate"] = datetime.strptime(to_date, "%Y-%m-%d")

    grand_total = qs.aggregate(Sum("amount"))
    data["grand_total"] = grand_total
    # For Data End -------------
    if request.path == reverse("Accounts:dateRangeExpenditureReport"):
        template = "accounts/reports/date_range_expenditure_details.html"
    else:
        template = "accounts/reports/expenditure_details.html"

    html_string = render_to_string(template, {"data": data})
    html = HTML(string=html_string, base_url=request.build_absolute_uri())

    resultfile = html.write_pdf()

    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(resultfile)
        output.flush()
        output.seek(0)
        response.write(output.read())
    return response


@login_required
def shareholderListReport(request):
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = (
        "inline; attachment; filename=shareholder_list"
        + str(datetime.now().strftime("%Y%m%d"))
        + ".pdf"
    )
    response["Content-Transfer-Encoding"] = "binary"

    # For Data -------------
    qs = Shareholder.objects.all()

    subquery_sum = (
        ShareholderDeposit.objects.filter(
            shareholder_id=OuterRef("id"),
        )
        .values(
            "shareholder__id",
        )
        .annotate(
            sum_amount=Round(Sum(F("amount")), 0),
        )
    )

    qs = qs.annotate(
        sum_amount=Subquery(subquery_sum.values("sum_amount")),
    ).order_by("id")

    targeted_amount = TargetedAmount.objects.values_list("amount").order_by(
        "-inputDate"
    )[0]

    #! --------------------------------------
    data = {}
    data = data | {"shareholder": qs}
    data = data | {"heading": "Shareholders List"}
    data = data | company_info
    data["targeted_amount_per_flat"] = (
        targeted_amount[0] / company_info["no_of_flat_per_share"]
    )
    data["heading"] = "Shareholders List"
    grand_total = ShareholderDeposit.objects.aggregate(Sum("amount"))
    data["grand_total"] = grand_total
    # For Data End -------------

    html_string = render_to_string(
        "accounts/reports/shareholder_list.html", {"data": data}
    )
    html = HTML(string=html_string, base_url=request.build_absolute_uri())

    resultfile = html.write_pdf()

    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(resultfile)
        output.flush()
        output.seek(0)
        response.write(output.read())
    return response


# @login_required
# def shareholderDepositReport(request, shareholder):
#     response = HttpResponse(content_type="application/pdf")
#     response["Content-Disposition"] = (
#         "inline; attachment; filename=shareholder_list"
#         + str(datetime.now().strftime("%Y%m%d"))
#         + ".pdf"
#     )
#     response["Content-Transfer-Encoding"] = "binary"

#     # For Data -------------
#     qs = ShareholderDeposit.objects.filter(shareholder_id=shareholder)

#     subquery_deposit_amount_sum = (
#         Shareholder.objects.filter(id=OuterRef("shareholder_id"))
#         .values("id")
#         .annotate(
#             deposit_amount_sum=Coalesce(
#                 Sum(F("ShareholderDeposit__amount")), 0, output_field=DecimalField()
#             ),
#             shareholderName=F("shareholderName"),
#             numberOfFlat=F("numberOfFlat"),
#             image=F("image"),
#         )
#     )

#     qs = qs.annotate(
#         deposit_amount_sum=Subquery(
#             subquery_deposit_amount_sum.values("deposit_amount_sum"),
#         ),
#         shareholderName=Subquery(
#             subquery_deposit_amount_sum.values("shareholderName"),
#         ),
#         numberOfFlat=Subquery(
#             subquery_deposit_amount_sum.values("numberOfFlat"),
#         ),
#         image=Subquery(
#             subquery_deposit_amount_sum.values("image"),
#         ),
#     )

#     targeted_amount = TargetedAmount.objects.values_list("amount").order_by(
#         "-inputDate"
#     )[0]
#     #! --------------------------------------
#     data = {}
#     data = data | {"shareholder_deposit": qs}
#     data = data | {"heading": "Details information of Deposited amount:"}
#     data = data | company_info
#     data["targeted_amount_per_flat"] = (
#         targeted_amount[0] / company_info["no_of_flat_per_share"]
#     )
#     # For Data End -------------

#     html_string = render_to_string(
#         "accounts/reports/shareholder_deposit.html", {"data": data}
#     )
#     base_url=request.build_absolute_uri()
#     html = HTML(string=html_string, base_url=base_url)

#     resultfile = html.write_pdf()

#     with tempfile.NamedTemporaryFile(delete=True) as output:
#         output.write(resultfile)
#         output.flush()
#         output.seek(0)
#         response.write(output.read())
#     return response


@login_required
def pdfReport(request, filename, shareholder):
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = (
        "inline; attachment; filename="
        + filename
        + str(datetime.now().strftime("%Y%m%d"))
        + ".pdf"
    )
    response["Content-Transfer-Encoding"] = "binary"

    # For Data -------------
    qs = ShareholderDeposit.objects.filter(shareholder_id=shareholder)

    subquery_deposit_amount_sum = (
        Shareholder.objects.filter(id=OuterRef("shareholder_id"))
        .values("id")
        .annotate(
            deposit_amount_sum=Coalesce(
                Sum(F("ShareholderDeposit__amount")), 0, output_field=DecimalField()
            ),
            shareholderName=F("shareholderName"),
            numberOfFlat=F("numberOfFlat"),
            image=F("image"),
        )
    )

    qs = qs.annotate(
        deposit_amount_sum=Subquery(
            subquery_deposit_amount_sum.values("deposit_amount_sum"),
        ),
        shareholderName=Subquery(
            subquery_deposit_amount_sum.values("shareholderName"),
        ),
        numberOfFlat=Subquery(
            subquery_deposit_amount_sum.values("numberOfFlat"),
        ),
        image=Subquery(
            subquery_deposit_amount_sum.values("image"),
        ),
    )

    targeted_amount = TargetedAmount.objects.values_list("amount").order_by(
        "-inputDate"
    )[0]
    #! --------------------------------------
    data = {}
    data = data | {"shareholder_deposit": qs}
    data = data | {"heading": "Details information of Deposited amount:"}
    data = data | company_info
    data["targeted_amount_per_flat"] = (
        targeted_amount[0] / company_info["no_of_flat_per_share"]
    )
    # For Data End -------------

    html_string = render_to_string(
        "accounts/reports/shareholder_deposit.html", {"data": data}
    )
    base_url = request.build_absolute_uri()
    html = HTML(string=html_string, base_url=base_url)

    resultfile = html.write_pdf()
    return {"resultfile": resultfile, "response": response}


@login_required
def shareholderDepositReport(request, shareholder):
    resultfile = pdfReport(request, "Shareholder Deposit info", shareholder)

    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(resultfile["resultfile"])
        output.flush()
        output.seek(0)
        resultfile["response"].write(output.read())
    return resultfile["response"]


email_body_text = """Date: {}
To,
Mr. {}
Shareholder, AeroSky Tower
Bownia, Dhaka.

Dear Sir,
As-Salamu Alaikum,
We have accumulated your deposited amount upto the date mentioned above. If there are any errors in the account, we request you to kindly inform the management of Aerosky Tower for necessary corrections.

Thank you.

Sincerely,
Manager
Aerosky Tower
Bawnia, Turag, Dhaka."""

html_code = """
<ol>{}</ol>
        <div class="d-flex justify-container-between">
            <form class="row g-3 p-2">
                <div class="col-auto">
                    <input type="hidden" id="status_ok" name="status_ok" value=1 />
                </div>
                <div class="col-auto">
                <button type="submit" class="btn btn-sm btn-danger px-4 mt-0">Yes</button>
                </div>
            </form>
            <form class="row g-3 p-2">
                <div class="col-auto">
                <input type="hidden" name="status_cancel" value=2>
                <button type="submit" class="btn btn-sm btn-success mt-0">Cancel</button>
                </div>
            </form>
        </div>
"""


@login_required
def sendMailshareholderDepositReport(request):
    email_address_list_qs = (
        Shareholder.objects.exclude(email__isnull=True)
        .exclude(email__exact="")
        .values_list("shareholderName", "email", "id")
    )
    receipent_name_tupple_list = [
        (name, email, id) for name, email, id in email_address_list_qs
    ]

    if (
        request.GET.get("status_ok") == None
        and request.GET.get("status_cancel") == None
    ):
        y = ""
        for x in email_address_list_qs:
            y += "<li>" + x[0] + ": <span class='text-primary'>" + x[1] + "</span></li>"
        template_name = "template_response.html"
        heading = "Are you sure you want to send eMail to:"
        context = {
            "heading": heading,
            "html_code": html_code.format(y),
            # "img_file": "matir-bank.svg",
            # "scripts": scripts,
        }
        return TemplateResponse(request, template_name, context)

    if request.GET.get("status_cancel") == "2":
        return HttpResponseRedirect("/")

    subject = "AeroSky Tower shareholder's deposit information."
    from_mail = request.user.email
    to_cc = ""
    to_bcc = ""
    for x in receipent_name_tupple_list:
        try:
            attachedFile = pdfReport(request, "Shareholder Deposit info", int(x[2]))
            mail = EmailMessage(
                subject=subject,
                body=email_body_text.format(datetime.now().strftime("%d %B %Y"), x[0]),
                from_email=from_mail,
                to=[x[0], x[1]],
                bcc=[to_bcc],
                cc=[to_cc],
            )
            mail.attach(
                f'Deposit Information of {x[0]} {datetime.now().strftime("%Y-%m-%d")}.pdf',
                attachedFile["resultfile"],
                "application/pdf",
            )
            mail.send()
            # except Exception as ex:
        except ArithmeticError as aex:
            return HttpResponse("Invalid header found")
    receipent_list = ""
    for x in receipent_name_tupple_list:
        receipent_list += f"{x[0]}, "
    messages.success(request, f"Thank you.\nEmail sent to {receipent_list}.")
    return HttpResponseRedirect("/")
