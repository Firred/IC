import pip
import os
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


def create_parser():
    parser = argparse.ArgumentParser("python practica_3.py")
    parser.add_argument("--input", help="The name of the file that contains the list of examples "
                                        "or the data to classify.", type=str)
    parser.add_argument("--demo", help="Use this argument to execute a demo training with the 3 algorithms and "
                                       "test them with one classification.",
                        action='store_true', default=False)
    parser.add_argument("--classify", help="Use this argument to execute a classification.",
                        action='store_true', default=False)
    parser.add_argument("--training", help="The name of the training, the available trains are: [kmeans, bayes, lloyd]."
                        , type=str)
    parser.add_argument("--results", help="The name of the file (no extension) with the result of the training."
                                         " In a training, it will be a new file with the result "
                                         "(one .txt with the classes and one .npy/.npz with the matrix's results."
                                         " In a classification, it's the generic name "
                                         "(the name without '_bayes.txt', '_lloyd.npy', etc) of the files in "
                                         "the directory 'results' that contains the results of a previous training",
                        type=str)
    parser.add_argument("--b", help="Value of b in K-Means training. Default: 2", type=int)
    parser.add_argument("--epsilon", help="Value of epsilon in K-Means and Lloyd trainings."
                                          " Default: 0.01 for K-Means and 10+e-10 for Lloyd", type=float)
    parser.add_argument("--k", help="Value of k (maximum of iterations) in Lloyd training. Default: 10", type=int)
    parser.add_argument("--r", help="Value of r (learning ratio) in Lloyd training. Default: 0.1", type=float)

    return parser


def get_mean(examples):
    ev_values = examples.iloc[:, -1].unique()
    grouped = examples.groupby(examples.columns[-1])

    list = []

    for value in ev_values:
        list.insert(len(list), grouped.get_group(value).iloc[:, :-1].mean())

    return list


def exec_kmeans(file, b=2, epsilon=0.01, v=None):
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
    classes = examples.iloc[:, -1].unique()

    list = []

    for value in examples.iloc[:, -1].unique():
        list.insert(len(list), grouped.get_group(value).iloc[:, :-1].to_numpy())

    if all(x == grouped.count()[0][0] for x in grouped.count()[0]):
        ex = numpy.array(list)

        alg = bayes.Bayes(ex)
    else:
        alg = bayes.Bayes(list, True)

    return classes, numpy.array(m), numpy.array(alg.execute(m))


def exec_lloyd(file, epsilon=math.pow(10, -10), c=None, k=10, r=0.1):
    examples = read_csv(file, header=None)

    classes = examples.iloc[:, -1].unique()

    if c is None:
        c = get_mean(examples)

    ex = examples.iloc[:, :-1].to_numpy()

    alg = lloyd.Lloyd(ex, epsilon, k, r)

    return classes, alg.execute(c)


def save_and_show(output, classes, v, m, u, c):
    with open(output + "_classes.txt", 'w') as f:
        for cl in classes:
            f.write(cl + "\n")

    print("Training result for K-Means: \nv:\n", v)
    numpy.save(output + "_kmeans.npy", v)

    print("\nTraining result for Bayes: \nm:\n", m, "\nU:\n", u)
    numpy.savez(output + "_bayes.npz", m, u, m=m, u=u)

    print("\nTraining result for Lloyd: \nC:\n", c)
    numpy.save(output + "_lloyd.npy", c)


