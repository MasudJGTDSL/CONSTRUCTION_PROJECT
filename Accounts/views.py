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

from .forms import SendMailForm, ChartForm, ExpenditureForm
import plotly.express as px
from .models import Item, ItemCode, Shareholder, ShareholderDeposit, Expenditure


class ExpenditureView(generic.edit.FormView):
    template_name = "accounts/expenditure_input.html"
    form_class = ExpenditureForm
    success_url = "/"
    # print(form)

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Thank you. We will be in touch soon.")
        return super().form_valid(form)

    

def index(request):
    # start = request.GET.get("start")
    # end = request.GET.get("end")

    qs_1 = ShareholderDeposit.objects.values("shareholder__shareholderName").annotate(
        Deposited_Amount=Sum(Coalesce(F("amount"), 0, output_field=FloatField()))
    )

    qs = qs_1.annotate(
        Shareholder=F("shareholder__shareholderName"), Amount=F("Deposited_Amount")
    )

    # if start:
    #     qs = Shareholder.filter(date__gte=start)
    # if end:
    #     qs = Shareholder.filter(date__lte=end)

    # fig = px.bar(
    #     x=[c["Shareholder"] for c in qs],
    #     y=[c["Amount"] for c in qs],
    #     text=[f"{(amnt/10**5):,.2f}Lac" for amnt in [c["Amount"] for c in qs]],
    #     title="Amount Deposited Per Flat",
    #     labels={"x": "Share Holders", "y": "Amount Taka"},
    # )

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
    # fig_avg = px.bar(
    #     x=x_avg,
    #     y=y_avg,
    #     text=text_avg,
    #     title="Amount Deposited",
    #     labels={"x": "Share Holders", "y": "Average Amount per Flat"},
    # )
    fig_avg = px.bar(
        x=x_avg,
        y=y_avg,
        # text=text_avg,
        text_auto=".2s",
        title="Amount Deposited",
        labels={"x": "Share Holders", "y": "Average Amount per Flat"},
        color=y_avg,
        range_y=[10000, 3000000],
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

    # fig_avg.title = "Amount Deposited"
    # fig_avg.labels = {"x": "Share Holders", "y": "Average Amount per Flat"}
    fig_avg.update_traces(textangle=-90, textposition="outside", cliponaxis=False)
    fig_avg.update_layout(
        title={"font_size": 24, "xanchor": "center", "x": 0.5}, barmode="group"
    )

    fig.update_traces(textinfo="label+percent", textposition="outside")
    fig.update_layout(
        showlegend=False, title={"font_size": 24, "xanchor": "auto", "x": 0.5}
    )

    chart = fig.to_html()
    chart_avg = fig_avg.to_html()

    context = {"chart": chart, "chart_avg": chart_avg}
    return render(request, "accounts/dashboard.html", context)


def send_mail(request):
    qs = Shareholder.objects.aggregate(nos_of_shareholders=Count("id"))
    qs1 = Shareholder.objects.values_list("email")
    email_list = ""
    for x in qs1:
        email_list +=f"{x[0]},"
        
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
                return HttpResponseRedirect("/")
            else:
                return HttpResponse("Make sure all fields are entered and valid.")
    else:
        fm = SendMailForm(initial={'email_id': email_list})
        # fm.initial
    return render(request, "accounts/send_mail.html", {"fm": fm, "qs": qs})


def chart(request):
    # start = request.GET.get("start")
    # end = request.GET.get("end")

    qs = ShareholderDeposit.objects.values("shareholder__shareholderName").annotate(
        Deposited_Amount=Sum(Coalesce(F("amount"), 0, output_field=FloatField()))
    )

    qs = qs.annotate(
        Shareholder=F("shareholder__shareholderName"), Amount=F("Deposited_Amount")
    )

    # if start:
    #     qs = Shareholder.filter(date__gte=start)
    # if end:
    #     qs = Shareholder.filter(date__lte=end)

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
    # fig_avg = px.bar(
    #     x=x_avg,
    #     y=y_avg,
    #     text=text_avg,
    #     title="Amount Deposited",
    #     labels={"x": "Share Holders", "y": "Average Amount per Flat"},
    # )
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

    # fig_avg.title = "Amount Deposited"
    # fig_avg.labels = {"x": "Share Holders", "y": "Average Amount per Flat"}
    fig.update_layout(title={"font_size": 24, "xanchor": "center", "x": 0.5})

    chart = fig.to_html()

    fig_avg.update_layout(title={"font_size": 24, "xanchor": "center", "x": 0.5})
    chart_avg = fig_avg.to_html()

    context = {"chart": chart, "chart_avg": chart_avg}
    return render(request, "accounts/index.html", context)
