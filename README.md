# planilha-imdb-consulta

Uma planilha do excel, com macro, que possibilita importar informações do imdb a partir dos ids do filme.

Os ids do imdb podem ser obtidos através do script `obter_id_imdb.py`, que utiliza o selenium para realizar a captura.

## Requisitos
- Python >= 3.10<br>
[https://www.python.org/downloads/](https://www.python.org/downloads/)

- Instalar pacotes python:
    ```sh
    pip install selenium bs4 pypiwin32
    ```

## Utilização da planilha
- Execute o script `imdb_movie_vba.py` e autorize a execução do mesmo com permissão elevada (É necessário para registrar o objeto Python.ObjectLibrary, que será utilizado pela planilha).
- Abra a planilha, insira os ids desejados e clique em "Obter Informações".

**Obs**: Somente nas linhas no qual o campo `Título (PT)` estiver vazio e houver um id preenchido é que será obtido as informações

## Utilização do script para obter os ids
Para obter os ids a partir do site do imdb é necessário criar um arquivo .csv com os nomes dos filmes do qual se deseja obter a informação. A localização padrão do arquivo com os filmes é `files/filmes.csv`. Após a execução do script será gerado um novo arquivo, com o nome de `files/id_filmes.csv`.

**Obs**: Como exemplo de uso, foi deixado salvo os arquivos "filmes.csv", "id_filmes.csv" e a planilha preenchida a partir dos ids gerado pelo script.