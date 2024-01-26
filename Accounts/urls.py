from django.urls import path, include
from . import views
from . import reports

app_name = "Accounts"

urlpatterns = [
    path("", views.index, name="index"),
    path("VisitorList/", views.VisitorList.as_view(), name="VisitorList"),
    path("VisitorList/<int:pk>", views.VisitorDetails.as_view(), name="VisitorDetails"),
    path("send_mail/", views.send_mail, name="send_mail"),
    path(
        "contractor/<int:pk>",
        views.ContractorDetailView.as_view(),
        name="contractor-details",
    ),
    path(
        "shareholder_list/",
        views.ShareholderListView.as_view(),
        name="shareholder_list",
    ),
    path(
        "contractor_list/",
        views.ContractorListView.as_view(),
        name="contractor_list",
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
    path(
        "get_shareholder_deposit_info/<str:shareholder_id>",
        views.get_shareholder_deposit_info,
        name="get_shareholder_deposit_info",
    ),
]
#! Datast  =========================
Get_Dataset_URLs = [
    path("get_item/<str:itemCode_id>", views.get_item, name="get_item"),
    path(
        "get_credit_purchase_rest_amount/<int:seller_id>",
        views.get_credit_purchase_rest_amount,
        name="get_credit_purchase_rest_amount",
    ),
    path(
        "get_contractor_bill_rest_amount/<int:bill_id>",
        views.get_contractor_bill_rest_amount,
        name="get_contractor_bill_rest_amount",
    ),
]

Forms_URLs = [
    path(
        "targetedamount/", views.TargetedAmountPosting.as_view(), name="targetedamount"
    ),
    #! Shareholder ===============
    path("shareholder/", views.ShareholderView.as_view(), name="shareholder"),
    path(
        "shareholder_update/<int:pk>",
        views.ShareholderUpdate.as_view(),
        name="shareholder_update",
    ),
    path(
        "shareholder_deposit/",
        views.ShareholderDepositView.as_view(),
        name="shareholder_deposit",
    ),
    path(
        "shareholder_deposit_update/<int:pk>",
        views.ShareholderDepositUpdate.as_view(),
        name="shareholder_deposit_update",
    ),
    #! Contractor ===============
    path("contractortype/", views.ContractorTypeView.as_view(), name="contractortype"),
    path("contractor/", views.ContractorView.as_view(), name="contractor"),
    path(
        "contractor_update/<int:pk>",
        views.ContractorUpdate.as_view(),
        name="contractor_update",
    ),
    path(
        "expenditure_update/<int:pk>",
        views.ExpenditureUpdate.as_view(),
        name="expenditure_update",
    ),
    path(
        "contractor_bill_submission/",
        views.ContractorBillSubmissionView.as_view(),
        name="contractor_bill_submission",
    ),
    path(
        "contractor_bill_payment/",
        views.ContractorBillPaymentView.as_view(),
        name="contractor_bill_payment",
    ),
    #! Item ===============
    path("itemcode/", views.ItemCodeView.as_view(), name="itemcode"),
    path("item/", views.ItemView.as_view(), name="item"),
    path("expenditure/", views.ExpenditureView.as_view(), name="expenditure_posting"),
    #! CreditPurchase ===============
    path(
        "credit_purchase/", views.CreditPurchaseView.as_view(), name="credit_purchase"
    ),
    path(
        "credit_purchase_payment/",
        views.CreditPurchasePaymentView.as_view(),
        name="credit_purchase_payment",
    ),
]

#! PDF Reports ========================
Report_URLs = [
    path(
        "contractorDetails/<int:pk>",
        reports.contractorDetails,
        name="contractorDetails",
    ),
    path(
        "shareholderDetails/<int:pk>",
        reports.shareholderDetails,
        name="shareholderDetails",
    ),
    path(
        "expenditureSummaryReport/",
        reports.expenditureSummaryReport,
        name="expenditureSummaryReport",
    ),
    path(
        "expenditureDetailsReport/",
        reports.expenditureDetailsReport,
        name="expenditureDetailsReport",
    ),
]

urlpatterns += Forms_URLs
urlpatterns += Report_URLs
urlpatterns += Get_Dataset_URLs
