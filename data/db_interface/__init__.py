from data.db_interface.database import Database
from data.db_interface.read import ReadFromDatabase
from data.db_interface.write import WriteToDatabase

import os

__all__ = [
    "Database",
    "ReadFromDatabase",
    "WriteToDatabase"]

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

__credential_file__ = os.path.join(__location__, "mongo_connect")
