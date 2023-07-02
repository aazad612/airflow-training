from datetime import datetime

import os
import sys

CUR_DIR = os.path.abspath(os.path.dirname(__file__))

default_args = {
    'owner': 'Johney Aazad',
    'depends_on_past': False,
    'email_on_retry': False,
    'retries': 0,
    'start_date': datetime(2023,6,6)
    'catchup': False
}