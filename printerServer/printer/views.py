# -*- coding: utf-8 -*-
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import win32api, time, os
import pdfkit

GHOSTSCRIPT_PATH = "C:/Program Files/gs/gs9.27/bin/gswin64.exe"
GSPRINT_PATH = 'C:/Program Files/gs/gsprint/gsprint.exe'
FILE = 'C:/Users/CafeBoard/Desktop/file.html'


@csrf_exempt
def print_something(request):
    data = request.POST
    for e in data:
        data = json.loads(e)

    location_printer_url = data['location_url']
    if data['is_customer_print'] == 0:
        for printer_data in data['invoice_data']['data']:
            printer_name = printer_data['printer_name']
            if len(printer_data['items']) == 0:
                break
            else:
                options = {
                    'page-width': '72mm',
                    'page-height': '297mm'
                }
                pdfkit.from_url(location_printer_url + 'template/invoice-no-cash?invoice_id=%s&printer_name=%s' % (
                    data['invoice_id'], printer_name), 'C:/Users/CafeBoard/Desktop/%s.pdf' % printer_name,
                                options=options)
                currentprinter = printer_name
                params = '-ghostscript "' + GHOSTSCRIPT_PATH + '" -printer "' + currentprinter + '" -copies 1 "C:/Users/CafeBoard/Desktop/"' + printer_name + '".pdf "'
                win32api.ShellExecute(0, 'open', GSPRINT_PATH, params, 'K', 0)
                time.sleep(3)
                os.remove("C:/Users/CafeBoard/Desktop/" + printer_name + ".pdf")
                file = open("C:/Users/CafeBoard/Desktop/" + printer_name + ".pdf", 'w')
                file.close()
        return JsonResponse({"response": 'OK'})

    else:
        options = [
            ('page-width', '80mm'),
            ('page-height', '297mm')
        ]
        pdfkit.from_url(location_printer_url + 'template/invoice-cash?invoice_id=%s' % data['invoice_id'],
                        'C:/Users/CafeBoard/Desktop/cash.pdf', options=options)
        currentprinter = 'Cash'
        params = '-ghostscript "' + GHOSTSCRIPT_PATH + '" -printer "' + currentprinter + '" -copies 1 "C:/Users/CafeBoard/Desktop/cash.pdf "'
        win32api.ShellExecute(0, 'open', GSPRINT_PATH, params, 'K', 0)
        time.sleep(3)
        os.remove("C:/Users/CafeBoard/Desktop/cash.pdf")
        file = open("C:/Users/CafeBoard/Desktop/cash.pdf", 'w')
        file.close()

    return JsonResponse({"response": 'OK'})


@csrf_exempt
def print_night_report(request):
    data = request.POST
    for e in data:
        data = json.loads(e)

    location_printer_url = "https://namak.works/"

    options = [
        ('page-width', '80mm'),
        ('page-height', '297mm')
    ]
    pdfkit.from_url(location_printer_url + 'template/night-report?cash_id=%s' % data['cash_id'],
                    'C:/Users/CafeBoard/Desktop/close.pdf', options=options)
    currentprinter = 'Cash'
    params = '-ghostscript "' + GHOSTSCRIPT_PATH + '" -printer "' + currentprinter + '" -copies 1 "C:/Users/CafeBoard/Desktop/close.pdf "'
    win32api.ShellExecute(0, 'open', GSPRINT_PATH, params, 'K', 0)
    time.sleep(3)
    os.remove("C:/Users/CafeBoard/Desktop/close.pdf")
    file = open("C:/Users/CafeBoard/Desktop/close.pdf", 'w')
    file.close()

    return JsonResponse({"response": 'OK'})
