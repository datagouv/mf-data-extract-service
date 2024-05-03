from dotenv import load_dotenv
from os.path import join, dirname
import os

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

ENV_NAME = os.environ.get("ENV_NAME")
MINIO_URL = os.environ.get("MINIO_URL")
MINIO_PUBLIC_URL = os.environ.get("MINIO_PUBLIC_URL")
MINIO_BUCKET = os.environ.get("MINIO_BUCKET")
MINIO_USER = os.environ.get("MINIO_USER")
MINIO_PASSWORD = os.environ.get("MINIO_PASSWORD")
MINIO_SECURE = eval(os.environ.get("MINIO_SECURE"))
APIKEY_DATAGOUV = os.environ.get("APIKEY_DATAGOUV")
APIKEY_AROME = os.environ.get("APIKEY_AROME")
APIKEY_ARPEGE = os.environ.get("APIKEY_ARPEGE")
APIKEY_AROME_OM = os.environ.get("APIKEY_AROME_OM")
APIKEY_VAGUE_SURCOTE = os.environ.get("APIKEY_VAGUE_SURCOTE")
DATAGOUV_URL = os.environ.get("DATAGOUV_URL")

# Nb of batch we want to retrieve (every 6 hours)
MAX_LAST_BATCHES = 3
BATCH_URL_SIZE = 50

BATCH_URL_SIZE_PACKAGE = {
    "arome": 40,
    "arpege": 40,
    "arome-om": 340,
    "vague-surcote": 90
}

