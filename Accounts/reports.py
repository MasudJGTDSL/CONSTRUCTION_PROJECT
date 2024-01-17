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
