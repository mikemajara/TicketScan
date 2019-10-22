#!/usr/bin/env python
# -*- coding: utf-8 -*-

# TODO
#   Examples here are based on deprecated class ticket_parser
#   replace these tests with generalized, and specific tests
#   for tickets.
import os

import cv2
import pytest
from ticket_scan.scanner.ocr import extract_text_from_image, extract_text_from_file


__author__ = "Miguel López-N. Alcalde"
__copyright__ = "Miguel López-N. Alcalde"
__license__ = "proprietary"

TEST_IMAGES_PATH = 'test_images'
TEST_IMAGES_VALUES_FROM_FILE = {
    "149533795324992.jpeg": "MERCADONA S.A.\n\nC/ MAYOR, 7 - ESPINARLO\n\n \n\n \n\n \n\n \n\n \n\n \n\n \n\n \n\n \n\n \n\n \n\n \n\nMURCIA\nELEFONU: 968307114\nNIF; A-46103834\n1/03/2019 19:51 OP: 105946\nPACTURA SIMPL IFICADA: 2308-011-U4301l\nwa\nPrecio — Importe\nbescr ipcién unidad  (€)\n1 B,ALMENGRA S/A 8,40\n4. SEMT S/LACTO 4,50 18,00\n3 GALLETA RELTEY 1322 3,66\n1 COPOS AVENA 0,81\n1 COSTILLA BARB 3,99\n1 ZANAHORIA BOLS 6,69\n2 VENTRESCA ATUN 2,15 4,30\n1 PAPEL HIGIENIC z,70\n1 HIGIENICO DGBL 2,07\n1 PEPINO\n0,478 kg 1,89 €/kg uv, 90\n1 PLATANO\n0,616 kg 2,29 e/kg Al\nTAL 6,93\nTARJETA, BANCARTA = 46,98\nULTALLE (€)\n{¥A BASE IMPONIBLE CUOTA\ndk 20,19 0,81\n10% 19,24 1,92\n“ih 3,94 0,83\nIUTAL 43,37 3,56\n\nTARJ) Reb RagO 16\nAUT: 307029\n\nwl: 44101236\n+ PALO TARJETA BANCARIA *\n- WuuGG00031010\n\n+1DA CLAST\n“30\n\nCA\n\nSE ADMLIEN DEVOLUCTONES CON TICKET",
    "8219702639756318720.jpeg": "| _ Fytitstso. britesaggercetes.\nWPM kK.) $i Shs Heain  & : .. a3\n4 Yal mejor precio. Ea de | ule\n\nLIDL SUPERMERCADOS S.A.U.\nAvenida Miguel de Cervantes N2 110\n30009 Murcia\nNIF A60195278\nwww. lidl.es\n\nEUR\nFlauta de cereales 1,50 B\nzZ x 0,75\nPachugas codorniz 3,69 B\nAlcachofa unidad 1,16 4\n4 x 0,29\nCapsulas Intenso 1,99 B\nCapst: is Ristretto 1,99 B\nAlitas de poilo 2,39 B\n0,69 A\n\nChamp ‘6n\n\nTotal 13,41\n\nEntregado Me 20,42\nCambio -7,01\n\n_ IVA‘ IVA + P Neto 7 PYP\nA 4h 0,07 1,78 1,85\nB 10 % 1,05 - 10,51 11,56\n\nsuma 1,12 629 13,41\n\n~EARQUERANN\n\n3508 039467/02 12.01.19\nDevoluciones articulos de bazar con\n\nticket de compra y embalaje original\nen un plazo maximo de 30 dias sin\nperjuicio de la ley de garantias.\nHorario Tienda Lu a Sa 09:00 a 22:00\n- Atencién al cliente\nwww. ]idl.es/contacto Tel.900958311\nGRACIAS POR SU VISITA\n\n \n\n \n\n \n\n \n\n \n\n \n\n \n\n \n\n \n\n \n\n \n\n \n\n \n\n \n\n12:55"
}
TEST_IMAGES_VALUES_FROM_IMAGE = {
    "cropped_247_227.png": "Murcia",
    "cropped_386_359.png": "26/03/2019 20:54 0P; 11/2496",
    "cropped_606_581.png": "4 1 PICOS PACK-2 1,08",
}

def test_extract_text_from_file_should_return_tested_text():
    for filename in TEST_IMAGES_VALUES_FROM_FILE.keys():
        expected_result = TEST_IMAGES_VALUES_FROM_FILE[filename]
        fullpath = os.path.join(TEST_IMAGES_PATH, filename)
        assert expected_result == extract_text_from_file(fullpath)

def test_extract_text_from_image_should_return_tested_text():
    for filename in TEST_IMAGES_VALUES_FROM_IMAGE.keys():
        expected_result = TEST_IMAGES_VALUES_FROM_IMAGE[filename]
        fullpath = os.path.join(TEST_IMAGES_PATH, filename)
        image = cv2.imread(fullpath)
        assert expected_result == extract_text_from_image(image)