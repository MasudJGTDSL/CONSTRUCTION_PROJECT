from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.views.generic import (
    TemplateView,
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
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

from Accounts.forms import SendMailForm, ChartForm
import plotly.express as px
from Accounts.models import Item, ItemCode, Shareholder, ShareholderDeposit, Expenditure

# ANSI Color Code
RESET = "\033[0m"
BLACK = "\033[30m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
WHITE = "\033[37m"

# Background colors:
BG_BLACK = "\033[40m"
BG_RED = "\033[41m"
BG_GREEN = "\033[42m"
BG_YELLOW = "\033[43m"
BG_BLUE = "\033[44m"
BG_MAGENTA = "\033[45m"
BG_CYAN = "\033[46m"
BG_WHITE = "\033[47m"

# Text formatting:
TXT_BOLD = "\033[1m"
# Dim: \033[2m
# Underline: \033[4m
# Blink: \033[5m
# Reverse: \033[7m
# Hidden: \033[8m

# company_info = company_info_settings("request")

# py manage.py runscript from_gpt


def index(request):
    return render(request, "accounts/dashboard.html", {"data": "This is Data"})


# py manage.py runscript test
def send_mail(request):
    qs = Shareholder.objects.aggregate(nos_of_shareholders=Count("id"))
    if request.method == "POST":
        fm = SendMailForm(request.POST or None, request.FILES or None)
        if fm.is_valid():
            subject = fm.cleaned_data["subject"]
            message = fm.cleaned_data["msg"]
            from_mail = request.user.email
            print(from_mail)
            to_mail = fm.cleaned_data["email_id"]
            to_cc = fm.cleaned_data["email_cc"]
            to_bcc = fm.cleaned_data["email_bcc"]
            print(fm.cleaned_data)
            attach = fm.cleaned_data["attachment"]
            if from_mail and to_mail:
                try:
                    mail = EmailMessage(
                        subject=subject,
                        body=message,
                        from_email=from_mail,
                        to=[to_mail],
                        bcc=[to_bcc],
                        cc=[to_cc],
                    )
                    mail.attach(attach.name, attach.read(), attach.content_type)
                    mail.send()
                # except Exception as ex:
                except ArithmeticError as aex:
                    print(aex.args)
                    return HttpResponse("Invalid header found")
                return HttpResponseRedirect("/mail/thanks/")
            else:
                return HttpResponse("Make sure all fields are entered and valid.")
    else:
        fm = SendMailForm()
    return render(request, "accounts/send_mail.html", {"fm": fm, "qs": qs})


def chart():
    qs1 = ShareholderDeposit.objects.values("shareholder__shareholderName").annotate(
        Deposited_Amount=Sum(Coalesce(F("amount"), 0, output_field=FloatField()))
    )

    qs = qs1.annotate(
        Shareholder=F("shareholder__shareholderName"), Amount=F("Deposited_Amount")
    )

    fig = px.bar(
        x=[c["Shareholder"] for c in qs],
        y=[c["Amount"] for c in qs],
        text=[f"{(amnt/10**5):,.2f}Lac" for amnt in [c["Amount"] for c in qs]],
        title="Amount Deposited Per Flat",
        labels={"x": "Share Holders", "y": "Amount Taka"},
    )

    qs_avg = ShareholderDeposit.objects.values("shareholder__shareholderName").annotate(
        Deposited_Amount=ExpressionWrapper(
            Sum(Coalesce(F("amount"), 0, output_field=FloatField()))
            / F("shareholder__numberOfFlat"),
            output_field=FloatField(),
        )
    )

    x_avg = qs_avg.values_list("shareholder__shareholderName", flat=True)
    y_avg = qs_avg.values_list("Deposited_Amount", flat=True)
    text_avg = [f"{(amnt/10**3):,.2f}K" for amnt in y_avg]

    fig_avg = px.bar(
        x=x_avg,
        y=y_avg,
        # text=text_avg,
        text_auto=".2s",
        title="Amount Deposited",
        labels={"x": "Share Holders", "y": "Average Amount per Flat"},
        color=y_avg,
        # color_discrete_map = ['gold', 'mediumturquoise', 'darkorange', 'lightgreen']
        color_discrete_map={
            "Thur": "lightcyan",
            "Fahim Amin": "cyan",
            "Sat": "royalblue",
            "Sun": "darkblue",
        },
    )

    fig = px.pie(
        qs,
        values="Amount",
        names="Shareholder",
        title="Amount Deposited",
        #  color_discrete_sequence=px.colors.sequential.RdBu
    )

    fig.update_traces(textposition="outside")
    fig.update_layout(title={"font_size": 24, "xanchor": "center", "x": 0.5})
    chart = fig.to_html()

    fig_avg.update_layout(title={"font_size": 24, "xanchor": "center", "x": 0.5})
    chart_avg = fig_avg.to_html()

    context = {"chart": chart, "chart_avg": chart_avg, "qs": qs}
    return context


def expenditure():
    qs = (
        Expenditure.objects.select_related("item")
        .select_related("item__ItemCode")
        .all()
    )
    subquery_item_sum = (
        Expenditure.objects.values("item__ItemCode__workSector", "item__itemName")
        .filter(item=OuterRef("item__id"))
        .annotate(
            item_sum=Sum(F("amount")),
            quantity_sum=Sum(F("quantity")),
        )
    )
    subquery_work_sector_sum = (
        Expenditure.objects.values("item__ItemCode__workSector")
        .filter(item__ItemCode=OuterRef("item__ItemCode__id"))
        .annotate(
            work_sector_sum=Sum(F("amount")),
        )
    )
    qs = qs.annotate(
        item_sum=Subquery(subquery_item_sum.values("item_sum")),
        quantity_sum=Subquery(subquery_item_sum.values("quantity_sum")),
        worksector_sum=Subquery(subquery_work_sector_sum.values("work_sector_sum")),
    ).order_by("item__ItemCode", "item", "-dateOfTransaction")

    return {"qs": qs}


def run():
    query_set = expenditure()["qs"]

    print("My Print", (" \u26BD\uFE0B ").join("\U0001F3F5" * 15))

    print(
        f"\033[38;5;208m {BG_YELLOW}{TXT_BOLD}\033[2:4m Returned Data 📜 :\
            {RESET}\033[2;30m {query_set}"
    )
    print((" 👁️ 👀 ").join("\U0001F3F5" * 10))
    # print('amount_before_maturity: ', amount_before_maturity)

    print(
        f'\033[38;5;208m {BG_YELLOW}{TXT_BOLD} Query 📜 :{RESET}\033[2;30m \
            {str(query_set.query).replace(chr(34), "`").replace("CAST(","").replace("AS NUMERIC)","")}\n \u26BD\uFE0B No. of Record: {query_set.count()}\n'
    )
