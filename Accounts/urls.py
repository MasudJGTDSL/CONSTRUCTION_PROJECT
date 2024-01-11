from django.urls import path, include
from . import views
from . import reports

app_name = "Accounts"

urlpatterns = [
    path("", views.index, name="index"),
    path("send_mail/", views.send_mail, name="send_mail"),
    path(
        "targetedamount/", views.TargetedAmountPosting.as_view(), name="targetedamount"
    ),
    path("contractortype/", views.ContractorTypeView.as_view(), name="contractortype"),
    path("contractor/", views.ContractorView.as_view(), name="contractor"),
    path(
        "contractor/<int:pk>",
        views.ContractorDetailView.as_view(),
        name="contractor-details",
    ),
    path("itemcode/", views.ItemCodeView.as_view(), name="itemcode"),
    path("item/", views.ItemView.as_view(), name="item"),
    path("expenditure/", views.ExpenditureView.as_view(), name="expenditure_posting"),
    path(
        "contractor_bill/", views.ContractorBillView.as_view(), name="contractor_bill"
    ),
    path("shareholder/", views.ShareholderView.as_view(), name="shareholder"),
    path(
        "shareholder_list/",
        views.ShareholderListView.as_view(),
        name="shareholder_list",
    ),
    path(
        "shareholder_deposit/",
        views.ShareholderDepositView.as_view(),
        name="shareholder_deposit",
    ),
    path(
        "shareholder_deposit_list/<int:shareholder_id>",
        views.ShareholderDepositList.as_view(),
        name="shareholder_deposit_list",
    ),
    path(
        "shareholder/<int:pk>",
        views.ShareholderDetailView.as_view(),
        name="shareholder-details",
    ),
    path("chart/", views.chart, name="chart"),
    path("plot/", views.plot_chart, name="plot_chart"),
    # Html Reports ========================
    path(
        "expenditure_summary/",
        views.ExpenditureSummary.as_view(),
        name="expenditure_summary",
    ),
    path(
        "expenditure_details_list/",
        views.ExpenditureDetailsList.as_view(),
        name="expenditure_details_list",
    ),
    # Html Reports End ====================
    # serializers =========================
    path("get_item/<str:itemCode_id>", views.get_item, name="get_item"),
    path(
        "get_shareholder_deposit_info/<str:shareholder_id>",
        views.get_shareholder_deposit_info,
        name="get_shareholder_deposit_info",
    ),
    # serializers end =========================
]

Report_URLS = [
    path(
        "contractorDetails/<int:pk>",
        reports.contractorDetails,
        name="contractorDetails",
    ),
]
urlpatterns += Report_URLS
