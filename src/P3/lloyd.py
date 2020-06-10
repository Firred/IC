import numpy


class Lloyd:
    def __init__(self, x, epsilon, k, r):
        self.x = x
        self.epsilon = epsilon
        self.k = k
        self.r = r

    def execute(self, c):
        c = numpy.array(c)
        it = 0

        new_c = self.calculate_c(c)

        while (self.calculate_d(new_c, c) > self.epsilon).all() and (self.k > it):
            c = new_c
            new_c = self.calculate_c(new_c)
            it += 1

        return new_c

    def calculate_c(self, c):
        new_c = c.copy()

        for example in self.x:
            ex = (example - new_c)**2
            ex = numpy.sum(ex, axis=1)

            index = numpy.where(ex == numpy.amin(ex))

            new_c[index] = new_c[index] + self.r*(example - new_c[index])

        return new_c

    @staticmethod
    def calculate_d(x, y):
        diff = (x - y) ** 2

        diff = numpy.sum(diff, axis=1)

        return numpy.sqrt(diff)

    @staticmethod
    def get_classification(x, c, classes=None):
        diff = (x - c) ** 2

        cl = numpy.sum(diff, axis=1)

        if classes is None:
            c_type = numpy.where(cl == numpy.amin(cl))[0][0]
        else:
            c_type = classes[numpy.where(cl == numpy.amin(cl))][0]

        return c_type, cl
