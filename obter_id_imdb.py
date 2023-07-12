import csv
import time
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.by import By

#################################################################
# Código para fazer a consulta dos filmes, encontrados dentro   #
# do arquivo .csv, e obter o id, no sistema do imdb, utilizando #
# o selenium e o google para realizar a busca                   #
#################################################################

# Varíaveis para acesso
base_path = Path(__file__).resolve(strict=True).parent
path = base_path.joinpath("files")
obj_orig = path.joinpath("filmes.csv")  # Arquivo com a lista de filmes original
obj_dest = path.joinpath("id_filmes.csv")  # Arquivo com a lista de filmes com id


class movie:
    def __init__(self, nome: str) -> None:
        self.nome = nome

    def url_busca(self) -> str:
        nome = self.nome.split(" ")
        valor = '+'.join(nome)
        return f"https://www.google.com.br/search?as_sitesearch=imdb.com&q={valor}"

    def obter_id(self) -> str | None:
        try:
            element = driver.find_element(
                By.XPATH, "//a[contains(@href, 'https://www.imdb.com/title/')]"
            )
            link = element.get_attribute("href")
            link = link.split("/")
            id_final = link[4][2:]
            return id_final
        except:
            return None


if __name__ == "__main__":
    path.mkdir(exist_ok=True)

    # Abro o Chrome
    driver = webdriver.Chrome()

    # Crio os objetos para fazer as escritas e leituras dos .csv
    read_obj = open(obj_orig, "r")
    write_obj = open(obj_dest, "w", newline="")
    csv_reader = csv.reader(read_obj)
    csv_writer = csv.writer(write_obj)

    # Contador de falhas no acesso
    cont = 0
    for lin in csv_reader:
        print(f"Obtendo informações do filme '{lin[0]}'")
        filme = movie(lin[0])  # Pego nome do filme

        driver.get(filme.url_busca())  # Obtenho a url
        time.sleep(2)

        res = filme.obter_id()
        if not res:
            cont += 1
        else:
            cont = 0
            print(f"Obtido o id {res}")
        if cont == 3:
            print("Finalizando a busca devido à 3 falhas consecutivas")
            break  # Saio do loop caso tenha 3 falhas consecutivas
        csv_writer.writerow([res])  # Escrevo a linha no .csv

    # Fecho as conexões
    driver.close()
    read_obj.close()
    write_obj.close()
