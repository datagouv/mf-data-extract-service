from dotenv import load_dotenv
from os.path import join, dirname
import os

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

MINIO_URL=os.environ.get("MINIO_URL")
MINIO_BUCKET=os.environ.get("MINIO_BUCKET")
MINIO_USER=os.environ.get("MINIO_USER")
MINIO_PASSWORD=os.environ.get("MINIO_PASSWORD")
APIKEY_DATAGOUV = os.environ.get("APIKEY_DATAGOUV")
APIKEY_AROME = os.environ.get("APIKEY_AROME")
APIKEY_ARPEGE = os.environ.get("APIKEY_ARPEGE")

DATAGOUV_URL="https://demo.data.gouv.fr"
# Nb of batch we want to retrieve (every 6 hours)
MAX_LAST_BATCHES = 1
BATCH_URL_SIZE = 50

# PACKAGES = [
#     {
#         "type_package": "arome",
#         "dataset_id": "65aade5a97e39e6c4cae5252",
#         "apikey": APIKEY_AROME,
#         "base_url": "https://public-api.meteofrance.fr/previnum/DPPaquetAROME/models/AROME/grids",
#         "product": "productARO",
#         "grid": "0.01",
#         "packages": [
#             {
#                 "name": "SP1",
#                 "time": ['01H', '02H']
#             }
#         ]
#     }
# ]

