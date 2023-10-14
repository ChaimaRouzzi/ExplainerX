import asyncpg

async def connect_to_db():
    # Replace the values below with your PostgreSQL connection details
    connection_pool = await asyncpg.create_pool(
        host="localhost",
        port=5432,
        user="postgres",
        password="chaima",
        database="datawerhouse",
        min_size = 5  ,  
        max_size = 20,    
        max_inactive_connection_lifetime = 3, 
        timeout =20 ,   
        command_timeout = 30  
    )
    return connection_pool

async def connect_to_db2():
    # Replace the values below with your PostgreSQL connection details
    connection_pool2 = await asyncpg.create_pool(
        host="localhost",
        port=5432,
        user="postgres",
        password="chaima",
        database="datawerhouse_version2",
        min_size = 5 ,     
        max_size = 20,     
        max_inactive_connection_lifetime = 3,  # 30 minutes
        timeout = 20,      # 10 seconds
        command_timeout = 30,  # 30 seconds
    )
    return connection_pool2
