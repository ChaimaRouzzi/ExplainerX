import asyncpg
import json
from datetime import datetime
import pandas as pd
import numpy as np
import subprocess
import ast
from Data_Understanding.df import fd
from Data_Understanding.data_analysis_logic import (fetch_rows,fetch_columns,versions_number,fetch_data_updated_version,fetch_data_version,updated_versions_number)

async def initilal_profiling(connection,connection2):
   
 
    nb_versions=await versions_number(connection)
    updated_ver= await updated_versions_number(connection2)
   
    result={    
            "versions_number":nb_versions,
            "updated_version":updated_ver,
            }
         
    
    return  json.dumps(result)
        

