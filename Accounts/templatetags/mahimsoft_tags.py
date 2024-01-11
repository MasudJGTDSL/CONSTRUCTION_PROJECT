from django.template.defaultfilters import floatformat
import locale
from django.utils import numberformat
from decimal import Decimal
from datetime import date, datetime, time
from django import template
from django.conf import settings

# from fdr import choices

register = template.Library()


@register.filter
def subtract(value, arg):
    return value - arg


@register.filter
def number_product(value: Decimal, arg: Decimal):
    return round(value * arg, 0)


@register.filter
def devided(value, arg):
    return value / arg


@register.filter(is_safe=True)
def enTobnNumber(Value):
    numEn = "0123456789"
    numBn = "০১২৩৪৫৬৭৮৯"
    x = {}
    #! Adding Item to Dictionary =============
    for i in numEn:
        x[i] = numBn[int(i)]

    result = ""
    for it in Value:  # ! Item in given String Value =====
        if it in x:  # ! if key in Dictionary ========
            result += x[it]
        else:  # ! if key is not in Dictionary ========
            result += it
    return result


@register.filter(is_safe=True)
def dateINbangla(dateValue):
    day = dateValue.day
    month = dateValue.month
    year = dateValue.year
    monthNameVal = [
        "জানুয়ারি",
        "ফেব্রুয়ারি",
        "মার্চ",
        "এপ্রিল",
        "মে",
        "জুন",
        "জুলাই",
        "আগস্ট",
        "সেপ্টেম্বর",
        "অক্টোবর",
        "নভেম্বর",
        "ডিসেম্বর",
    ][int(month) - 1]
    return enTobnNumber(str(day) + " " + monthNameVal + ", " + str(year))


# @register.filter(is_safe=True)
# def LedgerSectorChoice(input):
#     sector_choices = dict(choices.Sectors)
#     sector = sector_choices.get(input)
#     return sector


@register.filter(is_safe=True)
def get_financial_year(date, fullFinYear=True):
    if fullFinYear == True:
        if date.month <= 6:
            financial_year = f"{date.year -1}-{date.year}"
        else:
            financial_year = f"{date.year}-{date.year +1}"
    else:
        if date.month <= 6:
            financial_year = f"{date.year -1}"
        else:
            financial_year = f"{date.year}"
    return financial_year


@register.filter(is_safe=True)
def percent(value):
    if value is None:
        return None
    else:
        value = floatformat(Decimal(value) * 100, 2)
        return f"{Decimal(value)}%"


@register.filter("has_group")
def has_group(user, group_name):
    groups = user.groups.all().values_list("name", flat=True)
    # print(groups)
    return True if group_name in groups else False

    # 🧾🧾🧾🖍🖍🖍 Uses in templates =================
    # {% if request.user|has_group:"Administradores"%}
    #       <div> Admins can see everything </div>
    # {% endif %}


# @register.filter
# def get_profile_image_url(user):
#     if user.Profile.image.url:
#         url= f'"{settings.MEDIA_ROOT}{user.Profile.image.url}"'
#         return url # user.Profile.image.url
#     else:
#         # Provide a default image URL or handle the case when no image is available.
#         return f'{settings.MEDIA_ROOT}/default.png'


"""
#!For Linux Local setting: 
To view local list: locale -a, 
For setup: sudo dpkg-reconfigure locales,

Other commands: 
sudo apt-get install language-pack-bn-base
sudo yum groupinstall "Bengali Support"
sudo locale-gen
import locale

locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
formatted_number = locale.format_string("%d", your_number, grouping=True)
print(formatted_number)
"""


@register.filter(is_safe=True)
def intcomma_bd(value, preserve_decimal=False):
    locale.setlocale(locale.LC_ALL, "bn_BD")
    try:
        if not isinstance(value, (int, float, Decimal)):
            value = float(value)
    except (TypeError, ValueError):
        return value
    number_with_coma = locale.format_string("%.0f", value, True)
    return number_with_coma


@register.filter(is_safe=True)
def floatcomma_bd(value, preserve_decimal=False):
    locale.setlocale(locale.LC_ALL, "bn_BD")
    try:
        if not isinstance(value, (int, float, Decimal)):
            value = float(value)
    except (TypeError, ValueError):
        return value
    number_with_coma = locale.format_string("%.2f", value, True)
    return number_with_coma


@register.filter(is_safe=True)
def floatword_indian(value):
    """
    Converts a large integer number into a friendly text representation.
    Highest Denomination is used and 2 lower powers are considered for floating
    points in text representation.
    Numbers less than 99 are returned without conversion.

    Denominations used are: Hundred, Thousand, Lakh, Crore

    Examples:
        1000 becomes 1 Thousand
        15000 becomes 15 Thousands
        15600 becomes 15.60 Thousands
        100000 becomes 1 Lakh
        1125000 becomes 11.25 Lakhs
        10000000 becomes 1 Crore
        56482485 becomes 5.64 Crore
        56482485.25 becomes 5.64 Crores

    :return: String
    """
    if isinstance(value, int) and value < 100:
        return str(value)
    if isinstance(value, float) and value < 99:
        return str(value)

    try:
        if isinstance(value, str):
            if "." not in value and int(value) < 99:
                return value
            if float(value) < 99:
                return value
    except (ValueError, TypeError):
        return value

    value_integer = str(value).split(".")[0]
    value_len = len(value_integer)
    if value_len > 7:
        crores = value_integer[:-7]
        lakhs = value_integer[-7:-5]
        if crores == "1" and lakhs == "00":
            return "1 Crore"
        if lakhs == "00":
            return "%s Crores" % crores
        return "%s.%s Crores" % (crores, lakhs)
    elif value_len > 5:
        lakhs = value_integer[:-5]
        thousands = value_integer[-5:-3]
        if lakhs == "1" and thousands == "00":
            return "1 Lakh"
        if thousands == "00":
            return "%s Lakhs" % lakhs
        return "%s.%s Lakhs" % (lakhs, thousands)
    elif value_len > 3:
        thousands = value_integer[:-3]
        hundreds = value_integer[-3:-1]
        if thousands == "1" and hundreds == "00":
            return "1 Thousand"
        if hundreds == "00":
            return "%s Thousands" % thousands
        return "%s.%s Thousands" % (thousands, hundreds)
    else:
        hundreds = value_integer[:-2]
        tens_ones = value_integer[-2:]
        if hundreds == "1" and tens_ones == "00":
            return "1 Hundred"
        if tens_ones == "00":
            return "%s Hundreds" % hundreds
        return "%s.%s Hundreds" % (hundreds, tens_ones)
