import pip
import argparse
import numpy
import math
import kmeans
import bayes
import lloyd


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


def exec_kmeans(file, b, epsilon, v=None):
    examples = read_csv(file, header=None)

    if v is None:
        v = get_mean(examples)

    ex = examples.iloc[:, :-1]
    classes = examples.iloc[:, -1].unique()

    alg = kmeans.KMeans(ex.to_numpy(), b, epsilon)

    return classes, alg.execute(v)


def exec_bayes(file):
    examples = read_csv(file, header=None)
    grouped = examples.groupby(examples.columns[-1])
    m = get_mean(examples)

    list = []

    for value in examples.iloc[:, -1].unique():
        list.insert(len(list), grouped.get_group(value).iloc[:, :-1].to_numpy())

    if all(x == grouped.count()[0][0] for x in grouped.count()[0]):
        ex = numpy.array(list)

        alg = bayes.Bayes(ex)
    else:
        alg = bayes.Bayes(list, True)

    return m, alg.execute(m)


def exec_lloyd(file, epsilon=math.pow(10,-10), c=None, k=10, r=0.1):
    examples = read_csv(file, header=None)

    if c is None:
        c = get_mean(examples)

    ex = examples.iloc[:, :-1].to_numpy()

    alg = lloyd.Lloyd(ex, epsilon, k, r)

    return alg.execute(c)


if __name__ == "__main__":
    #parser = create_parser(demo_list)

    #args = parser.parse_args()

    #v = numpy.array([[6.7, 3.43], [2.39, 2.94]])
    #v = numpy.array([[4.6, 3.0, 4.0, 0.0],
    #                 [6.8, 3.4, 4.6, 0.7]])

    #classes, v = exec_kmeans("data\Iris2Clases.txt", 2, 0.01, v)

    #test = numpy.array([2, 3])
    #print("Ejecutar" + str(v))

    #print(kmeans.KMeans.get_classification(test, v, classes))

    #m, u = exec_bayes("data\pruebabayes.txt")
    #m, u = exec_bayes("data\Iris2Clases.txt")
    #print(bayes.Bayes.get_classification(test, m, u, classes))


    #exec_lloyd("data\pruebabayes.txt", epsilon=0.1)
    #c = exec_lloyd("data\Iris2Clases.txt")

    #print(lloyd.Lloyd.get_classification(test, c, classes))

    file = "data\Iris2Clases.txt"

    classes, v = exec_kmeans(file, 2, 0.01)
    m, u = exec_bayes(file)
    c = exec_lloyd(file)

    test = read_csv("data\TestIris01.txt", header=None)
    test = test.iloc[:, :-1].to_numpy()

    #test = numpy.array([3, 7])

    print(kmeans.KMeans.get_classification(test, v, classes))
    print(bayes.Bayes.get_classification(test, m, u, classes))
    print(lloyd.Lloyd.get_classification(test, c, classes))