def execute(args):
    #Demo
    if args.demo is True:
        file = "data\pruebabayes.txt"

        v = get_mean(read_csv(file, header=None))

        classes, v = exec_kmeans(file, 2, 0.1, v)
        m, u = exec_bayes(file)[1:]
        c = exec_lloyd(file)[1]

        print("K-Means:")
        print(v)

        print("\nBayes:")
        print(u)

        print("\nLloyd:")
        print(c)

        test = numpy.array([3, 7])

        print("\nK-Means Classification:\n" + str(kmeans.KMeans.get_classification(test, v, classes)))
        print("\nBayes Classification:\n" + str(bayes.Bayes.get_classification(test, m, u, classes)))
        print("\nLloyd Classification:\n" + str(lloyd.Lloyd.get_classification(test, c, classes)))

    #Ejecuta archivo
    elif args.input is not None:
        #Clasificar archivo
        if args.classify is True:
            if args.results is not None:
                classes = []
                with open("./results/" + args.results + "_classes.txt", "r") as file:
                    for line in file:
                        classes.append(line[:-1])

                print("Clases: ", classes)

                x = read_csv(args.input, header=None).iloc[:, :-1].to_numpy()
                print("\nClassification for:\n", x)

                if args.training is None:
                    v = numpy.load("./results/" + args.results + "_kmeans.npy")
                    values = numpy.load("./results/" + args.results + "_bayes.npz")
                    c = numpy.load("./results/" + args.results + "_lloyd.npy")

                    print("Kmeans: ", kmeans.KMeans.get_classification(x, v, classes))
                    print("Bayes: ", bayes.Bayes.get_classification(x, values['m'], values['u'], classes))
                    print("Lloyd: ", lloyd.Lloyd.get_classification(x, c, classes))

                elif args.training == "kmeans":
                    v = numpy.load("./results/" + args.results + "_kmeans.npy")
                    print("Kmeans: ", kmeans.KMeans.get_classification(x, v, classes))

                elif args.training == "bayes":
                    values = numpy.load("./results/" + args.results + "_bayes.npz")
                    print("Bayes: ", bayes.Bayes.get_classification(x, values['m'], values['u'], classes))

                elif args.training == "lloyd":
                    c = numpy.load("./results/" + args.results + "_lloyd.npy")
                    print("Lloyd: ", lloyd.Lloyd.get_classification(x, c, classes))

                else:
                    print("Incorrect training name. Available trainings: 'kmeans', 'bayes' and 'lloyd'")

            else:
                print("It's necessary to introduce a --results parameter with the generic "
                      "name of the files that contains the results of a training")

        #Entrenar ejemplos
        else:
            if args.epsilon is not None:
                epsilon = args.epsilon
            else:
                epsilon = None

            if args.b is not None:
                b = args.b
            else:
                b = 2

            if args.k is not None:
                k = args.k
            else:
                k = 10

            if args.r is not None:
                r = args.r
            else:
                r = 0.1

            file = args.input
            if args.results is None:
                output = os.path.basename(args.input)
                output = os.path.splitext(output)[0]
            else:
                output = os.path.basename(args.results)

            output = "./results/" + output

            if args.training is None:
                if epsilon is not None:
                    classes, v = exec_kmeans(file, b, epsilon)
                else:
                    classes, v = exec_kmeans(file, b)

                m, u = exec_bayes(file)[1:]

                if epsilon is not None:
                    c = exec_lloyd(file, epsilon, k=k, r=r)[1]
                else:
                    c = exec_lloyd(file, k=k, r=r)[1]

                save_and_show(output, classes, v, m, u, c)
            else:
                if args.training == "kmeans":
                    if epsilon is not None:
                        classes, v = exec_kmeans(file, b, epsilon)
                    else:
                        classes, v = exec_kmeans(file, b)

                    with open(output + "_classes.txt", 'w') as f:
                        for cl in classes:
                            f.write(cl + "\n")

                    numpy.save(output + "_kmeans.npy", v)

                    print("Training result: \nv:\n", v)

                elif args.training == "bayes":
                    classes, m, u = exec_bayes(file)

                    with open(output + "_classes.txt", 'w') as f:
                        for cl in classes:
                            f.write(cl + "\n")

                    numpy.savez(output + "_bayes.npz", m, u, m=m, u=u)

                    print("\nTraining result: \nm:\n", m, "\nU:\n", u)

                elif args.training == "lloyd":
                    if epsilon is not None:
                        classes, c = exec_lloyd(file, epsilon, k=k, r=r)
                    else:
                        classes, c = exec_lloyd(file, k=k, r=r)

                    with open(output + "_classes.txt", 'w') as f:
                        for cl in classes:
                            f.write(cl + "\n")

                    numpy.save(output + "_lloyd.npy", c)

                    print("\nTraining result: \nC:\n", c)
                else:
                    print("Invalid training.")

    #Default: Iris
    else:
        #Entrenamiento
        if args.classify is False:
            if args.results is not None:
                output = "./results/" + args.results
            else:
                output = "./results/iris"

            file = "data\Iris2Clases.txt"

            v = numpy.array([[4.6, 3.0, 4.0, 0.0],
                            [6.8, 3.4, 4.6, 0.7]])

            classes, v = exec_kmeans(file, 2, math.pow(10, -10), v)
            m, u = exec_bayes(file)[1:]
            c = exec_lloyd(file, c=v)[1]

            save_and_show(output, classes, v, m, u, c)

        #Clasificacion
        else:
            classes = []
            with open("./results/iris_classes.txt", "r") as file:
                for line in file:
                    classes.append(line[:-1])

            v = numpy.load("./results/iris_kmeans.npy")
            values = numpy.load("./results/iris_bayes.npz")
            c = numpy.load("./results/iris_lloyd.npy")

            tests = ["./data/TestIris01.txt", "./data/TestIris02.txt", "./data/TestIris03.txt"]

            print("Clases: ", classes)

            for test in tests:
                x = read_csv(test, header=None).iloc[:, :-1].to_numpy()

                print("\nClassification for:\n", x)

                print("Kmeans: ", kmeans.KMeans.get_classification(x, v, classes))
                print("Bayes: ", bayes.Bayes.get_classification(x, values['m'], values['u'], classes))
                print("Lloyd: ", lloyd.Lloyd.get_classification(x, c, classes))


if __name__ == "__main__":
    parser = create_parser()

    args = parser.parse_args()


    execute(args)
