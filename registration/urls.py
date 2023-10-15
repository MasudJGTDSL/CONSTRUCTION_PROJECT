from django.urls import path
from . import views

app_name = 'registration'

urlpatterns = [
    # path('', views.home, name="home"),
    path('registerPage/', views.registerPage, name="registerPage"),
    # path('user_list_dropdown/', views.user_list_dropdown,
        #  name="user_list_dropdown"),
    ]

get_JSON_Response = [
    # path("get_BankBranch/<str:bank_id>", views.get_BankBranch, name="get_BankBranch"),
    # path("get_Account/<str:bankBranch_id>", views.get_Account, name="get_BankBranch"),
    # path("get_FDRInfo/<int:pk>", views.get_FDRInfo, name="get_FDRInfo"),
    # path("get_LedgerInfo/<int:pk>", views.get_LedgerInfo, name="get_LedgerInfo"),
    # path(
    #     "get_EncashmentInfo/<int:pk>",
    #     views.get_EncashmentInfo,
    #     name="get_EncashmentInfo",
    # ),
    # # path('accountSerializer/<str:bankBranch_id>', views.AccountSerializer.as_view(), name='accountSerializer'),
]

urlpatterns += get_JSON_Response

Report_URLS = [
    # path("RPTFDRList/", reports.RPTFDRList, name="RPTFDRList"),
    # path("RPTFdrDetails/<int:pk>", reports.RPTFdrDetails, name="RPTFdrDetails"),
    # path(
    #     "RPTFDRListSummarize/<str:flag>",
    #     reports.RPTFDRListSummarize,
    #     name="RPTFDRListSummarize",
    # ),
]

urlpatterns += Report_URLS
