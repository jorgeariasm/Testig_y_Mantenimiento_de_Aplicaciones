"""
    Código que ejecuta todas las funciones contenidas en utils.py.
"""


import re
import utils

if __name__ == "__main__":
    # Proceso de descompresión de un archivo zip
    zip_file = 'data/twitter_reduced.zip'
    target_folder = 'data'
    utils.descomprime_zip(zip_file, target_folder)

    # Proceso de carga de un archivo csv.
    csv_file = 'data/twitter_reduced.csv'
    dataset = utils.carga_dataset(csv_file)

    # Mostrar los primeros 5 registros del dataset
    print("\nPrimeros 5 registros del dataset:")
    for i in range(min(5, len(dataset))):
        print(dataset[i])

    # Preprocesamiento de los textos en el dataset.
    for data in dataset:
        data['text'] = utils.preprocesar_texto(data['text'])
        data['text'] = utils.eliminar_stopwords(data['text'])

    # Imprimir los primeros 5 registros después del preprocesamiento
    print("\nPrimeros 5 registros después del preprocesamiento:")
    for i in range(min(5, len(dataset))):
        print(dataset[i])

    # Imprimir las 5 últimas filas del dataset después del preprocesamiento
    print("\nÚltimas 5 filas después del preprocesamiento:")
    for data in dataset[-5:]:
        print(data)

    # Obtener las frecuencias y el vocabulario
    frecuencias, vocabulario = utils.obtener_frecuencias_y_vocabulario(dataset)

    # Mostrar los primeros 5 elementos de la lista de diccionarios con la nueva estructura
    print("\nPrimeros 5 elementos de la lista de diccionarios:")
    for i in range(min(5, len(frecuencias))):
        frecuencia_actualizada = {palabra: frecuencias[i].get(palabra, 0) for palabra in frecuencias[i].keys()}
        print(frecuencia_actualizada)

    # Ordenar alfabéticamente el vocabulario
    vocabulario.sort()

    # Filtrar las palabras utilizando expresiones regulares, para evitar que aparezcan solo números
    patron = r'^[a-zA-Z]+$'
    vocabulario_filtrado = [palabra for palabra in vocabulario if re.match(patron, palabra)]

    # Mostrar las primeras 10 palabras ordenadas alfabéticamente
    print("\nPrimeras 10 palabras ordenadas alfabéticamente:")
    print(vocabulario_filtrado[:10])

    # Agregar las frecuencias de términos a cada registro del dataset
    utils.agregar_frecuencias(dataset)

    # Imprimir el elemento 20 del dataset
    print("\nElemento 20 del dataset:")
    print(dataset[19])

    # Código para guardar el dataset en formato CSV
    csv_file = 'data/twitter_processed.csv'
    utils.guardar_dataset_csv(dataset, csv_file)

    # Código para leer el dataset procesado y obtener el número de clusters
    csv_file = 'data/twitter_processed.csv'
    num_clusters = utils.obtener_numero_clusters(csv_file)
    print("\nNúmero de clusters:", num_clusters)

    # Eliminar elementos vacíos
    dataset_sin_nulos = utils.eliminar_elementos_nulos(dataset)

    # Verificar los elementos vacíos
    porcentaje_nulos = utils.verificar_elementos_vacios(dataset)
    print(f"\nPorcentaje de elementos nulos en el dataset original: {porcentaje_nulos}%")
    porcentaje_vacios_sin_nulos = utils.verificar_elementos_vacios(dataset_sin_nulos)
    print(f"\nPorcentaje de elementos nulos en el dataset sin elementos nulos: {porcentaje_vacios_sin_nulos}%")

    # Generar el word cloud por cluster
    utils.generar_wordcloud_por_cluster(dataset_sin_nulos)

    # Código para generar el histograma de frecuencias por cluster
    utils.generar_histograma_por_cluster(dataset_sin_nulos)

    # Respuestas al Ejercicio 7
    print("\nPREGUNTAS - Ejercicio 7")
    print("\na) ¿Cuáles son las palabras más utilizadas en las críticas positivas?")
    print("\nRespuesta: "
          "\nLas palabras más utilizadas en los sentimientos positivos son: 'Im', 'Good', 'Love', 'Day', 'Thanks'")

    print("\nb) ¿Cuáles son las palabras más utilizadas en las críticas negativas?")
    print("\nRespuesta: "
          "\nLas palabras más utilizadas en los sentimientos negativos son: 'Im', 'Work', 'Go', 'Get', 'Cant'")

    print("\nc) ¿Hay palabras que aparezcan tanto en los sentimientos positivos como negativos?")
    print("\nRespuesta: "
          "\nSí, hay palabras que aparecen en ambos sentimientos, como: 'Im', 'Like', 'Day', 'Today', 'Time'")

    print("\nd) A partir de la WordCloud, ¿Qué se puede deducir sobre el sentimiento general de cada grupo?")
    print("\nRespuesta: "
          "\nEn el cluster 0 (asociado a sentimientos negativos) se observa insatisfacción por falta de tiempo, "
          "trabajo y obligaciones.")
    print("\nRespuesta: "
          "\nEn el cluster 1 (asociado a sentimientos positivos) se observa gratitud, amor y felicidad explícita.")
