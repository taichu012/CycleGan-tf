import tensorflow as tf
from blocks import build_blocks

class Discriminator:
    """Discriminator from CycleGAN Paper"""
    def __init__(self, name, params, use_sigmoid=False, is_training=True, verbose=False):
        self.name = name
        self.params = params.copy()
        self.is_training = is_training
        self.use_sigmoid = use_sigmoid
        self.variables = None
        self.verbose = verbose

    def __call__(self, inputs):
        with tf.variable_scope(self.name, reuse=self.params['reuse']):
            if self.verbose:
                print('Building Discriminator %s' % self.name)
            output = build_blocks([
                'C64N', 'C128', 'C256', 'C512x2', 'c1s1-1-N'
            ], self.params, is_training=self.is_training, verbose=self.verbose)(inputs)
            if self.use_sigmoid:
                output = tf.sigmoid(output, name='sigmoid')

        self.variables = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, scope=self.name)
        self.params['reuse'] = True

        return output