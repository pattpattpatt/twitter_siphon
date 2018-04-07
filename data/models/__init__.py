from ..db_interface.read import ReadFromDatabase as ReadDb
from ..db_interface.write import WriteToDatabase as WriteDb
import os

__all__ = ["ReadDb", "WriteDb"]


__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

__congress__ = os.path.join(__location__, "congress.pickle")
