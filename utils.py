"""
    Funciones con los procesos necesarios para trabajar sobre una bbdd de tweeets y extraer
    las palabras más frecuentes capaces de representar sentimientos negativos o positivos
    de quienes los redactaron.
"""

import zipfile
import csv
import re
from typing import List
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from collections import Counter


def descomprime_zip(zip_file: str, target_folder: str) -> None:
    """
    Descomprime un archivo ZIP en la carpeta de destino.

    Parámetros:
    - zip_file (str): Ruta del archivo ZIP a descomprimir.
    - target_folder (str): Carpeta de destino para extraer los archivos.
    """
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(target_folder)


def carga_dataset(csv_file: str) -> list:
    """
    Carga el dataset desde una cadena CSV y lo devuelve como una lista de diccionarios.

    Parámetros:
    - csv_data (str): Cadena CSV a cargar.

    Devuelve:
    - list: Lista de diccionarios representando el dataset.
    """
    dataset = []
    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            dataset.append({
                'sentiment': row['sentiment'],
                'id': row['id'],
                'date': row['date'],
                'query': row['query'],
                'user': row['user'],
                'text': row['text']
            })
    return dataset


def preprocesar_texto(texto: str) -> str:
    """
    Realiza un preprocesamiento básico en un texto dado:
    - Elimina las URLs
    - Elimina los caracteres no ASCII y los símbolos
    - Convierte el texto a minúsculas
    - Elimina espacios en blanco adicionales

    Parámetros:
    - texto (str): Texto a preprocesar.

    Devuelve:
    - str: Texto preprocesado.
    """
    # Eliminar las URLs
    texto_sin_url = re.sub(r"http\S+|www\S+|https\S+", "", texto)

    # Eliminar los caracteres no ASCII y los símbolos
    texto_sin_especiales = re.sub(r"[^\w\s]", "", texto_sin_url)

    # Convertir el texto a minúsculas
    texto_preprocesado = texto_sin_especiales.lower()

    # Eliminar espacios en blanco adicionales
    texto_preprocesado = " ".join(texto_preprocesado.split())

    return texto_preprocesado


def eliminar_stopwords(texto: str) -> str:
    """
    Elimina las stopwords de un texto dado.

    Parámetros:
    - texto (str): Texto al que se le eliminarán las stopwords.

    Devuelve:
    - str: Texto sin las stopwords.
    """
    stopwords = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 'yourself',
                 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself',
                 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this',
                 'that', 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have',
                 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if',
                 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against',
                 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from',
                 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once',
                 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more',
                 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too',
                 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now']

    palabras = texto.split()
    palabras_filtradas = [palabra for palabra in palabras if palabra not in stopwords]
    texto_sin_stopwords = " ".join(palabras_filtradas)

    return texto_sin_stopwords


def obtener_frecuencias_y_vocabulario(dataset: list) -> tuple:
    """
    Calcula las frecuencias de términos y el vocabulario a partir de un dataset.

    Parámetros:
    - dataset (list): Lista de diccionarios representando el dataset.

    Devuelve:
    - tuple: Tupla que contiene la lista de frecuencias de términos y el vocabulario.
    """
    frecuencias = []
    vocabulario = set()

    for tweet in dataset:
        frecuencia_tweet = {}
        palabras = tweet['text'].split()

        for palabra in palabras:
            if palabra not in frecuencia_tweet:
                frecuencia_tweet[palabra] = 1
            else:
                frecuencia_tweet[palabra] += 1

        frecuencias.append(frecuencia_tweet)
        vocabulario.update(palabras)

    vocabulario = sorted(list(vocabulario))

    return frecuencias, vocabulario


def agregar_frecuencias(dataset: List[dict]) -> None:
    """
    Agrega una nueva variable 'frecuencias' a cada registro del dataset,
    con su diccionario de frecuencias de términos asociado.

    Parámetros:
    - dataset (List[dict]): Dataset representado como una lista de diccionarios.
    """
    frecuencias, _ = obtener_frecuencias_y_vocabulario(dataset)
    for data, frecuencia in zip(dataset, frecuencias):
        data['frecuencias'] = frecuencia
    return dataset


def guardar_dataset_csv(dataset, csv_file):
    """
    Guarda el dataset en formato CSV.

    Parámetros:
    - dataset (list): Dataset representado como una lista de diccionarios.
    - csv_file (str): Ruta del archivo CSV donde se guardará el dataset.
    """
    with open(csv_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=dataset[0].keys())
        writer.writeheader()
        writer.writerows(dataset)


