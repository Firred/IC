import sys
import os
import argparse
from pandas.io.parsers import read_csv
import numpy as np
import math
import anytree
from anytree.exporter import UniqueDotExporter
import pydot

node_id = 0


def id3(examples, ev_column, attr, tree_graf=None):
    global node_id
    node_id += 1

    if len(examples) <= 0:
        return

    if examples[ev_column[0]].all():
        anytree.Node(ev_column[1], tree_graf, label=str(node_id))
        return

    elif (examples[ev_column[0]] == False).all():
        anytree.Node(ev_column[2], tree_graf, label=str(node_id))
        return

    elif len(attr) <= 0:
        raise Exception("No attributes left.")

    else:
        merits = calculate_merit(examples, ev_column[0], attr)

        best = merits[-1][0]

        print("Atributo elegido: " + str(merits[-1]))

        new_attr = attr[:]
        new_attr.remove(best)

        if tree_graf is None:
            root = anytree.Node(best, label=str(node_id))
        else:
            root = anytree.Node(best, tree_graf, label=str(node_id))

        for value in examples[best].unique():
            new_examples = examples[examples[best] == value]

            node_id += 1

            node_value = anytree.Node(value, root, label=str(node_id))

            id3(new_examples, ev_column, new_attr, node_value)

    return root


def calculate_merit(data, evaluation_column, attr):
    distribution = get_attribute_distribution(data, evaluation_column, attr)

    transformed_distribution = transform_distribution(distribution[0], distribution[1])

    merits = []

    for attr in transformed_distribution:
        merit = get_merit(attr[1], attr[2], attr[3])
        merits.insert(0, (attr[0], merit))

    merits = sorted(merits, reverse=True, key=lambda x: x[1])

    return merits


def alg(data, evaluation_column, positive=None, negative=None, output="result"):
    if positive is None:
        ev_values = data[evaluation_column].unique()

        if len(ev_values) == 2:
            positive = ev_values[0]
            negative = ev_values[1]
        else:
            raise Exception("La columna de evaluacion tiene mas de 2 valores posibles.")

    data[evaluation_column] = data[evaluation_column].replace(positive, True)
    data[evaluation_column] = data[evaluation_column].replace(negative, False)

    attr = list(filter(lambda key: key != evaluation_column, data.keys()))
    merits = calculate_merit(data, evaluation_column, attr)

    print("Meritos: " + str(merits))

    print('Ejemplos:')
    print(data)

    print("id3: ")

    try:
        result = id3(data, (evaluation_column, positive, negative), attr)
    except Exception:
        print("No quedan atributos.")
        return

    for pre, fill, node in anytree.RenderTree(result):
        print("%s%s" % (pre, node.name))

    try:
        UniqueDotExporter(result).to_dotfile("results/" + output + ".dot")
        (graph,) = pydot.graph_from_dot_file("results/" + output + ".dot")
        graph.write_png("results/" + output + ".png")
    except Exception:
        print("Error al generar el grafico, compruebe que pydot y graphviz estan "
              "instalados usando 'pip install pydot graphviz' y la carpeta 'results' existe en el mismo directorio "
              "que practica_2.py y vuelva a intentarlo")


def infor(p, n):
    infors = np.zeros((len(p)))
    for i in range(0, len(p)):
        # La comprobación evita MathError en log(p) y log(n) cuando p ó n =0
        if p[i] == 0:
            p_log = 0
        else:
            p_log = - p[i] * math.log2(p[i])

        if n[i] == 0:
            n_log = 0
        else:
            n_log = - n[i] * math.log2(n[i])

        infors[i] = p_log + n_log

    return infors


def get_merit(attribute_distribution):
    merit = 0

    for values in attribute_distribution:
        merit += values[0] * infor(values[1], values[2])

    return merit


def get_merit(r, p, n):
    merit = r * infor(p, n)

    return merit.sum(axis=0)


def transform_distribution(dist, number_examples):
    trans_dist = []

    for attr in dist:
        total_value = attr[1].sum(axis=1)
        r = total_value / number_examples

        p_n = attr[1] / total_value[:, None]

        trans_dist.insert(0, (attr[0], r, p_n[:, 0], p_n[:, 1]))

    return trans_dist


