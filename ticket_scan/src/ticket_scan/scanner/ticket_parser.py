import json

example_ticket = {
    '0': 'MERCADONA S.A.',
    '1': 'C/ MAYOR, 7 - ESPINARLO',
    '2': 'o MURCIA',
    '3': 'TELEFONO; 9568307114',
    '4': 'NIF: A-46103834',
    '5': '17/63/2019 19:51 OP: 1059346',
    '6': 'HACTURA SIMPLIFICADA: 2308-011-643UT6',
    '7': 'Preciu Importe',
    '8': 'Vescripción unidad (€)',
    '9': '1 B,ALMENDRA S/A 8,40',
    '10': '4 L SEMI S/LACTO 4,50 16,00',
    '11': '3 GALLETA RELTEV 1,22 3,66',
    '12': '1 COPOS AVENA 0,81',
    '13': '1 COSTILLA BARB 3,99',
    '14': '1 ZANAHORIA BOLS 0,69',
    '15': '2 VENTRESCA ATUN 2,15 4,30',
    '16': '1 PAPEL HIGIENIC 2,70',
    '17': '1 HIGIÉNICO DOBL 2,07',
    '18': '1 PEPINO y o',
    '19': '0,418 kg 1,89 €/kg ug',
    '20': '1 PLATANO o',
    '21': '0,616 kg 2,29 e/ky 1,41',
    '22': 'TOTAL 49',
    '23': 'LILTALLE (€)',
    '24': '1YA BASE IMPONIBLE CUOTA',
    '25': '4% 20,19 0,81',
    '26': '10% 19,24 1,92',
    '27': '2% 3,94 0,83',
    '28': 'DUTAL 43,97 3,56',
    '29': 'A',
    '30': 'AUT: 307029',
    '31': 'uz 44101236',
    '32': '+ PAGO TARJETA BANCARIA +',
    '33': '- YUYODO3 101',
    '34': '«13A CLASICA',
    '35': 'SE ADMLIEN DEVOLUCIONES CON TiCkEf'
}

store_name = "MERCADONA S.A."
list_upper_limit = "Descripción unidad (€)"
list_lower_limit = "TOTAL "

# TODO set searches or defaults for specific ticket.
street = ""
telephone = ""
store_id = ""
# ...

date_upper_limit = "" # In this case nif string...

# TODO locate line with known format for this case it should
## be all the store info
def locate_line_with_similarity(ticket:dict, string, similarity_threshold=75):
    pass

# TODO locate one or more lines with known formats of
## upper and lower lines bounding
## for this case it should be date and lines
def locate_lines_with_limits(upper_limit, lower_limit):
    pass

# TODO request stores to ticket_store and check which
## one is the more likely to be it.
##
def get_store(ticket: dict):
    pass

# TODO parse whole ticket and return the most plausible form
## of ticket (Store, Ticket info, lines, total and payment method)
def parse_ticket(ticket: dict):
    pass