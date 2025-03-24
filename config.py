# if not available use : prisma generate
from prisma import Prisma 

# URL configuration ================================================
# other URL's required in routers later on
ROS2_SERVER_PUBLISHER_URL = "http://127.0.0.1:8003"
ROS2_SERVER_SUBSCRIBER_URL = "http://127.0.0.1:8003"

# for some reasons (i don't know why) each python library that connects to a database
# uses a different URL pattern to connect to a certain database. Here below i provide the ones for a MySQL server
# if using SQLalchemy:
# https://docs.sqlalchemy.org/en/20/dialects/mysql.html
# if using Prisma:
# https://www.prisma.io/docs/orm/overview/databases/mysql
MYSQL_DB_SERVER_URL = "mysql://aiUser:pwdAIteamDB@bsu-db-server:3306/bsu_warehouse_db"
# add the "origins" (the url of the server)
ORIGINS = [
    "http://localhost:8000", # this process
    "http://127.0.0.1:8000", # this process
    "http://bsu-server:8000",# this process
    "http://127.0.0.1:8002", # bsu-website
    "http://127.0.0.1:80",   # bsu-website
    "http://bsu-website:80", # doesn't seem to work
    "http://bsu-website",    # doesn't seem to work
    "http://bsu-ros-server",    # 
    "http://bsu-ros-server:8003",    # 
]
# URL configuration ================================================


# create DB connection ================================================
DB_CLIENT = Prisma()
# create DB connection ================================================