def get_attribute_distribution(data, evaluation_column, keys):
    grouped = data.groupby(evaluation_column)

    number_examples = len(data)

    positives = grouped.get_group(True)
    negatives = grouped.get_group(False)

    final_dist = []

    for attribute in keys:
        pos_counts = positives[attribute].value_counts()
        neg_counts = negatives[attribute].value_counts()

        if len(neg_counts.keys()) < len(pos_counts.keys()):
            result = (attribute, extract_data(pos_counts, neg_counts, pos_counts.keys()))

        else:
            result = (attribute, extract_data(pos_counts, neg_counts, neg_counts.keys()))

        final_dist.insert(0, result)

    return final_dist, number_examples


def extract_data(pos, neg, values):
    final_matrix = np.zeros([len(values), 2])
    i = 0

    for value in values:
        final_matrix[i][0] = pos.get(value, 0)
        final_matrix[i][1] = neg.get(value, 0)

        i += 1

    return final_matrix


def parse_demo(arg):
    switcher = {
        'Jugar': ("demo\AtributosJuego.txt", "demo\Juego.txt", "Jugar", "si", "no"),
        'Edificios': ("demo\AtributosEdificios.txt", "demo\Edificios.txt", "Clase", "+", "-"),
        'Creditos': ("demo\AtributosCreditos.txt", "demo\Clientes.txt", "Conceder", "Si", "No")
    }

    return switcher.get(arg, None)


def create_parser(demo_list):
    parser = argparse.ArgumentParser("python practica_2.py")
    parser.add_argument("--demo",
                        help="Name of the demo that you want to play. It doesn't require any other parameter. "
                             "Options: " + str(demo_list) +
                             " (Default: Juego)",
                        type=str)
    parser.add_argument("--attributes", help="The name of the file that contains the list of attributes.", type=str)
    parser.add_argument("--examples", help="The name of the file that contains the list of examples.", type=str)
    parser.add_argument("--evaluation-column", help="The name of the column in attributes "
                                                    "that represents the evaluation value."
                                                    "By default the last column of attributes will be chosen.", type=str)
    parser.add_argument("--output", help="The name of the output file, "
                                         "by default it will be the name of the 'examples' file. "
                                         "DO NOT USE ANY EXTENSION, "
                                         "the script generates 2 files, a *.dot and a *.png", type=str)

    return parser


def process_args(args):
    demo = parse_demo(args.demo)
    header = None
    examples = None
    ev_column = None

    # attribute and examples introduced
    if (args.attributes is not None) and (args.examples is not None):
        header = read_csv(args.attributes, header=None).values
        examples = read_csv(args.examples, names=header[0])

        # evaluation_column introduced
        if args.evaluation_column is not None:
            ev_column = args.evaluation_column
        else:
            # gets last column
            ev_column = header[0][-1]

    # attribute and examples not introduced
    elif (args.attributes is None) and (args.examples is None):
        if args.demo is not None:
            demo = parse_demo(args.demo)

            if demo is not None:
                header = read_csv(demo[0], header=None).values
                examples = read_csv(demo[1], names=header[0])
            else:
                print("--demo debe contener uno de los siguientes valores: " + str(demo_list))

        else:
            demo = parse_demo("Jugar")

            header = read_csv(demo[0], header=None).values
            examples = read_csv(demo[1], names=header[0])
    else:
        print("Es necesario introducir --attribute y --examples simulaneamente. Si desea probar los casos de ejemoplo, "
              "use la opcion --demo.")
        return None

    if args.output is None:
        if demo is not None:
            file = os.path.basename(demo[1])
        else:
            file = os.path.basename(args.examples)

        output = os.path.splitext(file)[0]
    else:
        output = args.output

    return demo, header, examples, ev_column, output


if __name__ == "__main__":
    demo_list = ["Juego", "Edificios", "Creditos"]

    parser = create_parser(demo_list)

    args = parser.parse_args()

    try:
        demo, header, examples, ev_column, output = process_args(args)

        try:
            if demo is not None:
                alg(examples, demo[2], demo[3], demo[4], output)
            else:
                alg(examples, ev_column, output=output)

            print("Resultados generados en la carpeta results bajo el nombre de " + output + ".")
        except Exception as ex:
            print("Error en la ejecucion: ", ex)
    except TypeError:
        print("Error en los argumentos.")
