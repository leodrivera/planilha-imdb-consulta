# Install
# pip install bs4 pypiwin32

import json
import re

import pythoncom
import requests
from bs4 import BeautifulSoup


class imdb_movie:
    _DICT_HEADER = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
        "accept-language": "pt-BR",
    }

    def __init__(self, id, DICT_HEADER=_DICT_HEADER):
        self._id = id
        URL = f"https://www.imdb.com/title/tt{id}"
        response = requests.get(URL, headers=DICT_HEADER).content
        self._soup = BeautifulSoup(response, "html.parser")
        meta_dict = self._soup.find_all("script", type="application/ld+json")
        self._meta = json.loads(meta_dict[0].get_text())

    def _result_parser(self, result):
        result = result.replace("&quot;", '"')
        result = result.replace("&apos;", "'")
        result = result.replace("&amp;", "&")
        return result

    @property
    def id(self):
        return self._id

    @property
    def year(self):
        year = self._soup.find("title").get_text()
        year = re.findall(r"^.*?\([^\d]*(\d+)[^\d]*\).*$", year)
        return year[0]

    @property
    def title(self):
        result = self._result_parser(self._meta["name"])
        return result

    @property
    def title_pt(self):
        try:
            result = self._meta["alternateName"]
        except KeyError:
            result = self._meta["name"]
        return self._result_parser(result)

    @property
    def duration(self):
        try:
            duration = self._meta["duration"]
            duration = duration.replace("PT", "")
        except KeyError:
            duration = ""
        return duration

    @property
    def rating(self):
        return self._meta["aggregateRating"]["ratingValue"]

    @property
    def description(self):
        result = self._meta["description"]
        return self._result_parser(result)

    @property
    def genre(self):
        genres = self._meta["genre"]
        result = ""
        for genre in genres:
            result += f"{genre}, "
        return result[:-2]


class PythonObjectLibrary:
    # This will create a GUID to register it with Windows, it is unique.
    _reg_clsid_ = pythoncom.CreateGuid()

    # Register the object as an EXE file, the alternative is an DLL file (INPROC_SERVER)
    _reg_clsctx_ = pythoncom.CLSCTX_LOCAL_SERVER

    # the program ID, this is the name of the object library that users will use to create the object.
    _reg_progid_ = "Python.ObjectLibrary"

    # this is a description of our object library.
    _reg_desc_ = "This is our Python object library."

    # a list of strings that indicate the public methods for the object. If they aren't listed they are conisdered private.
    _public_methods_ = ["get_movie_info"]

    def get_movie_info(self, id: str) -> str:
        movie = imdb_movie(id)
        infos = [
            "title_pt",
            "title",
            "year",
            "description",
            "duration",
            "genre",
            "rating",
        ]
        result = ""
        for info in infos:
            result += f"{eval(f'movie.{info}')}//"
        return result[:-2]


if __name__ == "__main__":
    import win32com.server.register

    win32com.server.register.UseCommandLine(PythonObjectLibrary)
