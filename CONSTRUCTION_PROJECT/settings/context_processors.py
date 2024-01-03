from datetime import date, datetime, time, timedelta

from django.utils import timezone

# from fdr.models import CurrentFiscal

#! Setup ===================
anonymous_company = False
language = "en"

font_en_banner = "BalletRegular"
font_bn_banner = "b_fontkero"

font_en_other = "CompanyNameFont"
font_bn_other = "b_fontpadmo"

font_size_en_banner = "fs-3"
font_size_bn_banner = "fs-1"


def company_info_settings(request):
    if anonymous_company:
        if language == "en":
            company_name = "Name of The Institution"
            company_head_office = "Head Office"
            company_abr = "Samprity"
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
            company_name = "Samprity Tower"
            company_abr = "S.Tower"
            company_address = "Samprity Tower, Bawnia, Turag, Dhaka-1231"
            company_head_office = ""
            #! Font asigning ================
            font_banner = font_en_banner
            font_size_banner = font_size_en_banner
            font_other = font_en_other
        else:
            company_name = "‌সম্প্রীতি টাওয়ার"
            copy_right = "মাহিম সফ্‌ট | "
            company_abr = "জেজিটিডিএসএল"
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
    }
