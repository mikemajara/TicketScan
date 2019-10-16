import time
import json
import random
import numpy as np

COMPANIES = [
    {
        "_id": "5d76824c1855750cd80a8037",
        "name": "MERCADONA S.A.",
        "tax_id": "A-46103834",
        "web": None
    }
]

STORES = [
    {
        "_id": "5d8742d3dcad30c5cc30624d",
        "address": "C/ MAYOR, 7 - ESPINARDO",
        "address_strings": [
            "C/ MAYOR, 7 - ESPINARDO",
            "Murcia"
        ],
        "city": "Murcia",
        "company_id": "5d76824c1855750cd80a8037",
        "country": "Spain",
        "phone": "968392509"
    }
]

PRODUCTS = [
    'LECHE', 
    'CEBOLLA',
    'TOMATES',
    'HUEVOS',
    'AJOS',
    'PAN BIMBO',
    'FRUTA',
    'GAZPACHO',
    'ZANAHORIAS',
    'AGUA',
    'CHOCOLATE',
    'PIZZA',
    'QUESO GRATINADO',
    'QUESO NORMAL',
    'PAPEL HIGIÉNICO',
    'ACEITE TOSTADAS',
    'ACEITE COCINA',
    'DESHODORANTE'
]

METHODS = ['CARD', 'CASH']

BILLS = [5, 10, 20, 50, 100, 200, 500]


def str_time_prop(start, end, format, prop):
    stime = time.mktime(time.strptime(start, format))
    etime = time.mktime(time.strptime(end, format))
    ptime = stime + prop * (etime - stime)
    return time.strftime(format, time.localtime(ptime))


def get_random_date(start, end, prop):
    return str_time_prop(start, end, '%d/%m/%Y %H:%M', prop)
ff

def get_random_price():
    return round(random.random() * random.choice([1,10]), 2)


def get_random_line():
    name = random.choice(PRODUCTS)
    price = get_random_price()
    units = random.choice([1,1,1,1,1,1,2,2,2,3,3,4,])
    return {
        "name": name,
        "price": price,
        "total": round(units * price, 2),
        "units": units
    }

def get_random_payment_info(total):
    method = random.choice(METHODS)
    if method == 'CARD':
        return {
            "method": method,
            "total": total,
            "returned": None
        }
    else:
        payed = next(b for b in BILLS if b > total)
        returned = round(payed - total, 2)
        return {
            "method": method,
            "total": total,
            "returned": returned
        }



def get_random_lines():
    lines = []
    for _ in range(random.randint(1,10)):
        lines.append(get_random_line())
    return lines

def get_random_tickets(n):
    tickets = []
    for _ in range(n):
        company = random.choice(COMPANIES)
        store = random.choice(list(filter(lambda x: x["company_id"] == company["_id"], STORES)))
        date = get_random_date("01/07/2019 00:00", "01/10/2019 00:00", random.random())
        lines = get_random_lines()
        total = round(sum([l['total'] for l in lines]), 2)
        paymentInformation = get_random_payment_info(total)
        tickets.append({
            "company": company,
            "store": store,
            "date": date,
            "lines": lines,
            "paymentInformation": paymentInformation,
        })
    return tickets

def generate_random_ticket_file(n=9, file_name='random_tickets.json'):
    with open(file_name, 'w') as f:
        json.dump(get_random_tickets(n), f) 


