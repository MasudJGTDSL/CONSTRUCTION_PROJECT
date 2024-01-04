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

from .forms import (
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
from .models import (
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


class ContractorTypeView(generic.edit.FormView):
    template_name = "accounts/forms/form_single_column.html"
    form_class = ContractorTypeForm
    success_url = "/"
    # print(form)

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Thank you. A new contractor type added.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        # called whenever the pages is rendered
        context = super().get_context_data(**kwargs)
        heading = "Add New Contractor Type"
        context["heading"] = heading
        data = ContractorType.objects.all()
        context["data"] = data
        data_heading = "Existing Contractor Types:"
        context["data_heading"] = data_heading
        detil_tag = False
        context["detil_tag"] = detil_tag
        # context["query_params"] = self.request.GET.get(
        #     "q", "a default"
        # )  # should be testingtesting
        return context


class ContractorView(generic.edit.FormView):
    template_name = "accounts/forms/form_single_column.html"
    form_class = ContractorForm
    success_url = "/"
    # print(form)

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Thank you. A new contractor added.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        heading = "Add New Contractor"
        context["heading"] = heading
        data = Contractor.objects.all()
        context["data"] = data
        data_heading = "Existing Contractors:"
        context["data_heading"] = data_heading
        detil_tag = True
        context["detil_tag"] = detil_tag

        return context


class ContractorDetailView(DetailView):
    model = Contractor
    template_name = "accounts/report_templates/contractor_details.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context["now"] = timezone.now()
        return context
class ShareholderDetailView(DetailView):
    model = Shareholder
    template_name = "accounts/report_templates/shareholder_details.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context["now"] = timezone.now()
        return context


class ItemCodeView(generic.edit.FormView):
    template_name = "accounts/forms/form_single_column.html"
    form_class = ItemCodeForm
    success_url = "/"
    # print(form)

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Thank you. A new Work Sector added.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        heading = "Add New Work Sector"
        context["heading"] = heading
        data = ItemCode.objects.all()
        context["data"] = data
        data_heading = "Existing Work Sectors:"
        context["data_heading"] = data_heading
        detil_tag = False
        context["detil_tag"] = detil_tag
        return context


class ItemView(generic.edit.FormView):
    template_name = "accounts/forms/form_item_add.html"
    form_class = ItemForm
    success_url = "/"
    # print(form)

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Thank you. A new Item added.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        heading = "Add New Item"
        context["heading"] = heading
        data = Item.objects.all()
        context["data"] = data
        data_heading = "Existing Items:"
        context["data_heading"] = data_heading
        detil_tag = False
        context["detil_tag"] = detil_tag
        return context


class ExpenditureView(generic.edit.FormView):
    template_name = "accounts/forms/form_expenditure.html"
    form_class = ExpenditureForm
    success_url = "/"
    # print(form)

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Thank you. Expenditure posting done.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        heading = "Expenditure"
        context["heading"] = heading
        # max_date = Expenditure.objects.latest('dateOfTransaction').dateOfTransaction
        max_date = (
            Expenditure.objects.values_list("dateOfTransaction")
            .annotate(Transaction_Date_Count=Count(F("dateOfTransaction")))
            .order_by("-dateOfTransaction")[:7]
        )
        # print(max_date.query)
        # print(max_date)
        data = Expenditure.objects.filter(
            dateOfTransaction__in=[
                str(max_date[0][0].strftime("%Y-%m-%d")),
                str(max_date[1][0].strftime("%Y-%m-%d")),
                str(max_date[2][0].strftime("%Y-%m-%d")),
                str(max_date[3][0].strftime("%Y-%m-%d")),
                str(max_date[4][0].strftime("%Y-%m-%d")),
                str(max_date[5][0].strftime("%Y-%m-%d")),
                str(max_date[6][0].strftime("%Y-%m-%d")),
            ]
        )
        # print(data.query)
        data_heading = "Last 7 Days Expenditure:"
        context["data"] = data
        context["data_heading"] = data_heading
        return context


class ContractorBillView(generic.edit.FormView):
    template_name = "accounts/forms/form_contractor_bill.html"
    form_class = ContractorBillForm
    success_url = "/"
    # print(form)

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Thank you. Contractor Bill Posting done.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        heading = "Contractor Bill"
        context["heading"] = heading
        # max_date = Expenditure.objects.latest('dateOfTransaction').dateOfTransaction
        max_date = (
            ContractorBill.objects.values_list("dateOfTransaction")
            .annotate(Transaction_Date_Count=Count(F("dateOfTransaction")))
            .order_by("-dateOfTransaction")[:7]
        )
        # print(max_date.query)
        # print(max_date)
        data = ContractorBill.objects.filter(
            dateOfTransaction__in=[
                str(max_date[0][0].strftime("%Y-%m-%d")),
                str(max_date[1][0].strftime("%Y-%m-%d")),
                str(max_date[2][0].strftime("%Y-%m-%d")),
                str(max_date[3][0].strftime("%Y-%m-%d")),
                str(max_date[4][0].strftime("%Y-%m-%d")),
                str(max_date[5][0].strftime("%Y-%m-%d")),
                str(max_date[6][0].strftime("%Y-%m-%d")),
            ]
        )
        # print(data.query)
        data_heading = "Last 7 Days Bill Payment:"
        context["data"] = data
        context["data_heading"] = data_heading
        return context


class ShareholderDepositView(generic.edit.FormView):
    template_name = "accounts/forms/form_shareholder_deposit.html"
    form_class = ShareholderDepositForm
    success_url = "/"
    # print(form)

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Thank you. Shareholder Deposit Posting done.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        heading = "Shareholder Deposit"
        context["heading"] = heading
        # max_date = Expenditure.objects.latest('dateOfTransaction').dateOfTransaction
        max_date = (
            ShareholderDeposit.objects.values_list("dateOfTransaction")
            .annotate(Transaction_Date_Count=Count(F("dateOfTransaction")))
            .order_by("-dateOfTransaction")[:7]
        )
        # print(max_date.query)
        # print(max_date)
        data = ShareholderDeposit.objects.filter(
            dateOfTransaction__in=[
                str(max_date[0][0].strftime("%Y-%m-%d")),
                str(max_date[1][0].strftime("%Y-%m-%d")),
                str(max_date[2][0].strftime("%Y-%m-%d")),
                str(max_date[3][0].strftime("%Y-%m-%d")),
                str(max_date[4][0].strftime("%Y-%m-%d")),
                str(max_date[5][0].strftime("%Y-%m-%d")),
                str(max_date[6][0].strftime("%Y-%m-%d")),
            ]
        )
        # print(data.query)
        data_heading = "Last 7 Days Shareholder Deposit:"
        context["data"] = data
        context["data_heading"] = data_heading
        return context


class ShareholderView(generic.edit.FormView):
    template_name = "accounts/forms/form_shareholder.html"
    form_class = ShareholderForm
    success_url = "/"
    # print(form)

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Thank you. A New Shareholder Added.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        heading = "Add New Shareholder"
        context["heading"] = heading
        data = Shareholder.objects.all().order_by("-numberOfFlat")
        data_heading = "Existing Shareholder List:"
        context["data"] = data
        context["data_heading"] = data_heading
        return context


def chart(request):
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
        email_list += f"{x[0]},"

    if request.method == "POST":
        fm = SendMailForm(request.POST or None, request.FILES or None)
        if fm.is_valid():
            subject = fm.cleaned_data["subject"]
            message = fm.cleaned_data["msg"]
            from_mail = request.user.email
            to_mail = fm.cleaned_data["email_id"]
            to_cc = fm.cleaned_data["email_cc"]
            to_bcc = fm.cleaned_data["email_bcc"]
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
                    return HttpResponse("Invalid header found")
                return HttpResponseRedirect("/")
            else:
                return HttpResponse("Make sure all fields are entered and valid.")
    else:
        fm = SendMailForm(initial={"email_id": email_list})
        # fm.initial
    return render(request, "accounts/send_mail.html", {"fm": fm, "qs": qs})


def index(request):
    qs = Expenditure.objects.values("item__ItemCode__workSector").annotate(
        spent_amount=Sum(Coalesce(F("amount"), 0, output_field=FloatField()))
    )
    qs = qs.annotate(
        work_sector=F("item__ItemCode__workSector"), Amount=F("spent_amount")
    )

    fig_bar = px.bar(
        x=[c["work_sector"] for c in qs],
        y=[c["Amount"] for c in qs],
        # text=[f"{(amnt/10**5):,.2f} Lac" for amnt in [c["Amount"] for c in qs]],
        text_auto=".2s",
        title="Work Sector Wise Spent Amount",
        color=[c["Amount"] for c in qs],
        labels={"x": "Work Sector", "y": "Amount Taka"},
    )
    fig_bar.update_layout(
        title={"font_size": 24, "xanchor": "center", "x": 0.5}, barmode="group"
    )
    fig_bar.update_traces(textangle=-90, textposition="outside", cliponaxis=False)
    fig_bar_chart = fig_bar.to_html()

    fig_pie = px.pie(
        qs,
        values="Amount",
        names="work_sector",
        title="Work Sector Wise Spent Amount",
        #  color_discrete_sequence=px.colors.sequential.RdBu
    )
    # update_traces(title_text="Work Sector", selector=dict(type='pie'))
    fig_pie.update_traces(textinfo="label+percent", textposition="outside")
    fig_pie.update_layout(
        showlegend=True, title={"font_size": 24, "xanchor": "auto", "x": 0.5}
    )
    fig_pie_chart = fig_pie.to_html()

    total_deposited = ShareholderDeposit.objects.aggregate(Sum("amount"))
    total_Expenditure = Expenditure.objects.aggregate(Sum("amount"))

    qs_shareholder = ShareholderDeposit.objects.values("shareholder__shareholderName").annotate(
        Deposited_Amount=Sum(Coalesce(F("amount"), 0, output_field=FloatField()))
    )

    qs_shareholder = qs_shareholder.annotate(
        Shareholder=F("shareholder__shareholderName"), Amount=F("Deposited_Amount")
    )

    qs_shareholder_avg = ShareholderDeposit.objects.values("shareholder__shareholderName").annotate(
        Deposited_Amount=ExpressionWrapper(
            Sum(Coalesce(F("amount"), 0, output_field=FloatField()))
            / F("shareholder__numberOfFlat"),
            output_field=FloatField(),
        )
    )

    x_avg = qs_shareholder_avg.values_list("shareholder__shareholderName", flat=True)
    y_avg = qs_shareholder_avg.values_list("Deposited_Amount", flat=True)
    text_avg = [f"{(amnt/10**3):,.2f}K" for amnt in y_avg]

    fig_shareholder_avg = px.bar(
        x=x_avg,
        y=y_avg,
        # text=text_avg,
        text_auto=".2s",
        title="Per Flat Deposited by The Shareholders",
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

    fig_shareholder = px.pie(
        qs_shareholder,
        values="Amount",
        names="Shareholder",
        title="Amount Deposited by The Shareholders",
        #  color_discrete_sequence=px.colors.sequential.RdBu
    )

    # fig_avg.title = "Amount Deposited"
    # fig_avg.labels = {"x": "Share Holders", "y": "Average Amount per Flat"}
    fig_shareholder_avg.update_traces(textangle=-90, textposition="outside", cliponaxis=False)
    fig_shareholder_avg.update_layout(
        title={"font_size": 24, "xanchor": "center", "x": 0.5}, barmode="group"
    )

    fig_shareholder.update_traces(textinfo="label+percent", textposition="outside")
    fig_shareholder.update_layout(
        showlegend=False, title={"font_size": 24, "xanchor": "auto", "x": 0.5}
    )

    chart_shareholder = fig_shareholder.to_html()
    chart_shareholder_avg = fig_shareholder_avg.to_html()

    context = {
        "chart_shareholder":chart_shareholder,
        "chart_shareholder_avg":chart_shareholder_avg,
        "fig_pie_chart": fig_pie_chart,
        "fig_bar_chart": fig_bar_chart,
        "total_deposited": total_deposited,
        "total_Expenditure": total_Expenditure,
    }  # "fig_bar_chart": fig_bar_chart
    return render(request, "accounts/dashboard.html", context)


# def chart(request):
#     # start = request.GET.get("start")
#     # end = request.GET.get("end")

#     qs = ShareholderDeposit.objects.values("shareholder__shareholderName").annotate(
#         Deposited_Amount=Sum(Coalesce(F("amount"), 0, output_field=FloatField()))
#     )

#     qs = qs.annotate(
#         Shareholder=F("shareholder__shareholderName"), Amount=F("Deposited_Amount")
#     )

#     # if start:
#     #     qs = Shareholder.filter(date__gte=start)
#     # if end:
#     #     qs = Shareholder.filter(date__lte=end)

#     fig = px.bar(
#         x=[c["Shareholder"] for c in qs],
#         y=[c["Amount"] for c in qs],
#         text=[f"{(amnt/10**5):,.2f}Lac" for amnt in [c["Amount"] for c in qs]],
#         title="Amount Deposited Per Flat",
#         labels={"x": "Share Holders", "y": "Amount Taka"},
#     )

#     qs_avg = ShareholderDeposit.objects.values("shareholder__shareholderName").annotate(
#         Deposited_Amount=ExpressionWrapper(
#             Sum(Coalesce(F("amount"), 0, output_field=FloatField()))
#             / F("shareholder__numberOfFlat"),
#             output_field=FloatField(),
#         )
#     )

#     x_avg = qs_avg.values_list("shareholder__shareholderName", flat=True)
#     y_avg = qs_avg.values_list("Deposited_Amount", flat=True)
#     text_avg = [f"{(amnt/10**3):,.2f}K" for amnt in y_avg]
#     # fig_avg = px.bar(
#     #     x=x_avg,
#     #     y=y_avg,
#     #     text=text_avg,
#     #     title="Amount Deposited",
#     #     labels={"x": "Share Holders", "y": "Average Amount per Flat"},
#     # )
#     fig_avg = px.bar(
#         x=x_avg,
#         y=y_avg,
#         # text=text_avg,
#         text_auto=".2s",
#         title="Amount Deposited",
#         labels={"x": "Share Holders", "y": "Average Amount per Flat"},
#         color=y_avg,
#         # color_discrete_map = ['gold', 'mediumturquoise', 'darkorange', 'lightgreen']
#         color_discrete_map={
#             "Thur": "lightcyan",
#             "Fahim Amin": "cyan",
#             "Sat": "royalblue",
#             "Sun": "darkblue",
#         },
#     )
#     fig = px.pie(
#         qs,
#         values="Amount",
#         names="Shareholder",
#         title="Amount Deposited",
#         #  color_discrete_sequence=px.colors.sequential.RdBu
#     )
#     # fig_avg.title = "Amount Deposited"
#     # fig_avg.labels = {"x": "Share Holders", "y": "Average Amount per Flat"}
#     fig.update_layout(title={"font_size": 24, "xanchor": "center", "x": 0.5})
#     chart = fig.to_html()
#     fig_avg.update_layout(title={"font_size": 24, "xanchor": "center", "x": 0.5})
#     chart_avg = fig_avg.to_html()
#     context = {"chart": chart, "chart_avg": chart_avg}
#     return render(request, "accounts/index.html", context)


@login_required
def get_item(request, itemCode_id):
    item = Item.objects.filter(ItemCode_id=itemCode_id)
    data = serializers.serialize("json", item)
    return HttpResponse(data, content_type="application/json")


@login_required
def get_shareholder_deposit_info(request, shareholder_id):
    deposit = (
        ShareholderDeposit.objects.filter(shareholder_id=shareholder_id)
        .values(
            "shareholder__shareholderName",
            "dateOfTransaction",
            "modeOfDeposit",
            "amount",
            "remarks",
        )
        .order_by("-dateOfTransaction")
    )

    total_deposit = (
        ShareholderDeposit.objects.values("shareholder")
        .annotate(total_amount=Sum("amount"))
        .get(shareholder_id=shareholder_id)
    )

    print(total_deposit)
    total_deposited_amount = {
        "total_deposit": str(intcomma_bd(total_deposit["total_amount"]))
    }

    deposit_info = []

    for item in deposit:
        shareholderName = str(item["shareholder__shareholderName"])
        date_of_transaction = str(item["dateOfTransaction"].strftime("%d %b %Y"))
        modeOfDeposit = str(item["modeOfDeposit"])
        amount = f'{str(intcomma_bd(item["amount"]))}/='
        remarks = str((item["remarks"] if item["remarks"] != None else "----"))
        dict_items = {
            "shareholderName": shareholderName,
            "date_of_transaction": date_of_transaction,
            "modeOfDeposit": modeOfDeposit,
            "amount": amount,
            "remarks": remarks,
        }
        deposit_info.append(dict_items)

    deposit_info.append(total_deposited_amount)

    info = json.dumps(deposit_info)
    return HttpResponse(info)


#! Reports =================================================
class ExpenditureSummary(LoginRequiredMixin, ListView):
    model = Expenditure
    template_name = "accounts/report_templates/expenditure_summary.html"
    context_object_name = "expenditure"
    # paginate_by = 30

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.values(
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
        # subquery_unit = Item.objects.values("unit", "itemName").filter(
        #     itemName=OuterRef("item__itemName")
        # )

        # qs = qs.annotate(unit=Subquery(subquery_unit.values("unit")))
        qs = qs.annotate(
            worksector_sum=Subquery(subquery_work_sector_sum.values("worksector_sum")),
        )
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        grand_total = Expenditure.objects.aggregate(Sum("amount"))
        context["grand_total"] = grand_total
        return context


class ExpenditureDetailsList(LoginRequiredMixin, ListView):
    model = Expenditure
    template_name = "accounts/report_templates/expenditure_detail_list.html"
    context_object_name = "expenditure"
    # paginate_by = 30

    def get_queryset(self):
        qs = super().get_queryset()
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
                worksector_sum=Coalesce(
                    Sum(F("amount")), 0, output_field=DecimalField()
                )
            )
        )
        qs = qs.annotate(
            worksector_sum=Subquery(subquery_work_sector_sum.values("worksector_sum")),
        ).order_by("work_sector", "item_name", "-dateOfTransaction")
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        grand_total = Expenditure.objects.aggregate(Sum("amount"))
        context["grand_total"] = grand_total
        return context
