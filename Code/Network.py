import tensorflow as tf
import numpy as np


def weight_variable(shape):
    initial = tf.random_uniform(shape, 0.0, 1.0)
    return tf.Variable(initial)

def bias_variable(shape):
    initial = tf.random_uniform(shape, 0.095, 0.105)
    return tf.Variable(initial)

def LeakyReLU(x, alpha=1e-1):
    return tf.maximum(alpha*x, x)


class FCLayer:
    """A fully connected layer.

    INPUT_DIM  -- input vector dimensionality
    OUTPUT_DIM -- output vector dimensionality
    """
    def __init__(self, input_dim, output_dim, nonlinearity=tf.nn.relu):
        """
        Arguments:
            input_dim  -- input vector dimensionality
            output_dim -- output vector dimensionality
            nonlinearity -- the activation function (a tensorflow op)
        """
        self.W = weight_variable([output_dim, input_dim])
        self.b = bias_variable([output_dim])
        self.nonlinearity = nonlinearity
        self.INPUT_DIM = input_dim
        self.OUTPUT_DIM = output_dim

    def forward(self, X):
        """Forwards the input vector through this fully connected layer.
        """
        s = tf.matmul(X, tf.transpose(self.W)) + self.b
        return self.nonlinearity(s)


class GroupLayer:
    """A custom locally-connected layer.
    It consists of fully-connected local parts (sublayers).
    Basically, several FC layers in parallel.

    INPUT_DIM  -- input vector dimensionality
    OUTPUT_DIM -- output vector dimensionality
    """

    def __init__(self, input_groups, output_groups, nonlinearity=tf.nn.relu):
        """
        Arguments:
            input_groups  -- a list of sublayer input sizes
            output_groups -- a list of sublayer output sizes
            nonlinearity  -- the activation function (a tensorflow op)
        """
        # determine boundaries of locally connected regions
        self.boundaries = [sum(input_groups[:i])
                            for i in range(len(input_groups)+1)]

        self.INPUT_DIM = self.boundaries[-1]        # informative,
        self.OUTPUT_DIM = sum(output_groups)        #   really.

        self.sublayers = []
        for (ingroup, outgroup) in zip(input_groups, output_groups):
            self.sublayers += [FCLayer(ingroup, outgroup, nonlinearity)]


    def forward(self, X):
        """Forwards the input vector through this locally-connected layer.

        Arguments:
            X -- a tensorflow tensor/placeholder of appropriate dimensions
                 (N x INPUT_DIM, where N is the number of individual samples,
                  i.e. they are laid out in rows)
        """
        h = []
        for i, subl in enumerate(self.sublayers):
            h += [subl.forward(X[: , self.boundaries[i] : self.boundaries[i+1]])]
        return tf.concat(1, h)


# group_dimens - 2D matrica, u prvom retku su dimenzije ulaza svake grupe
# a u drugom dimenzije izlaza
# [[10, 10, 20], [4, 4, 1]] će biti sloj sa 40 ulaza i 9 izlaza
# prva vrijednost u architecture mora biti jednaka sumi prve dimenzija group_dimens
# druga vrijednost u architecture je jednaka sumi vrijednosti druge dimenzije group_dimens
class NNetwork:
    """A 2-layer neural network.
    FC_dim -- dimensions of hidden layers after the group layer.
    """

    def __init__(self, LC_groups, FC_dim):

        (LC_ingroups, LC_outgroups) = LC_groups
        D = sum(LC_ingroups)    # input layer dimensionality
        H = sum(LC_outgroups)   # hidden layer dimensionality
        C = FC_dim              # output dimensionalities

        self.layers = [GroupLayer(LC_ingroups, LC_outgroups,
                                      nonlinearity=tf.nn.relu)]
        for i in range(len(C)-1):
            self.layers += [FCLayer(H, C[i], nonlinearity=tf.nn.relu)]
            H = C[i]
        self.layers += [FCLayer(H, C[-1], nonlinearity=tf.nn.tanh)]
        #self.layers += [FCLayer(H, C, nonlinearity=tf.sigmoid)]

        # samples
        self.X = tf.placeholder(tf.float32, [None, D])    # N x D
        self.Y = tf.placeholder(tf.float32, [None, C[-1]])    # N x C

        # output
        self.out = self.X
        for l in self.layers:
            self.out = l.forward(self.out)

        # loss
        self.loss = tf.reduce_sum((self.out - self.Y)**2)

        # train step & session
        self.lr = tf.placeholder(tf.float32, shape=[])
        optimizer = tf.train.GradientDescentOptimizer(self.lr)
        optimizer = tf.train.AdamOptimizer(self.lr)
        self.train_step = optimizer.minimize(self.loss)
        self.session = tf.Session()
        self.session.run( tf.initialize_all_variables() )


    def train(self, X, Y_, n_iter, learning_rate):
        self.session.run( tf.initialize_all_variables() )

        errs = [];
        for i in range(n_iter):
            feed_dict = {self.X: X, self.Y: Y_, self.lr: learning_rate}
            fetches = [self.loss, self.train_step]

            (loss, _) = self.session.run(fetches, feed_dict=feed_dict)
            errs += [loss]

            if i%10==0 or i==n_iter-1:
                t = self.predict(X)

        return errs;


    def predict(self, X):
        return self.out.eval(feed_dict={self.X: X}, session=self.session)


def test():
    X = np.array([
        [0,0],
        [0,1],
        [1,0],
        [1,1]])
    Y = np.array([
        [1,0],
        [0,1],
        [0,1],
        [1,0]])
    #Y = np.array([[0,1,1,0]]).T

    tf.set_random_seed(42)

    eta=1e-2; niter=1000
    print("lr={}, niter={}".format(eta, niter))

    net = NNetwork(LC_groups=([2],[2]), FC_dim=[2], learning_rate=eta)
    errs = net.train(X, Y, n_iter=niter)
    print(net.predict(X))

if __name__=="__main__":
    test()