PACKAGES = [
    {
        "type_package": "vague-surcote",
        "detail_package": "MFWAM",
        "dataset_id_dev": "65b68c83b833790f93a4ab27",
        "dataset_id_prod": "65bd1a505a5b412989a84ca7",
        "apikey": APIKEY_VAGUE_SURCOTE,
        "base_url": "https://public-api.meteofrance.fr/previnum/DPPaquetWAVESMODELS/models/MFWAM/grids",
        "check_availability_url": "https://public-api.meteofrance.fr/previnum/DPPaquetWAVESMODELS/models/MFWAM/grids/0.025/packages/SP1",
        "product": "productMFWAM",
        "grid": "0.025",
        "extension": "grib2",
        "packages": [
            {
                "name": "SP1",
                "time": ['001H', '002H', '003H', '004H', '005H', '006H', '007H', '008H', '009H', '010H', '011H', '012H', '013H', '014H', '015H', '016H', '017H', '018H', '019H', '020H', '021H', '022H', '023H', '024H', '025H', '026H', '027H', '028H', '029H', '030H', '031H', '032H', '033H', '034H', '035H', '036H', '037H', '038H', '039H', '040H', '041H', '042H', '043H', '044H', '045H', '046H', '047H', '048H']
            }
        ]
    },
    {
        "type_package": "vague-surcote",
        "detail_package": "MFWAM",
        "dataset_id_dev": "65b68c841a2bd22881b8e487",
        "dataset_id_prod": "65bd1a2957e1cc7c9625e7b5",
        "apikey": APIKEY_VAGUE_SURCOTE,
        "base_url": "https://public-api.meteofrance.fr/previnum/DPPaquetWAVESMODELS/models/MFWAM/grids",
        "check_availability_url": "https://public-api.meteofrance.fr/previnum/DPPaquetWAVESMODELS/models/MFWAM/grids/0.1/packages/SP1",
        "product": "productMFWAM",
        "grid": "0.1",
        "extension": "grib2",
        "packages": [
            {
                "name": "SP1",
                "time": [
                    '001H', '002H', '003H', '004H', '005H', '006H', '007H', '008H', '009H',
                    '010H', '011H', '012H', '013H', '014H', '015H', '016H', '017H', '018H', '019H',
                    '020H', '021H', '022H', '023H', '024H', '025H', '026H', '027H', '028H', '029H',
                    '030H', '031H', '032H', '033H', '034H', '035H', '036H', '037H', '038H', '039H',
                    '040H', '041H', '042H', '043H', '044H', '045H', '046H', '047H', '048H',
                    '051H', '054H', '057H',
                    '060H', '063H', '066H', '069H',
                    '072H', '075H', '078H',
                    '081H', '084H', '087H',
                    '090H', '093H', '096H', '099H',
                    '102H'
                ]
            }
        ]
    },
    {
        "type_package": "vague-surcote",
        "detail_package": "MFWAM",
        "dataset_id_dev": "65b68c841a2bd22881b8e488",
        "dataset_id_prod": "65bd19fe0d61026813636c33",
        "apikey": APIKEY_VAGUE_SURCOTE,
        "base_url": "https://public-api.meteofrance.fr/previnum/DPPaquetWAVESMODELS/models/MFWAM/grids",
        "check_availability_url": "https://public-api.meteofrance.fr/previnum/DPPaquetWAVESMODELS/models/MFWAM/grids/0.5/packages/SP1",
        "product": "productMFWAM",
        "grid": "0.5",
        "extension": "grib2",
        "packages": [
            {
                "name": "SP1",
                "time": [
                    '001H', '002H', '003H', '004H', '005H', '006H', '007H', '008H', '009H',
                    '010H', '011H', '012H', '013H', '014H', '015H', '016H', '017H', '018H', '019H',
                    '020H', '021H', '022H', '023H', '024H', '025H', '026H', '027H', '028H', '029H',
                    '030H', '031H', '032H', '033H', '034H', '035H', '036H', '037H', '038H', '039H',
                    '040H', '041H', '042H', '043H', '044H', '045H', '046H', '047H', '048H',
                    '051H', '054H', '057H',
                    '060H', '063H', '066H', '069H',
                    '072H', '075H', '078H',
                    '081H', '084H', '087H',
                    '090H', '093H', '096H', '099H',
                    '102H'
                ]
            }
        ]
    },
    {
        "type_package": "vague-surcote",
        "detail_package": "WW3-MARP",
        "dataset_id_dev": "65b68c840053e6459a859ccf",
        "dataset_id_prod": "65bd19a20a9351d1cbe9a090",
        "apikey": APIKEY_VAGUE_SURCOTE,
        "base_url": "https://public-api.meteofrance.fr/previnum/DPPaquetWAVESMODELS/models/WW3-MARP/grids",
        "check_availability_url": "https://public-api.meteofrance.fr/previnum/DPPaquetWAVESMODELS/models/WW3-MARP/grids/0.01/packages/SP1",
        "product": "productWMARP",
        "grid": "0.01",
        "extension": "nc",
        "packages": [
            {
                "name": "SP1",
                "time": ['000H999H']
            }
        ]
    },
    {
        "type_package": "vague-surcote",
        "detail_package": "WW3-WARP",
        "dataset_id_dev": "65b68c8580a75b6c6bae3d66",
        "dataset_id_prod": "65bd197cd4222b0c96db759e",
        "apikey": APIKEY_VAGUE_SURCOTE,
        "base_url": "https://public-api.meteofrance.fr/previnum/DPPaquetWAVESMODELS/models/WW3-WARP/grids",
        "check_availability_url": "https://public-api.meteofrance.fr/previnum/DPPaquetWAVESMODELS/models/WW3-WARP/grids/0.01/packages/SP1",
        "product": "productWWARP",
        "grid": "0.01",
        "extension": "nc",
        "packages": [
            {
                "name": "SP1",
                "time": ['000H999H']
            }
        ]
    },
    {
        "type_package": "vague-surcote",
        "detail_package": "WW3-MARO",
        "dataset_id_dev": "65b68c852bb8441329433a30",
        "dataset_id_prod": "65bd19226c4e3fcbf4948f99",
        "apikey": APIKEY_VAGUE_SURCOTE,
        "base_url": "https://public-api.meteofrance.fr/previnum/DPPaquetWAVESMODELS/models/WW3-MARO/grids",
        "check_availability_url": "https://public-api.meteofrance.fr/previnum/DPPaquetWAVESMODELS/models/WW3-MARO/grids/0.01/packages/SP1",
        "product": "productWMARO",
        "grid": "0.01",
        "extension": "nc",
        "packages": [
            {
                "name": "SP1",
                "time": ['000H999H']
            }
        ]
    },
    {
        "type_package": "vague-surcote",
        "detail_package": "HYCOM2D-MARP",
        "dataset_id_dev": "65b68c8580a75b6c6bae3d67",
        "dataset_id_prod": "65bd183c9ec6ae3f87a5334a",
        "apikey": APIKEY_VAGUE_SURCOTE,
        "base_url": "https://public-api.meteofrance.fr/previnum/DPPaquetWAVESMODELS/models/HYCOM2D-MARP/grids",
        "check_availability_url": "https://public-api.meteofrance.fr/previnum/DPPaquetWAVESMODELS/models/HYCOM2D-MARP/grids/0.04/packages/SP1",
        "product": "productHMARP",
        "grid": "0.04",
        "extension": "grib2",
        "packages": [
            {
                "name": "SP1",
                "time": [
                    '000H', '001H', '002H', '003H', '004H', '005H', '006H', '007H', '008H', '009H',
                    '010H', '011H', '012H', '013H', '014H', '015H', '016H', '017H', '018H', '019H',
                    '020H', '021H', '022H', '023H', '024H', '025H', '026H', '027H', '028H', '029H',
                    '030H', '031H', '032H', '033H', '034H', '035H', '036H', '037H', '038H', '039H',
                    '040H', '041H', '042H', '043H', '044H', '045H', '046H', '047H', '048H', '049H',
                    '050H', '051H', '052H', '053H', '054H', '055H', '056H', '057H', '058H', '059H',
                    '060H', '061H', '062H', '063H', '064H', '065H', '066H', '067H', '068H', '069H',
                    '070H', '071H', '072H', '073H', '074H', '075H', '076H', '077H', '078H', '079H',
                    '080H', '081H', '082H', '083H', '084H', '085H', '086H', '087H', '088H', '089H',
                    '090H', '091H', '092H', '093H', '094H', '095H', '096H', '097H', '098H', '099H',
                    '100H', '101H', '102H'
                ]
            }
        ]
    },
    {
        "type_package": "vague-surcote",
        "detail_package": "HYCOM2D-WARP",
        "dataset_id_dev": "65b68c850e237844c20fd501",
        "dataset_id_prod": "65bd17fe9ec6ae3f87a53349",
        "apikey": APIKEY_VAGUE_SURCOTE,
        "base_url": "https://public-api.meteofrance.fr/previnum/DPPaquetWAVESMODELS/models/HYCOM2D-WARP/grids",
        "check_availability_url": "https://public-api.meteofrance.fr/previnum/DPPaquetWAVESMODELS/models/HYCOM2D-WARP/grids/0.04/packages/SP1",
        "product": "productHWARP",
        "grid": "0.04",
        "extension": "grib2",
        "packages": [
            {
                "name": "SP1",
                "time": [
                    '000H', '001H', '002H', '003H', '004H', '005H', '006H', '007H', '008H', '009H',
                    '010H', '011H', '012H', '013H', '014H', '015H', '016H', '017H', '018H', '019H',
                    '020H', '021H', '022H', '023H', '024H', '025H', '026H', '027H', '028H', '029H',
                    '030H', '031H', '032H', '033H', '034H', '035H', '036H', '037H', '038H', '039H',
                    '040H', '041H', '042H', '043H', '044H', '045H', '046H', '047H', '048H', '049H',
                    '050H', '051H', '052H', '053H', '054H', '055H', '056H', '057H', '058H', '059H',
                    '060H', '061H', '062H', '063H', '064H', '065H', '066H', '067H', '068H', '069H',
                    '070H', '071H', '072H', '073H', '074H', '075H', '076H', '077H', '078H', '079H',
                    '080H', '081H', '082H', '083H', '084H', '085H', '086H', '087H', '088H', '089H',
                    '090H', '091H', '092H', '093H', '094H', '095H', '096H', '097H', '098H', '099H',
                    '100H', '101H', '102H'
                ]
            }
        ]
    },
    {
        "type_package": "vague-surcote",
        "detail_package": "HYCOM2D-WARO",
        "dataset_id_dev": "65b68c8545f1789c428c8907",
        "dataset_id_prod": "65bd17b9775b5222832d67a4",
        "apikey": APIKEY_VAGUE_SURCOTE,
        "base_url": "https://public-api.meteofrance.fr/previnum/DPPaquetWAVESMODELS/models/HYCOM2D-WARO/grids",
        "check_availability_url": "https://public-api.meteofrance.fr/previnum/DPPaquetWAVESMODELS/models/HYCOM2D-WARO/grids/0.04/packages/SP1",
        "product": "productHWARO",
        "grid": "0.04",
        "extension": "grib2",
        "packages": [
            {
                "name": "SP1",
                "time": [
                    '000H', '001H', '002H', '003H', '004H', '005H', '006H', '007H', '008H', '009H',
                    '010H', '011H', '012H', '013H', '014H', '015H', '016H', '017H', '018H', '019H',
                    '020H', '021H', '022H', '023H', '024H', '025H', '026H', '027H', '028H', '029H',
                    '030H', '031H', '032H', '033H', '034H', '035H', '036H', '037H', '038H', '039H',
                    '040H', '041H', '042H', '043H', '044H', '045H', '046H', '047H', '048H', '049H',
                    '050H', '051H'
                ]
            }
        ]
    },
    {
        "type_package": "vague-surcote",
        "detail_package": "HYCOM2D-MARO",
        "dataset_id_dev": "65b68c860e237844c20fd502",
        "dataset_id_prod": "65bd17779ec6ae3f87a53348",
        "apikey": APIKEY_VAGUE_SURCOTE,
        "base_url": "https://public-api.meteofrance.fr/previnum/DPPaquetWAVESMODELS/models/HYCOM2D-MARO/grids",
        "check_availability_url": "https://public-api.meteofrance.fr/previnum/DPPaquetWAVESMODELS/models/HYCOM2D-MARO/grids/0.04/packages/SP1",
        "product": "productHMARO",
        "grid": "0.04",
        "extension": "grib2",
        "packages": [
            {
                "name": "SP1",
                "time": [
                    '000H', '001H', '002H', '003H', '004H', '005H', '006H', '007H', '008H', '009H',
                    '010H', '011H', '012H', '013H', '014H', '015H', '016H', '017H', '018H', '019H',
                    '020H', '021H', '022H', '023H', '024H', '025H', '026H', '027H', '028H', '029H',
                    '030H', '031H', '032H', '033H', '034H', '035H', '036H', '037H', '038H', '039H',
                    '040H', '041H', '042H', '043H', '044H', '045H', '046H', '047H', '048H', '049H',
                    '050H', '051H'
                ]
            }
        ]
    },
    {
        "type_package": "arome-om",
        "detail_package": "ANTIL",
        "dataset_id_dev": "65b68c862bb8441329433a31",
        "dataset_id_prod": "65bd162b9dc0d31edfabc2b9",
        "apikey": APIKEY_AROME_OM,
        "base_url": "https://public-api.meteofrance.fr/previnum/DPPaquetAROME-OM/v1/models/AROME-OM-ANTIL/grids",
        "check_availability_url": "https://public-api.meteofrance.fr/previnum/DPPaquetAROME-OM/models/AROME-OM-ANTIL/grids/0.025/packages/IP1",
        "product": "productOMAN",
        "grid": "0.025",
        "extension": "grib2",
        "packages": [
            {
                "name": "IP1",
                "time": [
                    '000H', '001H', '002H', '003H', '004H', '005H', '006H', '007H', '008H', '009H',
                    '010H', '011H', '012H', '013H', '014H', '015H', '016H', '017H', '018H', '019H',
                    '020H', '021H', '022H', '023H', '024H', '025H', '026H', '027H', '028H', '029H',
                    '030H', '031H', '032H', '033H', '034H', '035H', '036H', '037H', '038H', '039H',
                    '040H', '041H', '042H', '043H', '044H', '045H', '046H', '047H', '048H'
                ]
            },
            {
                "name": "IP2",
                "time": [
                    '000H', '001H', '002H', '003H', '004H', '005H', '006H', '007H', '008H', '009H',
                    '010H', '011H', '012H', '013H', '014H', '015H', '016H', '017H', '018H', '019H',
                    '020H', '021H', '022H', '023H', '024H', '025H', '026H', '027H', '028H', '029H',
                    '030H', '031H', '032H', '033H', '034H', '035H', '036H', '037H', '038H', '039H',
                    '040H', '041H', '042H', '043H', '044H', '045H', '046H', '047H', '048H'
                ]
            },
            {
                "name": "IP3",
                "time": [
                    '000H', '001H', '002H', '003H', '004H', '005H', '006H', '007H', '008H', '009H',
                    '010H', '011H', '012H', '013H', '014H', '015H', '016H', '017H', '018H', '019H',
                    '020H', '021H', '022H', '023H', '024H', '025H', '026H', '027H', '028H', '029H',
                    '030H', '031H', '032H', '033H', '034H', '035H', '036H', '037H', '038H', '039H',
                    '040H', '041H', '042H', '043H', '044H', '045H', '046H', '047H', '048H'
                ]
            },
            {
                "name": "IP4",
                "time": [
                    '001H', '002H', '003H', '004H', '005H', '006H', '007H', '008H', '009H', '010H',
                    '011H', '012H', '013H', '014H', '015H', '016H', '017H', '018H', '019H', '020H',
                    '021H', '022H', '023H', '024H', '025H', '026H', '027H', '028H', '029H', '030H',
                    '031H', '032H', '033H', '034H', '035H', '036H', '037H', '038H', '039H', '040H',
                    '041H', '042H', '043H', '044H', '045H', '046H', '047H', '048H'
                ]
            },
            {
                "name": "IP5",
                "time": [
                    '000H', '001H', '002H', '003H', '004H', '005H', '006H', '007H', '008H', '009H',
                    '010H', '011H', '012H', '013H', '014H', '015H', '016H', '017H', '018H', '019H',
                    '020H', '021H', '022H', '023H', '024H', '025H', '026H', '027H', '028H', '029H',
                    '030H', '031H', '032H', '033H', '034H', '035H', '036H', '037H', '038H', '039H',
                    '040H', '041H', '042H', '043H', '044H', '045H', '046H', '047H', '048H'
                ]
            },
            {
                "name": "SP1",
                "time": [
                    '000H', '001H', '002H', '003H', '004H', '005H', '006H', '007H', '008H', '009H',
                    '010H', '011H', '012H', '013H', '014H', '015H', '016H', '017H', '018H', '019H',
                    '020H', '021H', '022H', '023H', '024H', '025H', '026H', '027H', '028H', '029H',
                    '030H', '031H', '032H', '033H', '034H', '035H', '036H', '037H', '038H', '039H',
                    '040H', '041H', '042H', '043H', '044H', '045H', '046H', '047H', '048H'
                ]
            },
            {
                "name": "SP2",
                "time": [
                    '000H', '001H', '002H', '003H', '004H', '005H', '006H', '007H', '008H', '009H',
                    '010H', '011H', '012H', '013H', '014H', '015H', '016H', '017H', '018H', '019H',
                    '020H', '021H', '022H', '023H', '024H', '025H', '026H', '027H', '028H', '029H',
                    '030H', '031H', '032H', '033H', '034H', '035H', '036H', '037H', '038H', '039H',
                    '040H', '041H', '042H', '043H', '044H', '045H', '046H', '047H', '048H'
                ]
            },
            {
                "name": "SP3",
                "time": [
                    '000H', '001H', '002H', '003H', '004H', '005H', '006H', '007H', '008H', '009H',
                    '010H', '011H', '012H', '013H', '014H', '015H', '016H', '017H', '018H', '019H',
                    '020H', '021H', '022H', '023H', '024H', '025H', '026H', '027H', '028H', '029H',
                    '030H', '031H', '032H', '033H', '034H', '035H', '036H', '037H', '038H', '039H',
                    '040H', '041H', '042H', '043H', '044H', '045H', '046H', '047H', '048H'
                ]
            },
            {
                "name": "HP1",
                "time": [
                    '000H', '001H', '002H', '003H', '004H', '005H', '006H', '007H', '008H', '009H',
                    '010H', '011H', '012H', '013H', '014H', '015H', '016H', '017H', '018H', '019H',
                    '020H', '021H', '022H', '023H', '024H', '025H', '026H', '027H', '028H', '029H',
                    '030H', '031H', '032H', '033H', '034H', '035H', '036H', '037H', '038H', '039H',
                    '040H', '041H', '042H', '043H', '044H', '045H', '046H', '047H', '048H'
                ]
            },
            {
                "name": "HP2",
                "time": [
                    '000H', '001H', '002H', '003H', '004H', '005H', '006H', '007H', '008H', '009H',
                    '010H', '011H', '012H', '013H', '014H', '015H', '016H', '017H', '018H', '019H',
                    '020H', '021H', '022H', '023H', '024H', '025H', '026H', '027H', '028H', '029H',
                    '030H', '031H', '032H', '033H', '034H', '035H', '036H', '037H', '038H', '039H',
                    '040H', '041H', '042H', '043H', '044H', '045H', '046H', '047H', '048H'
                ]
            },
            {
                "name": "HP3",
                "time": [
                    '001H', '002H', '003H', '004H', '005H', '006H', '007H', '008H', '009H', '010H',
                    '011H', '012H', '013H', '014H', '015H', '016H', '017H', '018H', '019H', '020H',
                    '021H', '022H', '023H', '024H', '025H', '026H', '027H', '028H', '029H', '030H',
                    '031H', '032H', '033H', '034H', '035H', '036H', '037H', '038H', '039H', '040H',
                    '041H', '042H', '043H', '044H', '045H', '046H', '047H', '048H'
                ]
            }
        ]
    },
    {
        "type_package": "arome-om",
        "detail_package": "GUYANE",
        "dataset_id_dev": "65b68c860053e6459a859cd0",
        "dataset_id_prod": "65e0bd4b88e4fd88b989ba46",
        "apikey": APIKEY_AROME_OM,
        "base_url": "https://public-api.meteofrance.fr/previnum/DPPaquetAROME-OM/models/AROME-OM-GUYANE/grids",
        "check_availability_url": "https://public-api.meteofrance.fr/previnum/DPPaquetAROME-OM/models/AROME-OM-GUYANE/grids/0.025/packages/IP1",
        "product": "productOMGU",
        "grid": "0.025",
        "extension": "grib2",
        "packages": [
            {
                "name": "IP1",
                "time": [
                    '000H', '001H', '002H', '003H', '004H', '005H', '006H', '007H', '008H', '009H',
                    '010H', '011H', '012H', '013H', '014H', '015H', '016H', '017H', '018H', '019H',
                    '020H', '021H', '022H', '023H', '024H', '025H', '026H', '027H', '028H', '029H',
                    '030H', '031H', '032H', '033H', '034H', '035H', '036H', '037H', '038H', '039H',
                    '040H', '041H', '042H', '043H', '044H', '045H', '046H', '047H', '048H'
                ]
            },
            {
                "name": "IP2",
                "time": [
                    '000H', '001H', '002H', '003H', '004H', '005H', '006H', '007H', '008H', '009H',
                    '010H', '011H', '012H', '013H', '014H', '015H', '016H', '017H', '018H', '019H',
                    '020H', '021H', '022H', '023H', '024H', '025H', '026H', '027H', '028H', '029H',
                    '030H', '031H', '032H', '033H', '034H', '035H', '036H', '037H', '038H', '039H',
                    '040H', '041H', '042H', '043H', '044H', '045H', '046H', '047H', '048H'
                ]
            },
            {
                "name": "IP3",
                "time": [
                    '000H', '001H', '002H', '003H', '004H', '005H', '006H', '007H', '008H', '009H',
                    '010H', '011H', '012H', '013H', '014H', '015H', '016H', '017H', '018H', '019H',
                    '020H', '021H', '022H', '023H', '024H', '025H', '026H', '027H', '028H', '029H',
                    '030H', '031H', '032H', '033H', '034H', '035H', '036H', '037H', '038H', '039H',
                    '040H', '041H', '042H', '043H', '044H', '045H', '046H', '047H', '048H'
                ]
            },
            {
                "name": "IP4",
                "time": [
                    '001H', '002H', '003H', '004H', '005H', '006H', '007H', '008H', '009H', '010H',
                    '011H', '012H', '013H', '014H', '015H', '016H', '017H', '018H', '019H', '020H',
                    '021H', '022H', '023H', '024H', '025H', '026H', '027H', '028H', '029H', '030H',
                    '031H', '032H', '033H', '034H', '035H', '036H', '037H', '038H', '039H', '040H',
                    '041H', '042H', '043H', '044H', '045H', '046H', '047H', '048H'
                ]
            },
            {
                "name": "IP5",
                "time": [
                    '000H', '001H', '002H', '003H', '004H', '005H', '006H', '007H', '008H', '009H',
                    '010H', '011H', '012H', '013H', '014H', '015H', '016H', '017H', '018H', '019H',
                    '020H', '021H', '022H', '023H', '024H', '025H', '026H', '027H', '028H', '029H',
                    '030H', '031H', '032H', '033H', '034H', '035H', '036H', '037H', '038H', '039H',
                    '040H', '041H', '042H', '043H', '044H', '045H', '046H', '047H', '048H'
                ]
            },
            {
                "name": "SP1",
                "time": [
                    '000H', '001H', '002H', '003H', '004H', '005H', '006H', '007H', '008H', '009H',
                    '010H', '011H', '012H', '013H', '014H', '015H', '016H', '017H', '018H', '019H',
                    '020H', '021H', '022H', '023H', '024H', '025H', '026H', '027H', '028H', '029H',
                    '030H', '031H', '032H', '033H', '034H', '035H', '036H', '037H', '038H', '039H',
                    '040H', '041H', '042H', '043H', '044H', '045H', '046H', '047H', '048H'
                ]
            },
            {
                "name": "SP2",
                "time": [
                    '000H', '001H', '002H', '003H', '004H', '005H', '006H', '007H', '008H', '009H',
                    '010H', '011H', '012H', '013H', '014H', '015H', '016H', '017H', '018H', '019H',
                    '020H', '021H', '022H', '023H', '024H', '025H', '026H', '027H', '028H', '029H',
                    '030H', '031H', '032H', '033H', '034H', '035H', '036H', '037H', '038H', '039H',
                    '040H', '041H', '042H', '043H', '044H', '045H', '046H', '047H', '048H'
                ]
            },
            {
                "name": "SP3",
                "time": [
                    '000H', '001H', '002H', '003H', '004H', '005H', '006H', '007H', '008H', '009H',
                    '010H', '011H', '012H', '013H', '014H', '015H', '016H', '017H', '018H', '019H',
                    '020H', '021H', '022H', '023H', '024H', '025H', '026H', '027H', '028H', '029H',
                    '030H', '031H', '032H', '033H', '034H', '035H', '036H', '037H', '038H', '039H',
                    '040H', '041H', '042H', '043H', '044H', '045H', '046H', '047H', '048H'
                ]
            },
            {
                "name": "HP1",
                "time": [
                    '000H', '001H', '002H', '003H', '004H', '005H', '006H', '007H', '008H', '009H',
                    '010H', '011H', '012H', '013H', '014H', '015H', '016H', '017H', '018H', '019H',
                    '020H', '021H', '022H', '023H', '024H', '025H', '026H', '027H', '028H', '029H',
                    '030H', '031H', '032H', '033H', '034H', '035H', '036H', '037H', '038H', '039H',
                    '040H', '041H', '042H', '043H', '044H', '045H', '046H', '047H', '048H'
                ]
            },
            {
                "name": "HP2",
                "time": [
                    '000H', '001H', '002H', '003H', '004H', '005H', '006H', '007H', '008H', '009H',
                    '010H', '011H', '012H', '013H', '014H', '015H', '016H', '017H', '018H', '019H',
                    '020H', '021H', '022H', '023H', '024H', '025H', '026H', '027H', '028H', '029H',
                    '030H', '031H', '032H', '033H', '034H', '035H', '036H', '037H', '038H', '039H',
                    '040H', '041H', '042H', '043H', '044H', '045H', '046H', '047H', '048H'
                ]
            },
            {
                "name": "HP3",
                "time": [
                    '001H', '002H', '003H', '004H', '005H', '006H', '007H', '008H', '009H', '010H',
                    '011H', '012H', '013H', '014H', '015H', '016H', '017H', '018H', '019H', '020H',
                    '021H', '022H', '023H', '024H', '025H', '026H', '027H', '028H', '029H', '030H',
                    '031H', '032H', '033H', '034H', '035H', '036H', '037H', '038H', '039H', '040H',
                    '041H', '042H', '043H', '044H', '045H', '046H', '047H', '048H'
                ]
            }
        ]
    },
    {
        "type_package": "arome-om",
        "detail_package": "INDIEN",
        "dataset_id_dev": "65b68c860053e6459a859cd1",
        "dataset_id_prod": "65bd1560c73941a5e0ec1891",
        "apikey": APIKEY_AROME_OM,
        "base_url": "https://public-api.meteofrance.fr/previnum/DPPaquetAROME-OM/models/AROME-OM-INDIEN/grids",
        "check_availability_url": "https://public-api.meteofrance.fr/previnum/DPPaquetAROME-OM/models/AROME-OM-INDIEN/grids/0.025/packages/IP1",
        "product": "productOMOI",
        "grid": "0.025",
        "extension": "grib2",
        "packages": [
            {
                "name": "IP1",
                "time": [
                    '000H', '001H', '002H', '003H', '004H', '005H', '006H', '007H', '008H', '009H',
                    '010H', '011H', '012H', '013H', '014H', '015H', '016H', '017H', '018H', '019H',
                    '020H', '021H', '022H', '023H', '024H', '025H', '026H', '027H', '028H', '029H',
                    '030H', '031H', '032H', '033H', '034H', '035H', '036H', '037H', '038H', '039H',
                    '040H', '041H', '042H', '043H', '044H', '045H', '046H', '047H', '048H'
                ]
            },
            {
                "name": "IP2",
                "time": [
                    '000H', '001H', '002H', '003H', '004H', '005H', '006H', '007H', '008H', '009H',
                    '010H', '011H', '012H', '013H', '014H', '015H', '016H', '017H', '018H', '019H',
                    '020H', '021H', '022H', '023H', '024H', '025H', '026H', '027H', '028H', '029H',
                    '030H', '031H', '032H', '033H', '034H', '035H', '036H', '037H', '038H', '039H',
                    '040H', '041H', '042H', '043H', '044H', '045H', '046H', '047H', '048H'
                ]
            },
            {
                "name": "IP3",
                "time": [
                    '000H', '001H', '002H', '003H', '004H', '005H', '006H', '007H', '008H', '009H',
                    '010H', '011H', '012H', '013H', '014H', '015H', '016H', '017H', '018H', '019H',
                    '020H', '021H', '022H', '023H', '024H', '025H', '026H', '027H', '028H', '029H',
                    '030H', '031H', '032H', '033H', '034H', '035H', '036H', '037H', '038H', '039H',
                    '040H', '041H', '042H', '043H', '044H', '045H', '046H', '047H', '048H'
                ]
            },
            {
                "name": "IP4",
                "time": [
                    '001H', '002H', '003H', '004H', '005H', '006H', '007H', '008H', '009H', '010H',
                    '011H', '012H', '013H', '014H', '015H', '016H', '017H', '018H', '019H', '020H',
                    '021H', '022H', '023H', '024H', '025H', '026H', '027H', '028H', '029H', '030H',
                    '031H', '032H', '033H', '034H', '035H', '036H', '037H', '038H', '039H', '040H',
                    '041H', '042H', '043H', '044H', '045H', '046H', '047H', '048H'
                ]
            },
            {
                "name": "IP5",
                "time": [
                    '000H', '001H', '002H', '003H', '004H', '005H', '006H', '007H', '008H', '009H',
                    '010H', '011H', '012H', '013H', '014H', '015H', '016H', '017H', '018H', '019H',
                    '020H', '021H', '022H', '023H', '024H', '025H', '026H', '027H', '028H', '029H',
                    '030H', '031H', '032H', '033H', '034H', '035H', '036H', '037H', '038H', '039H',
                    '040H', '041H', '042H', '043H', '044H', '045H', '046H', '047H', '048H'
                ]
            },
            {
                "name": "SP1",
                "time": [
                    '000H', '001H', '002H', '003H', '004H', '005H', '006H', '007H', '008H', '009H',
                    '010H', '011H', '012H', '013H', '014H', '015H', '016H', '017H', '018H', '019H',
                    '020H', '021H', '022H', '023H', '024H', '025H', '026H', '027H', '028H', '029H',
                    '030H', '031H', '032H', '033H', '034H', '035H', '036H', '037H', '038H', '039H',
                    '040H', '041H', '042H', '043H', '044H', '045H', '046H', '047H', '048H'
                ]
            },
            {
                "name": "SP2",
                "time": [
                    '000H', '001H', '002H', '003H', '004H', '005H', '006H', '007H', '008H', '009H',
                    '010H', '011H', '012H', '013H', '014H', '015H', '016H', '017H', '018H', '019H',
                    '020H', '021H', '022H', '023H', '024H', '025H', '026H', '027H', '028H', '029H',
                    '030H', '031H', '032H', '033H', '034H', '035H', '036H', '037H', '038H', '039H',
                    '040H', '041H', '042H', '043H', '044H', '045H', '046H', '047H', '048H'
                ]
            },
            {
                "name": "SP3",
                "time": [
                    '000H', '001H', '002H', '003H', '004H', '005H', '006H', '007H', '008H', '009H',
                    '010H', '011H', '012H', '013H', '014H', '015H', '016H', '017H', '018H', '019H',
                    '020H', '021H', '022H', '023H', '024H', '025H', '026H', '027H', '028H', '029H',
                    '030H', '031H', '032H', '033H', '034H', '035H', '036H', '037H', '038H', '039H',
                    '040H', '041H', '042H', '043H', '044H', '045H', '046H', '047H', '048H'
                ]
            },
            {
                "name": "HP1",
                "time": [
                    '000H', '001H', '002H', '003H', '004H', '005H', '006H', '007H', '008H', '009H',
                    '010H', '011H', '012H', '013H', '014H', '015H', '016H', '017H', '018H', '019H',
                    '020H', '021H', '022H', '023H', '024H', '025H', '026H', '027H', '028H', '029H',
                    '030H', '031H', '032H', '033H', '034H', '035H', '036H', '037H', '038H', '039H',
                    '040H', '041H', '042H', '043H', '044H', '045H', '046H', '047H', '048H'
                ]
            },
            {
                "name": "HP2",
                "time": [
                    '000H', '001H', '002H', '003H', '004H', '005H', '006H', '007H', '008H', '009H',
                    '010H', '011H', '012H', '013H', '014H', '015H', '016H', '017H', '018H', '019H',
                    '020H', '021H', '022H', '023H', '024H', '025H', '026H', '027H', '028H', '029H',
                    '030H', '031H', '032H', '033H', '034H', '035H', '036H', '037H', '038H', '039H',
                    '040H', '041H', '042H', '043H', '044H', '045H', '046H', '047H', '048H'
                ]
            },
            {
                "name": "HP3",
                "time": [
                    '001H', '002H', '003H', '004H', '005H', '006H', '007H', '008H', '009H', '010H',
                    '011H', '012H', '013H', '014H', '015H', '016H', '017H', '018H', '019H', '020H',
                    '021H', '022H', '023H', '024H', '025H', '026H', '027H', '028H', '029H', '030H',
                    '031H', '032H', '033H', '034H', '035H', '036H', '037H', '038H', '039H', '040H',
                    '041H', '042H', '043H', '044H', '045H', '046H', '047H', '048H'
                ]
            }
        ]
    },
    {
        "type_package": "arome-om",
        "detail_package": "POLYN",
        "dataset_id_dev": "65b68c870e237844c20fd503",
        "dataset_id_prod": "65bd1509cc112e6a1458ab95",
        "apikey": APIKEY_AROME_OM,
        "base_url": "https://public-api.meteofrance.fr/previnum/DPPaquetAROME-OM/models/AROME-OM-POLYN/grids",
        "check_availability_url": "https://public-api.meteofrance.fr/previnum/DPPaquetAROME-OM/models/AROME-OM-POLYN/grids/0.025/packages/IP1",
        "product": "productOMPF",
        "grid": "0.025",
        "extension": "grib2",
        "packages": [
            {
                "name": "IP1",
                "time": [
                    '000H', '001H', '002H', '003H', '004H', '005H', '006H', '007H', '008H', '009H',
                    '010H', '011H', '012H', '013H', '014H', '015H', '016H', '017H', '018H', '019H',
                    '020H', '021H', '022H', '023H', '024H', '025H', '026H', '027H', '028H', '029H',
                    '030H', '031H', '032H', '033H', '034H', '035H', '036H', '037H', '038H', '039H',
                    '040H', '041H', '042H', '043H', '044H', '045H', '046H', '047H', '048H'
                ]
            },
            {
                "name": "IP2",
                "time": [
                    '000H', '001H', '002H', '003H', '004H', '005H', '006H', '007H', '008H', '009H',
                    '010H', '011H', '012H', '013H', '014H', '015H', '016H', '017H', '018H', '019H',
                    '020H', '021H', '022H', '023H', '024H', '025H', '026H', '027H', '028H', '029H',
                    '030H', '031H', '032H', '033H', '034H', '035H', '036H', '037H', '038H', '039H',
                    '040H', '041H', '042H', '043H', '044H', '045H', '046H', '047H', '048H'
                ]
            },
            {
                "name": "IP3",
                "time": [
                    '000H', '001H', '002H', '003H', '004H', '005H', '006H', '007H', '008H', '009H',
                    '010H', '011H', '012H', '013H', '014H', '015H', '016H', '017H', '018H', '019H',
                    '020H', '021H', '022H', '023H', '024H', '025H', '026H', '027H', '028H', '029H',
                    '030H', '031H', '032H', '033H', '034H', '035H', '036H', '037H', '038H', '039H',
                    '040H', '041H', '042H', '043H', '044H', '045H', '046H', '047H', '048H'
                ]
            },
            {
                "name": "IP4",
                "time": [
                    '001H', '002H', '003H', '004H', '005H', '006H', '007H', '008H', '009H', '010H',
                    '011H', '012H', '013H', '014H', '015H', '016H', '017H', '018H', '019H', '020H',
                    '021H', '022H', '023H', '024H', '025H', '026H', '027H', '028H', '029H', '030H',
                    '031H', '032H', '033H', '034H', '035H', '036H', '037H', '038H', '039H', '040H',
                    '041H', '042H', '043H', '044H', '045H', '046H', '047H', '048H'
                ]
            },
            {
                "name": "IP5",
                "time": [
                    '000H', '001H', '002H', '003H', '004H', '005H', '006H', '007H', '008H', '009H',
                    '010H', '011H', '012H', '013H', '014H', '015H', '016H', '017H', '018H', '019H',
                    '020H', '021H', '022H', '023H', '024H', '025H', '026H', '027H', '028H', '029H',
                    '030H', '031H', '032H', '033H', '034H', '035H', '036H', '037H', '038H', '039H',
                    '040H', '041H', '042H', '043H', '044H', '045H', '046H', '047H', '048H'
                ]
            },
            {
                "name": "SP1",
                "time": [
                    '000H', '001H', '002H', '003H', '004H', '005H', '006H', '007H', '008H', '009H',
                    '010H', '011H', '012H', '013H', '014H', '015H', '016H', '017H', '018H', '019H',
                    '020H', '021H', '022H', '023H', '024H', '025H', '026H', '027H', '028H', '029H',
                    '030H', '031H', '032H', '033H', '034H', '035H', '036H', '037H', '038H', '039H',
                    '040H', '041H', '042H', '043H', '044H', '045H', '046H', '047H', '048H'
                ]
            },
            {
                "name": "SP2",
                "time": [
                    '000H', '001H', '002H', '003H', '004H', '005H', '006H', '007H', '008H', '009H',
                    '010H', '011H', '012H', '013H', '014H', '015H', '016H', '017H', '018H', '019H',
                    '020H', '021H', '022H', '023H', '024H', '025H', '026H', '027H', '028H', '029H',
                    '030H', '031H', '032H', '033H', '034H', '035H', '036H', '037H', '038H', '039H',
                    '040H', '041H', '042H', '043H', '044H', '045H', '046H', '047H', '048H'
                ]
            },
            {
                "name": "SP3",
                "time": [
                    '000H', '001H', '002H', '003H', '004H', '005H', '006H', '007H', '008H', '009H',
                    '010H', '011H', '012H', '013H', '014H', '015H', '016H', '017H', '018H', '019H',
                    '020H', '021H', '022H', '023H', '024H', '025H', '026H', '027H', '028H', '029H',
                    '030H', '031H', '032H', '033H', '034H', '035H', '036H', '037H', '038H', '039H',
                    '040H', '041H', '042H', '043H', '044H', '045H', '046H', '047H', '048H'
                ]
            },
            {
                "name": "HP1",
                "time": [
                    '000H', '001H', '002H', '003H', '004H', '005H', '006H', '007H', '008H', '009H',
                    '010H', '011H', '012H', '013H', '014H', '015H', '016H', '017H', '018H', '019H',
                    '020H', '021H', '022H', '023H', '024H', '025H', '026H', '027H', '028H', '029H',
                    '030H', '031H', '032H', '033H', '034H', '035H', '036H', '037H', '038H', '039H',
                    '040H', '041H', '042H', '043H', '044H', '045H', '046H', '047H', '048H'
                ]
            },
            {
                "name": "HP2",
                "time": [
                    '000H', '001H', '002H', '003H', '004H', '005H', '006H', '007H', '008H', '009H',
                    '010H', '011H', '012H', '013H', '014H', '015H', '016H', '017H', '018H', '019H',
                    '020H', '021H', '022H', '023H', '024H', '025H', '026H', '027H', '028H', '029H',
                    '030H', '031H', '032H', '033H', '034H', '035H', '036H', '037H', '038H', '039H',
                    '040H', '041H', '042H', '043H', '044H', '045H', '046H', '047H', '048H'
                ]
            },
            {
                "name": "HP3",
                "time": [
                    '001H', '002H', '003H', '004H', '005H', '006H', '007H', '008H', '009H', '010H',
                    '011H', '012H', '013H', '014H', '015H', '016H', '017H', '018H', '019H', '020H',
                    '021H', '022H', '023H', '024H', '025H', '026H', '027H', '028H', '029H', '030H',
                    '031H', '032H', '033H', '034H', '035H', '036H', '037H', '038H', '039H', '040H',
                    '041H', '042H', '043H', '044H', '045H', '046H', '047H', '048H'
                ]
            }
        ]
    },
    {
        "type_package": "arome-om",
        "detail_package": "NCALED",
        "dataset_id_dev": "65b68c870e237844c20fd504",
        "dataset_id_prod": "65bd14cca6919e97e9699b09",
        "apikey": APIKEY_AROME_OM,
        "base_url": "https://public-api.meteofrance.fr/previnum/DPPaquetAROME-OM/models/AROME-OM-NCALED/grids",
        "check_availability_url": "https://public-api.meteofrance.fr/previnum/DPPaquetAROME-OM/models/AROME-OM-NCALED/grids/0.025/packages/IP1",
        "product": "productOMNC",
        "grid": "0.025",
        "extension": "grib2",
        "packages": [
            {
                "name": "IP1",
                "time": [
                    '000H', '001H', '002H', '003H', '004H', '005H', '006H', '007H', '008H', '009H',
                    '010H', '011H', '012H', '013H', '014H', '015H', '016H', '017H', '018H', '019H',
                    '020H', '021H', '022H', '023H', '024H', '025H', '026H', '027H', '028H', '029H',
                    '030H', '031H', '032H', '033H', '034H', '035H', '036H', '037H', '038H', '039H',
                    '040H', '041H', '042H', '043H', '044H', '045H', '046H', '047H', '048H'
                ]
            },
            {
                "name": "IP2",
                "time": [
                    '000H', '001H', '002H', '003H', '004H', '005H', '006H', '007H', '008H', '009H',
                    '010H', '011H', '012H', '013H', '014H', '015H', '016H', '017H', '018H', '019H',
                    '020H', '021H', '022H', '023H', '024H', '025H', '026H', '027H', '028H', '029H',
                    '030H', '031H', '032H', '033H', '034H', '035H', '036H', '037H', '038H', '039H',
                    '040H', '041H', '042H', '043H', '044H', '045H', '046H', '047H', '048H'
                ]
            },
            {
                "name": "IP3",
                "time": [
                    '000H', '001H', '002H', '003H', '004H', '005H', '006H', '007H', '008H', '009H',
                    '010H', '011H', '012H', '013H', '014H', '015H', '016H', '017H', '018H', '019H',
                    '020H', '021H', '022H', '023H', '024H', '025H', '026H', '027H', '028H', '029H',
                    '030H', '031H', '032H', '033H', '034H', '035H', '036H', '037H', '038H', '039H',
                    '040H', '041H', '042H', '043H', '044H', '045H', '046H', '047H', '048H'
                ]
            },
            {
                "name": "IP4",
                "time": [
                    '001H', '002H', '003H', '004H', '005H', '006H', '007H', '008H', '009H', '010H',
                    '011H', '012H', '013H', '014H', '015H', '016H', '017H', '018H', '019H', '020H',
                    '021H', '022H', '023H', '024H', '025H', '026H', '027H', '028H', '029H', '030H',
                    '031H', '032H', '033H', '034H', '035H', '036H', '037H', '038H', '039H', '040H',
                    '041H', '042H', '043H', '044H', '045H', '046H', '047H', '048H'
                ]
            },
            {
                "name": "IP5",
                "time": [
                    '000H', '001H', '002H', '003H', '004H', '005H', '006H', '007H', '008H', '009H',
                    '010H', '011H', '012H', '013H', '014H', '015H', '016H', '017H', '018H', '019H',
                    '020H', '021H', '022H', '023H', '024H', '025H', '026H', '027H', '028H', '029H',
                    '030H', '031H', '032H', '033H', '034H', '035H', '036H', '037H', '038H', '039H',
                    '040H', '041H', '042H', '043H', '044H', '045H', '046H', '047H', '048H'
                ]
            },
            {
                "name": "SP1",
                "time": [
                    '000H', '001H', '002H', '003H', '004H', '005H', '006H', '007H', '008H', '009H',
                    '010H', '011H', '012H', '013H', '014H', '015H', '016H', '017H', '018H', '019H',
                    '020H', '021H', '022H', '023H', '024H', '025H', '026H', '027H', '028H', '029H',
                    '030H', '031H', '032H', '033H', '034H', '035H', '036H', '037H', '038H', '039H',
                    '040H', '041H', '042H', '043H', '044H', '045H', '046H', '047H', '048H'
                ]
            },
            {
                "name": "SP2",
                "time": [
                    '000H', '001H', '002H', '003H', '004H', '005H', '006H', '007H', '008H', '009H',
                    '010H', '011H', '012H', '013H', '014H', '015H', '016H', '017H', '018H', '019H',
                    '020H', '021H', '022H', '023H', '024H', '025H', '026H', '027H', '028H', '029H',
                    '030H', '031H', '032H', '033H', '034H', '035H', '036H', '037H', '038H', '039H',
                    '040H', '041H', '042H', '043H', '044H', '045H', '046H', '047H', '048H'
                ]
            },
            {
                "name": "SP3",
                "time": [
                    '000H', '001H', '002H', '003H', '004H', '005H', '006H', '007H', '008H', '009H',
                    '010H', '011H', '012H', '013H', '014H', '015H', '016H', '017H', '018H', '019H',
                    '020H', '021H', '022H', '023H', '024H', '025H', '026H', '027H', '028H', '029H',
                    '030H', '031H', '032H', '033H', '034H', '035H', '036H', '037H', '038H', '039H',
                    '040H', '041H', '042H', '043H', '044H', '045H', '046H', '047H', '048H'
                ]
            },
            {
                "name": "HP1",
                "time": [
                    '000H', '001H', '002H', '003H', '004H', '005H', '006H', '007H', '008H', '009H',
                    '010H', '011H', '012H', '013H', '014H', '015H', '016H', '017H', '018H', '019H',
                    '020H', '021H', '022H', '023H', '024H', '025H', '026H', '027H', '028H', '029H',
                    '030H', '031H', '032H', '033H', '034H', '035H', '036H', '037H', '038H', '039H',
                    '040H', '041H', '042H', '043H', '044H', '045H', '046H', '047H', '048H'
                ]
            },
            {
                "name": "HP2",
                "time": [
                    '000H', '001H', '002H', '003H', '004H', '005H', '006H', '007H', '008H', '009H',
                    '010H', '011H', '012H', '013H', '014H', '015H', '016H', '017H', '018H', '019H',
                    '020H', '021H', '022H', '023H', '024H', '025H', '026H', '027H', '028H', '029H',
                    '030H', '031H', '032H', '033H', '034H', '035H', '036H', '037H', '038H', '039H',
                    '040H', '041H', '042H', '043H', '044H', '045H', '046H', '047H', '048H'
                ]
            },
            {
                "name": "HP3",
                "time": [
                    '001H', '002H', '003H', '004H', '005H', '006H', '007H', '008H', '009H', '010H',
                    '011H', '012H', '013H', '014H', '015H', '016H', '017H', '018H', '019H', '020H',
                    '021H', '022H', '023H', '024H', '025H', '026H', '027H', '028H', '029H', '030H',
                    '031H', '032H', '033H', '034H', '035H', '036H', '037H', '038H', '039H', '040H',
                    '041H', '042H', '043H', '044H', '045H', '046H', '047H', '048H'
                ]
            }
        ]
    },
    {
        "type_package": "arome",
        "detail_package": None,
        "dataset_id_dev": "65aade5a97e39e6c4cae5252",
        "dataset_id_prod": "65bd1247a6238f16e864fa80",
        "apikey": APIKEY_AROME,
        "base_url": "https://public-api.meteofrance.fr/previnum/DPPaquetAROME/models/AROME/grids",
        "check_availability_url": "https://public-api.meteofrance.fr/previnum/DPPaquetAROME/models/AROME/grids/0.01/packages/SP1",
        "product": "productARO",
        "grid": "0.01",
        "extension": "grib2",
        "packages": [
            {
                "name": "SP1",
                "time": [
                    '00H', '01H', '02H', '03H', '04H', '05H', '06H', '07H', '08H', '09H',
                    '10H', '11H', '12H', '13H', '14H', '15H', '16H', '17H', '18H', '19H',
                    '20H', '21H', '22H', '23H', '24H', '25H', '26H', '27H', '28H', '29H',
                    '30H', '31H', '32H', '33H', '34H', '35H', '36H', '37H', '38H', '39H',
                    '40H', '41H', '42H', '43H', '44H', '45H', '46H', '47H', '48H', '49H',
                    '50H', '51H'
                ]
            },
            {
                "name": "SP2",
                "time": [
                    '00H', '01H', '02H', '03H', '04H', '05H', '06H', '07H', '08H', '09H',
                    '10H', '11H', '12H', '13H', '14H', '15H', '16H', '17H', '18H', '19H',
                    '20H', '21H', '22H', '23H', '24H', '25H', '26H', '27H', '28H', '29H',
                    '30H', '31H', '32H', '33H', '34H', '35H', '36H', '37H', '38H', '39H',
                    '40H', '41H', '42H', '43H', '44H', '45H', '46H', '47H', '48H', '49H',
                    '50H', '51H'
                ]
            },
            {
                "name": "SP3",
                "time": [
                    '00H', '01H', '02H', '03H', '04H', '05H', '06H', '07H', '08H', '09H',
                    '10H', '11H', '12H', '13H', '14H', '15H', '16H', '17H', '18H', '19H',
                    '20H', '21H', '22H', '23H', '24H', '25H', '26H', '27H', '28H', '29H',
                    '30H', '31H', '32H', '33H', '34H', '35H', '36H', '37H', '38H', '39H',
                    '40H', '41H', '42H', '43H', '44H', '45H', '46H', '47H', '48H', '49H',
                    '50H', '51H'
                ]
            },
            {
                "name": "HP1",
                "time": [
                    '00H', '01H', '02H', '03H', '04H', '05H', '06H', '07H', '08H', '09H',
                    '10H', '11H', '12H', '13H', '14H', '15H', '16H', '17H', '18H', '19H',
                    '20H', '21H', '22H', '23H', '24H', '25H', '26H', '27H', '28H', '29H',
                    '30H', '31H', '32H', '33H', '34H', '35H', '36H', '37H', '38H', '39H',
                    '40H', '41H', '42H', '43H', '44H', '45H', '46H', '47H', '48H', '49H',
                    '50H', '51H'
                ]
            }
        ]
    },
    {
        "type_package": "arome",
        "detail_package": None,
        "dataset_id_dev": "65aadec3dc9e969fd00e71e8",
        "dataset_id_prod": "65bd12d7bfd26e26804204cb",
        "apikey": APIKEY_AROME,
        "base_url": "https://public-api.meteofrance.fr/previnum/DPPaquetAROME/models/AROME/grids",
        "check_availability_url": "https://public-api.meteofrance.fr/previnum/DPPaquetAROME/models/AROME/grids/0.025/packages/SP1",
        "product": "productARO",
        "grid": "0.025",
        "extension": "grib2",
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
        "detail_package": None,
        "dataset_id_dev": "65aaded8dc9e969fd00e71e9",
        "dataset_id_prod": "65bd13b2eb9e79ab309f6e63",
        "apikey": APIKEY_ARPEGE,
        "base_url": "https://public-api.meteofrance.fr/previnum/DPPaquetARPEGE/models/ARPEGE/grids",
        "check_availability_url": "https://public-api.meteofrance.fr/previnum/DPPaquetARPEGE/models/ARPEGE/grids/0.1/packages/IP1",
        "product": "productARP",
        "grid": "0.1",
        "extension": "grib2",
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
        "detail_package": None,
        "dataset_id_dev": "65aadeebdc9e969fd00e71ea",
        "dataset_id_prod": "65bd13e557b26b467363b521",
        "apikey": APIKEY_ARPEGE,
        "base_url": "https://public-api.meteofrance.fr/previnum/DPPaquetARPEGE/models/ARPEGE/grids",
        "check_availability_url": "https://public-api.meteofrance.fr/previnum/DPPaquetARPEGE/models/ARPEGE/grids/0.25/packages/IP1",
        "product": "productARP",
        "grid": "0.25",
        "extension": "grib2",
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
