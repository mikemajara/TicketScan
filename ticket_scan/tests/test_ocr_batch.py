#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import os

import cv2
import pytest
from ticket_scan.scanner import ocr_batch

TEST_IMAGES_PATH = 'test_resources'
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
    "8219702639756318720.jpeg": {
        0: 'LTDL SUPERMERCADOS 5.A.U.',
        1: 'Avenida Miguel de Cervantes N2 110',
        2: '30009 Murcia',
        3: 'NIF A60195278',
        4: 'WWW. 110d1.es',
        5: 'Flauta de cereales 1,50 B',
        6: 'Pechugas codorniz 3,69 B',
        7: 'Alcachofa unidad 1164',
        8: '4 x 0,29',
        9: 'Cápsulas Intenso 1,99 B',
        10: 'Cáps:: 1s Ristretto 1,99 B',
        11: 'Alitas de poilo 2,39 B',
        12: 'Champ “ón 0,69 A',
        13: 'e e e e e a a o A',
        14: 'Entregado Il, 20,42',
        15: 'IVAR. IVA +  PhNeto  =  FvYr',
        16: 'mt',
        17: 'Suma 1,12 19,29 13,41',
        18: '3508  039467/02 12,01 19 12:55',
        19: '- Devoluciones artículos de bazar con',
        20: 'ticket de compra y embalaje original',
        21: 'en un plazo máximo de 30 días sin',
        22: 'perjuicio de la ley de garantías.',
        23: 'Horario Tienda Lu a Sa 09:00 a 22:00',
        24: '| - Atención al cliente',
        25: 'www. 11d1.es/contacto Tel. 900958311',
        26: 'o GRACIAS POR SU VISITA'
    },
    "cropped_247_227.png": {0: 'Murcia'},
    "cropped_386_359.png": {0: '26/03/2019 20:54 0P; 11/2496'},
    "cropped_606_581.png": {0: '4 1 PICOS PACK-2 1,08'}
}
TESTED_DICT_EXTRACT_IMAGE_FROM_PATH = {
    '149533795324992.jpeg': '', # todo this happens because of the parameters.
    '8219702639756318720.jpeg': '', # if it weren't for the parameters in config, text would be extracted normally.
    'cropped_247_227.png': 'Murcia',
    'cropped_386_359.png': '26/03/2019 20:54 0P; 11/2496',
    'cropped_606_581.png': '4 1 PICOS PACK-2 1,08'
}


def test_save_dict_to_file_should_create_file_with_dict_content():
    dictionary = {
        '0': 'line 0',
        '1': 'line 1',
    }
    fullpath = os.path.join(TEST_IMAGES_PATH, 'file.json')
    ocr_batch.save_dict_to_file(fullpath, dictionary)
    assert os.path.isfile(fullpath)
    with open(fullpath, "r") as f:
        real_output = json.load(f)
    expected_output = dictionary.copy()
    assert expected_output == real_output


def test_get_sorted_file_list_for_path_with_no_prefix_should_return_all_files():
    expected_value = sorted(os.listdir(TEST_IMAGES_PATH))
    real_value = ocr_batch.get_sorted_file_list_for_path(TEST_IMAGES_PATH)
    assert expected_value == real_value


def test_get_sorted_file_list_for_path_with_cropped_prefix_should_return_cropped_files():
    expected_value = [filename for filename in sorted(os.listdir(TEST_IMAGES_PATH)) if "cropped" in filename]
    real_value = ocr_batch.get_sorted_file_list_for_path(TEST_IMAGES_PATH, prefixes=["cropped"])
    assert expected_value == real_value


def test_get_sorted_file_list_for_path_with_jpeg_json_suffix_should_return_jpeg_json_files():
    expected_value = [
        filename for filename in sorted(os.listdir(TEST_IMAGES_PATH))
        if "jpeg" in filename or "json" in filename
    ]
    real_value = ocr_batch.get_sorted_file_list_for_path(TEST_IMAGES_PATH, suffixes=["jpeg", "json"])
    assert expected_value == real_value


def test_extract_text_lines_from_path_for_jpeg_png_should_return_tested_dict():
    expected_result = TESTED_DICT_EXTRACT_IMAGE_FROM_PATH
    fullpath = os.path.join(TEST_IMAGES_PATH)
    assert expected_result == ocr_batch.extract_text_lines_from_path(fullpath, suffixes=["jpeg"])


def test_extract_text_lines_from_image_should_return_tested_dict():
    for filename in TEST_IMAGES_VALUES_FROM_FILE.keys():
        expected_result = TEST_IMAGES_VALUES_FROM_FILE[filename]
        fullpath = os.path.join(TEST_IMAGES_PATH, filename)
        assert expected_result == ocr_batch.extract_text_lines_from_image(fullpath)
