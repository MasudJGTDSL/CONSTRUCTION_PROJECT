from django.contrib.auth.signals import (
    user_logged_in,
    user_logged_out,
    user_login_failed,
)
from django.db.models import Max
from django.db.models import Q
import datetime
from django.contrib.auth.models import User
from .models import UserLoggedinRecord,UserLoggedinFailed
from django.dispatch import receiver
from ipware import get_client_ip
import json
import urllib.request


##### FOR IP ADRESS ####
def get_ip(request):
    adress = request.META.get("HTTP_X_FORWARDED_FOR")
    if adress:
        ip = adress.split(",")[-1].strip()
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip


def client_location_details(request, *args, **kwargs):
    client_ip, is_routable = get_client_ip(request)
    if client_ip is None:
        client_ip = "0.0.0.0"
    else:
        if is_routable:
            ip_type = "public"
            ip_address = client_ip
        else:
            ip_type = "private"
            ip_address = "118.179.146.204"

        url = "https://api.ipfind.com/?ip=" + ip_address

        with urllib.request.urlopen(url) as response:
            responed = response.read()
        data = json.loads(responed)

        return data


@receiver(user_logged_in, sender=User)
def login_success(sender, request, user, **kwargs):
    # For visitor Count ==========================
    if get_ip(request) != "118.179.146.204":
        client = client_location_details(request, **kwargs)
        visitor = UserLoggedinRecord(visitorIP=client["ip_address"])
        visitor.country = client["country"]
        visitor.country_code = client["country_code"]
        visitor.continent = client["continent"]
        visitor.continent_code = client["continent_code"]
        visitor.city = client["city"]
        visitor.county = client["county"]
        visitor.region = client["region"]
        visitor.region_code = client["region_code"]
        visitor.timezone = client["timezone"]
        visitor.owner = client["owner"]
        visitor.longitude = client["longitude"]
        visitor.latitude = client["latitude"]
        visitor.currency = client["currency"]
        visitor.languages = client["languages"]
        visitor.user = user

        query_result = UserLoggedinRecord.objects.filter(
            Q(visitorIP__icontains=client["ip_address"])
        ).aggregate(Max("visitDateTime"))

        if query_result["visitDateTime__max"] != None:
            # If Visitor exist
            presentDate = int(datetime.datetime.now().strftime("%Y%m%d"))
            lastVisitDate = int(query_result["visitDateTime__max"].strftime("%Y%m%d"))

            if presentDate > lastVisitDate:
                visitor.visitCount = 1
                visitor.save()
            else:
                query_for_update = UserLoggedinRecord.objects.filter(
                    Q(visitorIP__icontains=client["ip_address"])
                ).order_by("-id")
                query_for_update.filter(id=query_for_update[0].id).update(
                    visitCount=query_for_update[0].visitCount + 1
                )
        else:
            # If Visitor not exist
            visitor.visitCount = 1
            visitor.save()
        # End visitor Count ==========================
    # print("-------------------------------")
    # print("Logged-in Signal... Run Intro..")
    # print("Sender:", sender)
    # print("Request:", request)
    # print("User:", user)
    # print("User:", kwargs["signal"])

    # for x in kwargs["Signal"]:
    #     a += 1
    #     print(f"{a}kwargs: {x}")
    # user_logged_in.connect(login_success, sender=User)


@receiver(user_login_failed)
def login_failed(sender, credentials, request, **kwargs):
    # For visitor Count ==========================
    if get_ip(request) != "118.179.146.204":
        client = client_location_details(request, **kwargs)
        visitor = UserLoggedinFailed(visitorIP=client["ip_address"])
        visitor.country = client["country"]
        visitor.country_code = client["country_code"]
        visitor.continent = client["continent"]
        visitor.continent_code = client["continent_code"]
        visitor.city = client["city"]
        visitor.county = client["county"]
        visitor.region = client["region"]
        visitor.region_code = client["region_code"]
        visitor.timezone = client["timezone"]
        visitor.owner = client["owner"]
        visitor.longitude = client["longitude"]
        visitor.latitude = client["latitude"]
        visitor.currency = client["currency"]
        visitor.languages = client["languages"]
        visitor.user = credentials["username"]
        visitor.password = credentials["password"]

        visitor.save()

    # print("Logged-in Signal... Run Intro..")
    # print("Sender:", sender)
    # print("Request:", request)
    # print("Credentials User:", credentials["username"])
    # print("Credentials Password:", credentials["password"])
    # print("kwargs:", kwargs)
# Credentials: {'username': 'sdfgshju', 'password': '********************'}