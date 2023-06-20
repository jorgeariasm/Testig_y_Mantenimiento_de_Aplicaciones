"""
    Conjuntos de test unitarios para validar la correcta ejecución de las funciones
"""

import os
import shutil
import zipfile
import tempfile
import pandas as pd
import unittest
from unittest import mock
from unittest.mock import patch, Mock
import utils


class TestUtils(unittest.TestCase):
    """Clase que contiene los tests para las funciones en el módulo utils."""

    def setUp(self):
        """Método que se ejecuta antes de cada test para configurar el entorno."""
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Método que se ejecuta después de cada test para limpiar el entorno."""
        shutil.rmtree(self.temp_dir)

    def test_descomprime_zip(self):
        """Prueba unitaria para la función descomprime_zip."""
        # Archivo ZIP válido con archivos dentro
        zip_file = os.path.join(self.temp_dir, 'valid.zip')
        target_folder = self.temp_dir

        # Crear un archivo ZIP válido con archivos dentro
        with zipfile.ZipFile(zip_file, 'w') as zip_ref:
            zip_ref.writestr('file1.txt', 'Content of file1')

        utils.descomprime_zip(zip_file, target_folder)

        # Verificar que los archivos se hayan extraído correctamente
        extracted_file = os.path.join(target_folder, 'file1.txt')
        self.assertTrue(os.path.exists(extracted_file))
        with open(extracted_file) as file:
            self.assertEqual(file.read(), 'Content of file1')

        # Eliminar los archivos de prueba
        os.remove(zip_file)
        os.remove(extracted_file)

        # Archivo ZIP vacío
        zip_file = os.path.join(self.temp_dir, 'empty.zip')
        target_folder = self.temp_dir

        # Crear un archivo ZIP vacío
        with zipfile.ZipFile(zip_file, 'w'):
            pass

        utils.descomprime_zip(zip_file, target_folder)

        # Verificar que no se haya creado ningún archivo
        self.assertEqual(len(os.listdir(target_folder)), 1)

        # Archivo ZIP inválido
        zip_file = os.path.join(self.temp_dir, 'invalid.zip')
        target_folder = self.temp_dir

        # Crear un archivo ZIP inválido
        with open(zip_file, 'wb') as file:
            file.write(b'Invalid ZIP data')

        with self.assertRaises(zipfile.BadZipFile):
            utils.descomprime_zip(zip_file, target_folder)

        print("El test de descomprime_zip pasó correctamente.")

    def test_carga_dataset(self):
        """Prueba unitaria para la función carga_dataset."""
        # Crear un archivo CSV temporal
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
            csv_data = '''sentiment,id,date,query,user,text
                          0,1,2022-01-01,query1,user1,Hello
                          4,2,2022-01-02,query2,user2,World'''
            temp_file.write(csv_data)
            temp_file.close()

            # Cargar el dataset desde el archivo CSV temporal
            dataset = utils.carga_dataset(temp_file.name)

            # Verificar que se haya cargado el dataset correctamente
            self.assertGreaterEqual(len(dataset), 1, "Error: El número de registros es menor que el mínimo requerido")

            # Verificar la estructura de los registros
            registro_esperado = {
                'sentiment': '',
                'id': '',
                'date': '',
                'query': '',
                'user': '',
                'text': ''
            }
            for registro in dataset:
                self.assertIsInstance(registro, dict, "Error: El registro no es un diccionario")
                self.assertEqual(set(registro.keys()), set(registro_esperado.keys()),
                                 "Error: Las claves del registro no coinciden con la estructura esperada")

        print("La carga del dataset se completó exitosamente.")

    def test_preprocesar_texto(self):
        """Prueba unitaria para la función preprocesar_texto."""
        casos_prueba = [
            {
                'texto': "I Love #PYTHON! https://uoc.edu",
                'texto_esperado': "i love python"
            },
            {
                'texto': "This is a TEST!!! 12345",
                'texto_esperado': "this is a test 12345"
            },
            {
                'texto': "Hi my name is FRAN-",
                'texto_esperado': "hi my name is fran"
            },
            {
                'texto': "Python is AWEESOME",
                'texto_esperado': "python is aweesome"
            },
            {
                'texto': "",
                'texto_esperado': ""
            },
            {
                'texto': "!@#$%^&*()",
                'texto_esperado': ""
            },
            {
                'texto': "   Spaces at the Beginning and End   ",
                'texto_esperado': "spaces at the beginning and end"
            },
            {
                'texto': "UPPERCASE and lowercase",
                'texto_esperado': "uppercase and lowercase"
            },
            {
                'texto': "Coffee with    Milk ",
                'texto_esperado': "coffee with milk"
            },
            {
                'texto': "SpecialChars@123",
                'texto_esperado': "specialchars123"
            },
            {
                'texto': "Testing    Multiple    Spaces",
                'texto_esperado': "testing multiple spaces"
            },
        ]

        for caso in casos_prueba:
            with self.subTest(texto=caso['texto']):
                texto = caso['texto']
                texto_esperado = caso['texto_esperado']

                texto_preprocesado = utils.preprocesar_texto(texto)
                self.assertEqual(texto_preprocesado, texto_esperado, "Error: El texto preprocesado no coincide")

        print("El preprocesamiento del texto se completó exitosamente.")

    def test_eliminar_stopwords(self):
        """Prueba unitaria para la función eliminar_stopwords."""
        casos_prueba = [
            {
                'texto': "this is a test. i should to remove the stopwords.",
                'texto_esperado': "test. remove stopwords."
            },
            {
                'texto': "i love coding in python and r.",
                'texto_esperado': "love coding python r."
            },
            {
                'texto': "these are some common stopwords: a, an, the, and, or.",
                'texto_esperado': "common stopwords: a, an, the, and, or."
            },
            {
                'texto': "stopwords can affect the results of text analysis.",
                'texto_esperado': "stopwords affect results text analysis."
            },
            {
                'texto': "working on my project, just getting started!",
                'texto_esperado': "working project, getting started!"
            },
            {
                'texto': "great day at the beach with friends. #fun",
                'texto_esperado': "great day beach friends. #fun"
            },
            {
                'texto': "watching a movie, it is so thrilling!",
                'texto_esperado': "watching movie, thrilling!"
            },
            {
                'texto': "this is an example",
                'texto_esperado': "example"
            },
            {
                'texto': "the sun is shining",
                'texto_esperado': "sun shining"
            },
            {
                'texto': "a beautiful day",
                'texto_esperado': "beautiful day"
            },
            {
                'texto': "in the park",
                'texto_esperado': "park"
            },
        ]

        for caso in casos_prueba:
            with self.subTest(texto=caso['texto']):
                texto = caso['texto']
                texto_esperado = caso['texto_esperado']

                texto_sin_stopwords = utils.eliminar_stopwords(texto)
                self.assertEqual(texto_sin_stopwords, texto_esperado, "Error: El texto sin stopwords no coincide")

        print("El test_eliminar_stopwords se completó exitosamente.")

    def test_obtener_frecuencias_y_vocabulario(self):
        """Prueba unitaria para la función frecuencias_y_vocabulario."""
        # Definir el dataset de prueba con frases largas y palabras repetidas
        dataset = [
            {"text": "test sentence repeated words sentence"},
            {"text": "test sentence repeated test test words"},
            {"text": "new test"},
            {"text": "test vocabulary"},
            {"text": "words"}
        ]

        # Obtener las frecuencias y el vocabulario
        frecuencias, vocabulario = utils.obtener_frecuencias_y_vocabulario(dataset)

        # Verificar que las frecuencias sean una lista de diccionarios
        self.assertIsInstance(frecuencias, list)
        self.assertTrue(all(isinstance(freq, dict) for freq in frecuencias))

        # Verificar que el vocabulario sea una lista
        self.assertIsInstance(vocabulario, list)

        # Verificar las frecuencias de las frases
        frecuencias_esperadas = [
            {'test': 1, 'sentence': 2, 'repeated': 1, 'words': 1},
            {'test': 3, 'sentence': 1, 'repeated': 1, 'words': 1},
            {'new': 1, 'test': 1},
            {'test': 1, 'vocabulary': 1},
            {'words': 1}
        ]

        for idx, frecuencia_esperada in enumerate(frecuencias_esperadas):
            with self.subTest(frecuencia_esperada=frecuencia_esperada):
                self.assertDictEqual(frecuencias[idx], frecuencia_esperada)

        # Verificar el vocabulario
        vocabulario_esperado = ['test', 'sentence', 'repeated', 'words', 'new', 'vocabulary']
        self.assertCountEqual(vocabulario, vocabulario_esperado)

        print("El test obtener_frecuencias_y_vocabulario se completó exitosamente.")

    def test_agregar_frecuencias(self):
        """Prueba unitaria para la función agregar_frecuencias."""
        # Datos de prueba
        dataset = [
            {'sentiment': '', 'id': '', 'date': '', 'query': '', 'user': '', 'text': 'example text'},
            {'sentiment': '', 'id': '', 'date': '', 'query': '', 'user': '', 'text': 'another example'},
            {'sentiment': '', 'id': '', 'date': '', 'query': '', 'user': '', 'text': 'one more example'},
            {'sentiment': '', 'id': '', 'date': '', 'query': '', 'user': '', 'text': 'example example example'},
            {'sentiment': '', 'id': '', 'date': '', 'query': '', 'user': '', 'text': ''},
            {'sentiment': '', 'id': '', 'date': '', 'query': '', 'user': '', 'text': '   leading and trailing spaces '},
            {'sentiment': '', 'id': '', 'date': '', 'query': '', 'user': '', 'text': 'uppercase and lowercase'},
            {'sentiment': '', 'id': '', 'date': '', 'query': '', 'user': '', 'text': 'coffee with    milk'}
        ]

        # Ejecutar la función a probar
        utils.agregar_frecuencias(dataset)

        # Verificar los resultados
        self.assertEqual(dataset[0]['frecuencias'], {'example': 1, 'text': 1})
        self.assertEqual(dataset[1]['frecuencias'], {'another': 1, 'example': 1})
        self.assertEqual(dataset[2]['frecuencias'], {'one': 1, 'more': 1, 'example': 1})
        self.assertEqual(dataset[3]['frecuencias'], {'example': 3})
        self.assertEqual(dataset[4]['frecuencias'], {})
        self.assertEqual(dataset[5]['frecuencias'], {'leading': 1, 'and': 1, 'trailing': 1, 'spaces': 1})
        self.assertEqual(dataset[6]['frecuencias'], {'uppercase': 1, 'and': 1, 'lowercase': 1})
        self.assertEqual(dataset[7]['frecuencias'], {'coffee': 1, 'with': 1, 'milk': 1})

        print("El test agregar_frecuencias se completó exitosamente.")

    def test_obtener_numero_clusters(self):
        """Prueba unitaria para la función obtener_numero_clusters."""
        csv_file = 'data/twitter_processed.csv'

        # Obtener el número de clusters del dataset
        num_clusters = utils.obtener_numero_clusters(csv_file)

        # Verificar que el número de clusters sea mayor o igual que cero
        self.assertGreaterEqual(num_clusters, 0, "Error: El número de clusters no es mayor o igual que cero")

        # Verificar si se han generado clusters
        if num_clusters == 0:
            self.assertEqual(num_clusters, 0, "Error: No se han generado clusters en el dataset.")
        elif num_clusters == 1:
            self.assertEqual(num_clusters, 1, "Error: Se ha generado 1 cluster en el dataset.")
        else:
            self.assertGreater(num_clusters, 1, f"Error: Se han generado {num_clusters} clusters en el dataset.")

        # Verificar que el número de clusters sea consistente con los valores únicos de 'sentiment'
        dataset = pd.read_csv(csv_file)
        sentiment_values = dataset['sentiment'].unique()
        self.assertEqual(len(sentiment_values), num_clusters,
                         "Error: El número de clusters no coincide con los valores únicos de 'sentiment'")

        print("El test de obtener_numero_clusters pasó correctamente.")

    def test_verificar_elementos_vacios(self):
        """Prueba unitaria para la función verificar_elementos_vacios."""
        # Caso de prueba 1: Dataset sin elementos vacíos
        dataset1 = [
            {'sentiment': '0', 'id': '1', 'date': '2022-01-01', 'query': 'query1',
             'user': 'user1', 'text': 'Hello', 'frecuencias': {}},
            {'sentiment': '4', 'id': '2', 'date': '2022-01-02', 'query': 'query2',
             'user': 'user2', 'text': 'World', 'frecuencias': {}},
            {'sentiment': '0', 'id': '3', 'date': '2022-01-03', 'query': 'query3',
             'user': 'user3', 'text': 'Good morning', 'frecuencias': {}}
        ]
        porcentaje_vacios1 = utils.verificar_elementos_vacios(dataset1)
        self.assertAlmostEqual(porcentaje_vacios1, 0.0, delta=0.01,
                               msg="Error: Se encontraron elementos vacíos en el dataset1")

        # Caso de prueba 2: Dataset con un 50% de elementos vacíos en 'text'
        dataset2 = [
            {'sentiment': '0', 'id': '1', 'date': '2022-01-01', 'query': 'query1',
             'user': 'user1', 'text': '', 'frecuencias': {}},
            {'sentiment': '4', 'id': '2', 'date': '2022-01-02', 'query': 'query2',
             'user': 'user2', 'text': 'World', 'frecuencias': {}},
            {'sentiment': '0', 'id': '3', 'date': '2022-01-03', 'query': 'query3',
             'user': 'user3', 'text': 'DAD', 'frecuencias': {}},
            {'sentiment': '4', 'id': '4', 'date': '2022-01-04', 'query': 'query4',
             'user': 'user4', 'text': '', 'frecuencias': {}}
        ]
        porcentaje_vacios2 = utils.verificar_elementos_vacios(dataset2)
        self.assertAlmostEqual(porcentaje_vacios2, 50.0, delta=0.01,
                               msg="Error: El porcentaje de elementos vacíos en el dataset2 no es correcto")

        # Caso de prueba 3: Dataset con un 100% de elementos vacíos en 'text'
        dataset3 = [
            {'sentiment': '0', 'id': '1', 'date': '2022-01-01', 'query': 'query1',
             'user': 'user1', 'text': '', 'frecuencias': {}},
            {'sentiment': '4', 'id': '2', 'date': '2022-01-02', 'query': 'query2',
             'user': 'user2', 'text': '', 'frecuencias': {}},
            {'sentiment': '0', 'id': '3', 'date': '2022-01-03', 'query': 'query3',
             'user': 'user3', 'text': '', 'frecuencias': {}}
        ]
        porcentaje_vacios3 = utils.verificar_elementos_vacios(dataset3)
        self.assertAlmostEqual(porcentaje_vacios3, 100.0, delta=0.01,
                               msg="Error: El porcentaje de elementos vacíos en el dataset3 no es correcto")

        # Caso de prueba 4: Dataset vacío
        dataset4 = []
        porcentaje_vacios4 = utils.verificar_elementos_vacios(dataset4)
        self.assertAlmostEqual(porcentaje_vacios4, 100.0, delta=0.01,
                               msg="Error: El porcentaje de elementos vacíos en el dataset4 no es correcto")

        # Imprimir el resultado del test
        print("El test de verificar_elementos_vacios pasó correctamente.")

    def test_eliminar_elementos_nulos(self):
        """Prueba unitaria para la función eliminar_elementos_nulos."""
        # Caso 1: Dataset vacío
        dataset_vacio = []
        dataset_resultado = utils.eliminar_elementos_nulos(dataset_vacio)
        self.assertListEqual(dataset_resultado, [], "Error: El dataset resultado no debería contener elementos")

        # Caso 2: Dataset sin elementos nulos
        dataset_sin_nulos = [
            {'sentiment': '0', 'id': '1', 'date': '2022-01-01', 'query': 'query1', 'user': 'user1', 'text': 'Hello'},
            {'sentiment': '4', 'id': '2', 'date': '2022-01-02', 'query': 'query2', 'user': 'user2', 'text': 'World'}
        ]
        dataset_resultado = utils.eliminar_elementos_nulos(dataset_sin_nulos)
        self.assertListEqual(dataset_resultado, dataset_sin_nulos,
                             "Error: El dataset resultado no coincide con el original")

        # Caso 3: Dataset con elementos nulos
        dataset_con_nulos = [
            {'sentiment': '0', 'id': '1', 'date': '2022-01-01', 'query': 'query1', 'user': 'user1', 'text': ''},
            {'sentiment': '4', 'id': '2', 'date': '2022-01-02', 'query': 'query2', 'user': 'user2', 'text': 'Hello'},
            {'sentiment': '0', 'id': '3', 'date': '2022-01-03', 'query': 'query3', 'user': 'user3', 'text': ''}
        ]
        dataset_resultado = utils.eliminar_elementos_nulos(dataset_con_nulos)
        self.assertListEqual(dataset_resultado, [
            {'sentiment': '4', 'id': '2', 'date': '2022-01-02', 'query': 'query2', 'user': 'user2', 'text': 'Hello'}
        ], "Error: El dataset resultado no coincide con el esperado")

        # Caso 4: Dataset con elementos nulos en otros campos
        dataset_con_nulos_otros_campos = [
            {'sentiment': '0', 'id': '1', 'date': '2022-01-01', 'query': '', 'user': 'user1', 'text': 'Hello'},
            {'sentiment': '4', 'id': '', 'date': '2022-01-02', 'query': 'query2', 'user': 'user2', 'text': 'World'},
            {'sentiment': '0', 'id': '3', 'date': '2022-01-03', 'query': 'query3', 'user': 'user3',
             'text': 'Good morning'}
        ]
        dataset_resultado = utils.eliminar_elementos_nulos(dataset_con_nulos_otros_campos)
        self.assertListEqual(dataset_resultado, dataset_con_nulos_otros_campos,
                             "Error: El dataset resultado no coincide con el original")

        # Imprimir el resultado del test
        print("El test de eliminar_elementos_nulos pasó correctamente.")

    def test_generar_wordcloud_por_cluster(self):
        """Prueba unitaria para la función generar_stopords_por_cluster."""
        # Simular las funciones imshow y show
        mock_imshow = Mock()
        mock_show = Mock()

        # Comprobar las funciones imshow y show con los mocks
        with patch('matplotlib.pyplot.imshow', mock_imshow), \
                patch('matplotlib.pyplot.show', mock_show):
            # Llamar a la función
            dataset_sin_nulos = [
                {'sentiment': '0', 'id': '1', 'date': '2022-01-01', 'query': 'query1', 'user': 'user1',
                 'text': 'Hello', 'frecuencias': {}},
                {'sentiment': '1', 'id': '2', 'date': '2022-01-02', 'query': 'query2', 'user': 'user2',
                 'text': 'World', 'frecuencias': {}},
                {'sentiment': '0', 'id': '3', 'date': '2022-01-03', 'query': 'query3', 'user': 'user3',
                 'text': 'Good morning', 'frecuencias': {}}
            ]
            utils.generar_wordcloud_por_cluster(dataset_sin_nulos)

            # Verificar las llamadas a las funciones y los argumentos
            self.assertGreaterEqual(mock_imshow.call_count, 1)  # Verificar que se generó al menos 1 word cloud
            self.assertGreaterEqual(mock_show.call_count, 1)  # Verificar que se llamó a show() al menos 1 vez

            # Verificar los argumentos de la llamada a imshow
            self.assertEqual(mock_imshow.call_args[1]['interpolation'], 'bilinear')

            # Verificar el orden de las llamadas a las funciones
            self.assertEqual(mock_imshow.call_args_list[0], mock.call(mock.ANY, interpolation='bilinear'))

            # Imprimir el resultado del test
            print("El test de generar_wordcloud_por_cluster pasó correctamente.")

    def test_generar_histograma_por_cluster(self):
        """Prueba unitaria para la función generar_histograma_por_cluster."""
        # Estructura del dataset
        dataset = [
            {'sentiment': '0', 'id': '1', 'date': '2022-01-01', 'query': 'query1', 'user': 'user1',
             'text': 'Hello', 'frecuencias': {}}
        ]

        # Simular la función obtener_frecuencias_y_vocabulario
        with patch('utils.obtener_frecuencias_y_vocabulario') as mock_obtener_frecuencias_y_vocabulario:
            mock_obtener_frecuencias_y_vocabulario.return_value = (
                [{'Hello': 1}],
                {'Hello'}
            )

            # Simular la función plt.show
            with patch('matplotlib.pyplot.show') as mock_show:
                # Llamar a la función
                utils.generar_histograma_por_cluster(dataset)

                # Verificar las llamadas a las funciones y los argumentos
                mock_obtener_frecuencias_y_vocabulario.assert_called_once_with(dataset)
                mock_show.assert_called_once()

                # Imprimir el resultado del test
                print("El test de generar_histograma_por_cluster pasó correctamente.")