PACKAGES = [
    {
        "type_package": "arome",
        "dataset_id": "65aade5a97e39e6c4cae5252",
        "apikey": APIKEY_AROME,
        "base_url": "https://public-api.meteofrance.fr/previnum/DPPaquetAROME/models/AROME/grids",
        "product": "productARO",
        "grid": "0.01",
        "packages": [
            {
                "name": "SP1",
                "time": ['01H', '02H', '03H', '04H', '05H', '06H', '07H', '08H', '09H', '10H', '11H', '12H', '13H', '14H', '15H', '16H', '17H', '18H', '19H', '20H', '21H', '22H', '23H', '24H', '25H', '26H', '27H', '28H', '29H', '30H', '31H', '32H', '33H', '34H', '35H', '36H', '37H', '38H', '39H', '40H', '41H', '42H']
            },
            {
                "name": "SP2",
                "time": ['01H', '02H', '03H', '04H', '05H', '06H', '07H', '08H', '09H', '10H', '11H', '12H', '13H', '14H', '15H', '16H', '17H', '18H', '19H', '20H', '21H', '22H', '23H', '24H', '25H', '26H', '27H', '28H', '29H', '30H', '31H', '32H', '33H', '34H', '35H', '36H', '37H', '38H', '39H', '40H', '41H', '42H']
            },
            {
                "name": "SP3",
                "time": ['01H', '02H', '03H', '04H', '05H', '06H', '07H', '08H', '09H', '10H', '11H', '12H', '13H', '14H', '15H', '16H', '17H', '18H', '19H', '20H', '21H', '22H', '23H', '24H', '25H', '26H', '27H', '28H', '29H', '30H', '31H', '32H', '33H', '34H', '35H', '36H', '37H', '38H', '39H', '40H', '41H', '42H']
            },
            {
                "name": "HP1",
                "time": ['01H', '02H', '03H', '04H', '05H', '06H', '07H', '08H', '09H', '10H', '11H', '12H', '13H', '14H', '15H', '16H', '17H', '18H', '19H', '20H', '21H', '22H', '23H', '24H', '25H', '26H', '27H', '28H', '29H', '30H', '31H', '32H', '33H', '34H', '35H', '36H', '37H', '38H', '39H', '40H', '41H', '42H']
            }
        ]
    },
    {
        "type_package": "arome",
        "dataset_id": "65aadec3dc9e969fd00e71e8",
        "apikey": APIKEY_AROME,
        "base_url": "https://public-api.meteofrance.fr/previnum/DPPaquetAROME/models/AROME/grids",
        "product": "productARO",
        "grid": "0.025",
        "packages": [
            {
                "name": "IP1",
                "time": ["00H06H", "07H12H", "13H18H", "19H24H", "25H30H", "31H36H", "37H42H"]
            },
            {
                "name": "IP2",
                "time": ["00H06H", "07H12H", "13H18H", "19H24H", "25H30H", "31H36H", "37H42H"]
            },
            {
                "name": "IP3",
                "time": ["00H06H", "07H12H", "13H18H", "19H24H", "25H30H", "31H36H", "37H42H"]
            },
            {
                "name": "IP4",
                "time": ["00H06H", "07H12H", "13H18H", "19H24H", "25H30H", "31H36H", "37H42H"]
            },
            {
                "name": "IP5",
                "time": ["00H06H", "07H12H", "13H18H", "19H24H", "25H30H", "31H36H", "37H42H"]
            },
            {
                "name": "SP1",
                "time": ["00H06H", "07H12H", "13H18H", "19H24H", "25H30H", "31H36H", "37H42H"]
            },
            {
                "name": "SP2",
                "time": ["00H06H", "07H12H", "13H18H", "19H24H", "25H30H", "31H36H", "37H42H"]
            },
            {
                "name": "SP3",
                "time": ["00H06H", "07H12H", "13H18H", "19H24H", "25H30H", "31H36H", "37H42H"]
            },
            {
                "name": "HP1",
                "time": ["00H06H", "07H12H", "13H18H", "19H24H", "25H30H", "31H36H", "37H42H"]
            },
            {
                "name": "HP2",
                "time": ["00H06H", "07H12H", "13H18H", "19H24H", "25H30H", "31H36H", "37H42H"]
            },
            {
                "name": "HP3",
                "time": ["00H06H", "07H12H", "13H18H", "19H24H", "25H30H", "31H36H", "37H42H"]
            }
        ]
    },
    {
        "type_package": "arpege",
        "dataset_id": "65aaded8dc9e969fd00e71e9",
        "apikey": APIKEY_ARPEGE,
        "base_url": "https://public-api.meteofrance.fr/previnum/DPPaquetARPEGE/models/ARPEGE/grids",
        "product": "productARP",
        "grid": "0.1",
        "packages": [
            {
                "name": "IP1",
                "time": ["000H012H", "013H024H", "025H036H", "037H048H", "049H060H", "061H072H", "073H084H", "085H096H", "097H102H"]
            },
            {
                "name": "IP2",
                "time": ["000H012H", "013H024H", "025H036H", "037H048H", "049H060H", "061H072H", "073H084H", "085H096H", "097H102H"]
            },
            {
                "name": "IP3",
                "time": ["000H012H", "013H024H", "025H036H", "037H048H", "049H060H", "061H072H", "073H084H", "085H096H", "097H102H"]
            },
            {
                "name": "IP4",
                "time": ["000H012H", "013H024H", "025H036H", "037H048H", "049H060H", "061H072H", "073H084H", "085H096H", "097H102H"]
            },
            {
                "name": "SP1",
                "time": ["000H012H", "013H024H", "025H036H", "037H048H", "049H060H", "061H072H", "073H084H", "085H096H", "097H102H"]
            },
            {
                "name": "SP2",
                "time": ["000H012H", "013H024H", "025H036H", "037H048H", "049H060H", "061H072H", "073H084H", "085H096H", "097H102H"]
            },
            {
                "name": "HP1",
                "time": ["000H012H", "013H024H", "025H036H", "037H048H", "049H060H", "061H072H", "073H084H", "085H096H", "097H102H"]
            },
            {
                "name": "HP2",
                "time": ["000H012H", "013H024H", "025H036H", "037H048H", "049H060H", "061H072H", "073H084H", "085H096H", "097H102H"]
            }
        ]
    },
    {
        "type_package": "arpege",
        "dataset_id": "65aadeebdc9e969fd00e71ea",
        "apikey": APIKEY_ARPEGE,
        "base_url": "https://public-api.meteofrance.fr/previnum/DPPaquetARPEGE/models/ARPEGE/grids",
        "product": "productARP",
        "grid": "0.25",
        "packages": [
            {
                "name": "IP1",
                "time": ["000H024H", "025H048H", "049H072H", "073H102H"]
            },
            {
                "name": "IP2",
                "time": ["000H024H", "025H048H", "049H072H", "073H102H"]
            },
            {
                "name": "IP3",
                "time": ["000H024H", "025H048H", "049H072H", "073H102H"]
            },
            {
                "name": "IP4",
                "time": ["000H024H", "025H048H", "049H072H", "073H102H"]
            },
            {
                "name": "SP1",
                "time": ["000H024H", "025H048H", "049H072H", "073H102H"]
            },
            {
                "name": "SP2",
                "time": ["000H024H", "025H048H", "049H072H", "073H102H"]
            },
            {
                "name": "HP1",
                "time": ["000H024H", "025H048H", "049H072H", "073H102H"]
            },
            {
                "name": "HP2",
                "time": ["000H024H", "025H048H", "049H072H", "073H102H"]
            }
        ]
    }
]