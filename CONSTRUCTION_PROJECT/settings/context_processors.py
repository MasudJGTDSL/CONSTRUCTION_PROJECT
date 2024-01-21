from datetime import date, datetime, time, timedelta
from django.contrib.auth.models import User
from Accounts.models import UserLoggedinRecord

from django.utils import timezone

# from fdr.models import CurrentFiscal

#! Setup ===================
anonymous_company = False
language = "en"

font_en_banner = "AeroSkyFont"
font_bn_banner = "b_fontkero"

font_en_other = "AeroSkyFont"
font_bn_other = "b_fontpadmo"

font_size_en_banner = "fs-5"
font_size_bn_banner = "fs-1"


def company_info_settings(request):
    if anonymous_company:
        if language == "en":
            company_name = "Name of The Institution"
            company_head_office = "Head Office"
            company_abr = "AS. Tower"
            copy_right = "Mahim Soft | "
            company_address = (
                "Address (House No.###, Street, City, State, Postcode, County, Country)"
            )
            font_banner = font_en_banner
            font_other = font_en_other
            font_size_banner = font_size_en_banner
        else:
            company_name = "প্রতিষ্ঠান/কোম্পানির পূর্ন নাম"
            copy_right = "মাহিম সফ্‌ট | "
            company_abr = "এক্সটিডিসিএল"
            company_head_office = "প্রতিষ্ঠানের প্রধান কার্যালয়"
            company_address = "প্রতিষ্ঠানের ঠিকানা (হাউজ নং-###, এলাকার নাম, শহরের নাম, পোস্ট কোড-####)"
            font_banner = font_bn_banner
            font_other = font_bn_other
            font_size_banner = font_size_bn_banner
        # From static/icons Folder ===========
        company_logo_fevicon = "anonymous_logo_fevicon.png"
        company_logo_sm = "anonymous_logo_sm.png"
        company_logo_lg = "anonymous_logo_lg.png"
    else:
        if language == "en":
            copy_right = "Mahim Soft | "
            company_name = "AeroSky Tower"
            company_abr = "SK.Tower"
            company_address = "AeroSky Tower, Bawnia, Turag, Dhaka-1231"
            company_head_office = ""
            #! Font asigning ================
            font_banner = font_en_banner
            font_size_banner = font_size_en_banner
            font_other = font_en_other
        else:
            company_name = "‌এ্যারোস্কাই টাওয়ার"
            copy_right = "মাহিম সফ্‌ট | "
            company_abr = "এ্যারোস্কাই"
            company_head_office = ""
            company_address = "বাউনিয়া, তুরাগ, ঢাকা-১২৩১"
            #! Font asigning ======================
            font_banner = font_bn_banner
            font_other = font_bn_other
            font_size_banner = font_size_bn_banner
        # From static/icons Folder ===========
        company_logo_fevicon = "company_logo_fevicon.png"
        company_logo_sm = "company_logo_sm.png"
        company_logo_lg = "company_logo_lg.png"
    time = timezone.now()
    total_number_of_flat = 36
    no_of_flat_per_share = 3
    return {
        "company_name": company_name,
        "company_abr": company_abr,
        "company_address": company_address,
        "company_head_office": company_head_office,
        "copy_right": copy_right,
        #! Font asigning ======================
        "font_banner": font_banner,
        "font_other": font_other,
        "font_size_banner": font_size_banner,
        # Logo and Icons ========
        "company_logo_sm": company_logo_sm,
        "company_logo_lg": company_logo_lg,
        "company_logo_fevicon": company_logo_fevicon,
        "time": time,
        "total_number_of_flat": total_number_of_flat,
        "no_of_flat_per_share": no_of_flat_per_share,
        "visitor_count": UserLoggedinRecord.objects.all().count(),
        "unique_visitor_count": UserLoggedinRecord.objects.values("visitorIP").distinct().count(),
    }