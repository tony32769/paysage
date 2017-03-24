from paysage import backends as be
from paysage import layers
from paysage.models import hidden

import pytest

def test_bernoulli_update():
    num_visible_units = 100
    num_hidden_units = 50
    batch_size = 25

    # set a seed for the random number generator
    be.set_seed()

    # set up some layer and model objects
    vis_layer = layers.BernoulliLayer(num_visible_units)
    hid_layer = layers.BernoulliLayer(num_hidden_units)
    rbm = hidden.Model([vis_layer, hid_layer])

    # randomly set the intrinsic model parameters
    a = be.randn((num_visible_units,))
    b = be.randn((num_hidden_units,))
    W = be.randn((num_visible_units, num_hidden_units))

    rbm.layers[0].int_params['loc'] = a
    rbm.layers[1].int_params['loc'] = b
    rbm.weights[0].int_params['matrix'] = W

    # generate a random batch of data
    vdata = rbm.layers[0].random((batch_size, num_visible_units))
    hdata = rbm.layers[1].random((batch_size, num_hidden_units))

    # compute extrinsic parameters
    hidden_field = be.dot(vdata, W) # (batch_size, num_hidden_units)
    hidden_field += be.broadcast(b, hidden_field)

    visible_field = be.dot(hdata, be.transpose(W)) # (batch_size, num_visible_units)
    visible_field += be.broadcast(a, visible_field)

    # update the extrinsic parameter using the layer functions
    rbm.layers[1].update(vdata, rbm.weights[0].W())
    rbm.layers[0].update(hdata, be.transpose(rbm.weights[0].W()))

    assert be.allclose(hidden_field, rbm.layers[1].ext_params['field']), \
    "hidden field wrong in bernoulli-bernoulli rbm"

    assert be.allclose(visible_field, rbm.layers[0].ext_params['field']), \
    "visible field wrong in bernoulli-bernoulli rbm"

def test_ising_update():
    num_visible_units = 100
    num_hidden_units = 50
    batch_size = 25

    # set a seed for the random number generator
    be.set_seed()

    # set up some layer and model objects
    vis_layer = layers.IsingLayer(num_visible_units)
    hid_layer = layers.IsingLayer(num_hidden_units)
    rbm = hidden.Model([vis_layer, hid_layer])

    # randomly set the intrinsic model parameters
    a = be.randn((num_visible_units,))
    b = be.randn((num_hidden_units,))
    W = be.randn((num_visible_units, num_hidden_units))

    rbm.layers[0].int_params['loc'] = a
    rbm.layers[1].int_params['loc'] = b
    rbm.weights[0].int_params['matrix'] = W

    # generate a random batch of data
    vdata = rbm.layers[0].random((batch_size, num_visible_units))
    hdata = rbm.layers[1].random((batch_size, num_hidden_units))

    # compute extrinsic parameters
    hidden_field = be.dot(vdata, W) # (batch_size, num_hidden_units)
    hidden_field += be.broadcast(b, hidden_field)

    visible_field = be.dot(hdata, be.transpose(W)) # (batch_size, num_visible_units)
    visible_field += be.broadcast(a, visible_field)

    # update the extrinsic parameter using the layer functions
    rbm.layers[1].update(vdata, rbm.weights[0].W())
    rbm.layers[0].update(hdata, be.transpose(rbm.weights[0].W()))

    assert be.allclose(hidden_field, rbm.layers[1].ext_params['field']), \
    "hidden field wrong in ising-ising rbm"

    assert be.allclose(visible_field, rbm.layers[0].ext_params['field']), \
    "visible field wrong in ising-ising rbm"

def test_exponential_update():
    num_visible_units = 100
    num_hidden_units = 50
    batch_size = 25

    # set a seed for the random number generator
    be.set_seed()

    # set up some layer and model objects
    vis_layer = layers.ExponentialLayer(num_visible_units)
    hid_layer = layers.ExponentialLayer(num_hidden_units)
    rbm = hidden.Model([vis_layer, hid_layer])

    # randomly set the intrinsic model parameters
    # for the exponential layers, we need a > 0, b > 0, and W < 0
    a = be.rand((num_visible_units,))
    b = be.rand((num_hidden_units,))
    W = -be.rand((num_visible_units, num_hidden_units))

    rbm.layers[0].int_params['loc'] = a
    rbm.layers[1].int_params['loc'] = b
    rbm.weights[0].int_params['matrix'] = W

    # generate a random batch of data
    vdata = rbm.layers[0].random((batch_size, num_visible_units))
    hdata = rbm.layers[1].random((batch_size, num_hidden_units))

    # compute extrinsic parameters
    hidden_rate = -be.dot(vdata, W) # (batch_size, num_hidden_units)
    hidden_rate += be.broadcast(b, hidden_rate)

    visible_rate = -be.dot(hdata, be.transpose(W)) # (batch_size, num_visible_units)
    visible_rate += be.broadcast(a, visible_rate)

    # update the extrinsic parameter using the layer functions
    rbm.layers[1].update(vdata, rbm.weights[0].W())
    rbm.layers[0].update(hdata, be.transpose(rbm.weights[0].W()))

    assert be.allclose(hidden_rate, rbm.layers[1].ext_params['rate']), \
    "hidden rate wrong in exponential-exponential rbm"

    assert be.allclose(visible_rate, rbm.layers[0].ext_params['rate']), \
    "visible rate wrong in exponential-exponential rbm"



if __name__ == "__main__":
    pytest.main([__file__])
