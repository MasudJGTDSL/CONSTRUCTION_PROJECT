from datetime import date, datetime, time, timedelta

from django.utils import timezone

# from fdr.models import CurrentFiscal

anonymous_company = True


def company_info_settings(request):
    if anonymous_company:
        company_name_bn = "প্রতিষ্ঠান/কোম্পানির পূর্ন নাম"
        company_name_en = "Name of The Institution"
        copy_right_bn = "মাহিম সফ্‌ট | "
        copy_right_en = "Mahim Soft | "
        company_abr_bn = "এক্সটিডিসিএল"
        company_abr_en = "XTDCL"
        company_head_office_bn = "প্রতিষ্ঠানের প্রধান কার্যালয়"
        company_head_office_en = "Head Office"
        company_address_bn = (
            "প্রতিষ্ঠানের ঠিকানা (হাউজ নং-###, এলাকার নাম, শহরের নাম, পোস্ট কোড-####)"
        )
        company_address_en = (
            "Address (House No.###, Street, City, State, Postcode, County, Country)"
        )
        # From static/icons Folder ===========
        company_logo_fevicon = "company_logo_fevicon_1.png"
        company_logo_sm = "company_logo_sm_5.png"
        company_logo_lg = "company_logo_lg.png"

    else:
        company_name_bn = "‌জালালাবাদ গ্যাস টি এ্যান্ড ডি সিস্টেম লিঃ"
        company_name_en = "Jalalabad Gas T & D System Ltd."
        copy_right_bn = "মাহিম সফ্‌ট | "
        copy_right_en = "Mahim Soft | "
        company_abr_bn = "জেজিটিডিএসএল"
        company_abr_en = "JGTDSL"
        company_head_office_bn = "পেট্রোবাংলার একটি কোম্পানি"
        company_head_office_en = "A Company of Petrobangla"
        company_address_bn = "গ্যাস ভবন, মেন্দিবাগ, সিলেট-৩১০০"
        company_address_en = "Gasbhaban, Mendibagh, Sylhet-3100"
        # From static/icons Folder ===========
        company_logo_fevicon = "company_logo_fevicon_1.png"
        company_logo_sm = "company_logo_sm_5.png"
        company_logo_lg = "company_logo_lg.png"

    # current_fiscal = CurrentFiscal.objects.all().order_by("-id")[0]
    # fiscal_year_1st_part = current_fiscal.Fiscal
    # fiscal_year_2nd_part = current_fiscal.Fiscal + 1
    # fiscal_start_date = date(fiscal_year_1st_part, 7, 1)
    # fiscal_end_date = date(fiscal_year_2nd_part, 6, 30)
    # fiscal = f"{fiscal_year_1st_part}-{fiscal_year_2nd_part}"
    time = timezone.now()
    return {
        "company_name_bn": company_name_bn,
        "company_name_en": company_name_en,
        "company_abr_bn": company_abr_bn,
        "company_abr_en": company_abr_en,
        "company_address_bn": company_address_bn,
        "company_address_en": company_address_en,
        "company_head_office_bn": company_head_office_bn,
        "company_head_office_en": company_head_office_en,
        "copy_right_bn": copy_right_bn,
        "copy_right_en": copy_right_en,
        # Logo and Icons ========
        "company_logo_sm": company_logo_sm,
        "company_logo_lg": company_logo_lg,
        "company_logo_fevicon": company_logo_fevicon,
        # Fiscal and Dates ======
        # "fiscal_year_1st_part": fiscal_year_1st_part,
        # "fiscal": fiscal,
        # "fiscal_start_date": fiscal_start_date,
        # "fiscal_end_date": fiscal_end_date,
        "time": time,
    }
