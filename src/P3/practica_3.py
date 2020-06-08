import pip
import argparse
import kmeans
import numpy

def import_or_install(package):
    try:
        __import__(package)
    except ImportError:
        pip.main(['install', package])


import_or_install("pandas")

from pandas.io.parsers import read_csv


def parse_demo(arg):
    switcher = {
        'Jugar': ("demo\AtributosJuego.txt", "demo\Juego.txt", "Jugar", "si", "no"),
        'Edificios': ("demo\AtributosEdificios.txt", "demo\Edificios.txt", "Clase", "+", "-"),
        'Creditos': ("demo\AtributosCreditos.txt", "demo\Clientes.txt", "Conceder", "Si", "No")
    }

    return switcher.get(arg, None)


def create_parser():
    parser = argparse.ArgumentParser("python practica_3.py")
    parser.add_argument("--examples", help="The name of the file that contains the list of examples.", type=str)
    parser.add_argument("--evaluation-column", help="The name of the column in attributes "
                                                    "that represents the evaluation value."
                                                    "By default the last column of attributes will be chosen.",
                        type=str)
    parser.add_argument("--output", help="The name of the output file with the result of the train", type=str)
    parser.add_argument("--train", help="The name of the train, the available trains are: [k-mean, bayes, lloyd].",
                        type=str)

    return parser


def get_mean(examples):
    ev_values = examples.iloc[:, -1].unique()
    grouped = examples.groupby(examples.columns[-1])

    list = []

    for value in ev_values:
        list.insert(len(list), grouped.get_group(value).iloc[:, :-1].mean())

    return list


if __name__ == "__main__":
    #parser = create_parser(demo_list)

    #args = parser.parse_args()

    examples = read_csv("data\prueba.txt", header=None)
    #examples = read_csv("data\Iris2Clases.txt", header=None)

    v = numpy.array([[6.7, 3.43], [2.39, 2.94]])
    #v = numpy.array([[4.6, 3.0, 4.0, 0.0],
    #                 [6.8, 3.4, 4.6, 0.7]])

    #v = get_mean(examples)

    ex = examples.iloc[:, :-1]
    classes = examples.iloc[:, -1].unique()

    print(classes)

    alg = kmeans.KMeans(ex.to_numpy(), 2, 0.01)

    v = alg.execute(v)

    test = numpy.array([2, 3])
    #test = read_csv("data\TestIris01.txt", header=None)
    #test = test.iloc[:, :-1].to_numpy()
    print("Ejecutar" + str(v))

    print(alg.get_classification(test, v))