def obtener_numero_clusters(csv_file):
    """
    Obtiene el número de clusters en la columna 'sentiment' del dataset.

    Parámetros:
    - csv_file (str): Ruta del archivo CSV que contiene el dataset.

    Devuelve:
    - int: Número de clusters encontrados.
    """
    # Cargar el dataset desde el archivo CSV
    dataset = pd.read_csv(csv_file)

    # Obtener los valores únicos en la columna 'sentiment'
    clusters = dataset['sentiment'].unique()

    # Obtener el número de clusters
    num_clusters = len(clusters)

    return num_clusters


def verificar_elementos_vacios(dataset):
    """
    Verifica si hay elementos vacíos en la columna 'text' de un dataset y calcula el porcentaje de elementos vacíos.

    Parámetros:
    - dataset (list): Dataset representado como una lista de diccionarios.

    Devuelve:
    - float: Porcentaje de elementos vacíos en la columna 'text'.
    """
    total_elementos = len(dataset)
    if total_elementos == 0:
        return 100.0

    elementos_vacios = sum(1 for registro in dataset if registro.get('text', '').strip() == '')
    porcentaje_vacios = (elementos_vacios / total_elementos) * 100

    return porcentaje_vacios


def eliminar_elementos_nulos(dataset):
    """
    Elimina los elementos nulos de un dataset.

    Parámetros:
    - dataset (list): Dataset representado como una lista de diccionarios.

    Devuelve:
    - list: Nuevo dataset sin elementos nulos.
    """
    dataset_sin_nulos = [registro for registro in dataset if registro.get('text', '').strip() != '']
    return dataset_sin_nulos


def generar_wordcloud_por_cluster(dataset_sin_nulos: object) -> object:
    """
    Genera un word cloud para cada cluster en el dataset.

    Parámetros:
    - dataset (list): Dataset representado como una lista de diccionarios.
    """
    clusters = set(d['sentiment'] for d in dataset_sin_nulos)
    for cluster in clusters:
        text_cluster = ' '.join(d['text'] for d in dataset_sin_nulos if d['sentiment'] == cluster)
        wordcloud = WordCloud(width=800, height=400).generate(text_cluster)

        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.title(f"Word Cloud - Cluster {cluster}")
        plt.axis("off")
        plt.show()


def generar_histograma_por_cluster(dataset_sin_nulos):
    """
    Genera un histograma por cluster con las frecuencias de las 20 palabras más frecuentes.

    Parámetros:
    - dataset_sin_nulos (list): Dataset representado como una lista de diccionarios sin elementos nulos.
    """
    frecuencias, vocabulario = obtener_frecuencias_y_vocabulario(dataset_sin_nulos)
    clusters = set(d['sentiment'] for d in dataset_sin_nulos)

    num_clusters = len(clusters)
    num_columns = 2  # valor variable según número de columnas deseadas
    num_rows = (num_clusters + num_columns - 1) // num_columns

    fig, axes = plt.subplots(num_rows, num_columns, figsize=(12, 8), squeeze=False)

    for i, cluster in enumerate(clusters):
        row = i // num_columns
        col = i % num_columns

        ax = axes[row, col]

        frecuencias_cluster = Counter([palabra for j, frecuencia in enumerate(frecuencias)
                                       for palabra, count in frecuencia.items()
                                       if dataset_sin_nulos[j]['sentiment'] == cluster])
        frecuencias_top20 = frecuencias_cluster.most_common(20)

        palabras = [palabra for palabra, _ in frecuencias_top20]
        counts = [count for _, count in frecuencias_top20]

        ax.bar(palabras, counts, alpha=0.7)
        ax.set_xlabel('Palabras')
        ax.set_ylabel('Frecuencia')
        ax.set_title(f'Histograma de las 20 Palabras Más Frecuentes - Cluster {cluster}')
        ax.tick_params(axis='x', rotation=90)

    # Eliminar subplots no utilizados
    if num_clusters < num_rows * num_columns:
        for i in range(num_clusters, num_rows * num_columns):
            fig.delaxes(axes[i // num_columns, i % num_columns])

    # Ajustar los subplots y mostrar la figura
    plt.tight_layout()
    plt.show()
