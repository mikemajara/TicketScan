#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

import cv2
import pytest
from ticket_scan.scanner import ocr_batch

TEST_IMAGES_PATH = 'test_images'
TEST_IMAGES_VALUES_FROM_FILE = {
    "149533795324992.jpeg": {
        0: 'MERCADONA S.A.',
        1: 'C/ MAYOR, 7 - ESPINARLO',
        2: 'o MURCIA',
        3: 'TELEFONO; 9568307114',
        4: 'NIF: A-46103834',
        5: '17/63/2019 19:51 OP: 1059346',
        6: 'HACTURA SIMPLIFICADA: 2308-011-643UT6',
        7: 'Preciu Importe',
        8: 'Vescripción unidad (€)',
        9: '1 B,ALMENDRA S/A 8,40',
        10: '4 L SEMI S/LACTO 4,50 16,00',
        11: '3 GALLETA RELTEV 1,22 3,66',
        12: '1 COPOS AVENA 0,81',
        13: '1 COSTILLA BARB 3,99',
        14: '1 ZANAHORIA BOLS 0,69',
        15: '2 VENTRESCA ATUN 2,15 4,30',
        16: '1 PAPEL HIGIENIC 2,70',
        17: '1 HIGIÉNICO DOBL 2,07',
        18: '1 PEPINO y o',
        19: '0,418 kg 1,89 €/kg ug',
        20: '1 PLATANO o',
        21: '0,616 kg 2,29 e/ky 1,41',
        22: 'TOTAL 49',
        23: 'LILTALLE (€)',
        24: '1YA BASE IMPONIBLE CUOTA',
        25: '4% 20,19 0,81',
        26: '10% 19,24 1,92',
        27: '2% 3,94 0,83',
        28: 'DUTAL 43,97 3,56',
        29: 'A',
        30: 'AUT: 307029',
        31: 'uz 44101236',
        32: '+ PAGO TARJETA BANCARIA +',
        33: '- YUYODO3 101',
        34: '«13A CLASICA',
        35: 'SE ADMLIEN DEVOLUCIONES CON TiCkEf'
    },
}


def test_extract_text_lines_from_image_should_return_tested_dict():
    for filename in TEST_IMAGES_VALUES_FROM_FILE.keys():
        expected_result = TEST_IMAGES_VALUES_FROM_FILE[filename]
        fullpath = os.path.join(TEST_IMAGES_PATH, filename)
        assert expected_result == ocr_batch.extract_text_lines_from_image(fullpath)
