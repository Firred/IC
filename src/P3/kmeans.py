import numpy


class KMeans:
    def __init__(self, x, b, epsilon):
        self.b = b
        self.epsilon = epsilon
        self.x = x

    def execute(self, v):
        u = self.calculate_u(v)

        new_v = self.calculate_v(u)

        while (self.calculate_d(new_v, v) >= self.epsilon).all():
            v = new_v
            u = self.calculate_u(v)

            new_v = self.calculate_v(u)

        return new_v

    def calculate_u(self, v):
        d = self.dij(self.x, v)

        d = 1/d

        if self.b > 2:
            d = numpy.power(d, (1/(self.b-1)))

        tot_d = numpy.sum(d, axis=1)

        return d.T/tot_d

    def calculate_v(self, u):
        if self.b != 1:
            u = u**self.b

        sum_p = numpy.sum(u, axis=1)

        new_v = (self.x.T[:, numpy.newaxis] * u)
        new_v = numpy.sum(new_v, axis=2)
        new_v = new_v/sum_p

        return new_v.T

    @staticmethod
    def dij(x, v):
        d = (x[:, numpy.newaxis] - v)
        d = d**2

        d = numpy.sum(d, axis=2)

        return d

    @staticmethod
    def calculate_d(x, y):
        diff = (x - y)**2

        diff = numpy.sum(diff, axis=0)
        return numpy.sqrt(diff)

    @staticmethod
    def get_classification(x, v, classes=None):
        diff = (x - v) ** 2

        diff = numpy.sum(diff, axis=1)

        if classes is None:
            c_type = numpy.where(diff == numpy.amin(diff))[0][0]
        else:
            c_type = classes[numpy.where(diff == numpy.amin(diff))[0][0]]

        return c_type, diff
