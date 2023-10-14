import json
from Data_Understanding.Data_Analysis.data_analysis_logic import (versions_number,updated_versions_number)

async def initilal_profiling(connection,connection2):
   
 
    nb_versions=await versions_number(connection)
    updated_ver= await updated_versions_number(connection2)
   
    result={    
            "versions_number":nb_versions,
            "updated_version":updated_ver,
            }
         
    
    return  json.dumps(result)
        

