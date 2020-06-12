import numpy


class Bayes:
    def __init__(self, x, list=False):
        self.x = x
        self.list = list

    def execute(self, m):
        if not self.list:
            return self.calculate_c(m)
        else:
            return self.calculate_c_list(m)

    def calculate_c(self, m):
        m = numpy.array(m)

        diff = (self.x[:] - m[:, numpy.newaxis, :])

        mult = numpy.einsum('ijk,ikm->ijm', diff.transpose(0, 2, 1), diff)
        c = mult/self.x.shape[1]

        return c

    def calculate_c_list(self, m):
        m = numpy.array(m)

        for i in range(0, len(self.x)):
            matrix = self.x[i]
            diff = (matrix - m[i])

            mult = diff.T.dot(diff)
            c = mult / matrix.shape[0]

        return c

    @staticmethod
    def get_classification(x, m, c, classes=None):
        diff = (x - m)

        mult = numpy.einsum('ijk,ikm->im', diff[:, numpy.newaxis], numpy.linalg.pinv(c))

        mult = numpy.einsum('ijk,ki->i', mult[:, numpy.newaxis], diff.T)

        if classes is None:
            c_type = numpy.where(mult == numpy.amin(mult))[0][0]
        else:
            c_type = classes[numpy.where(mult == numpy.amin(mult))[0][0]]

        return c_type, mult
