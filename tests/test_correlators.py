import numpy as np
import pyerrors as pe
import pytest

np.random.seed(0)


def test_function_overloading():
    corr_content_a = []
    corr_content_b = []
    for t in range(24):
        corr_content_a.append(pe.pseudo_Obs(np.random.normal(1e-10, 1e-8), 1e-4, 't'))
        corr_content_b.append(pe.pseudo_Obs(np.random.normal(1e8, 1e10), 1e7, 't'))

    corr_a = pe.correlators.Corr(corr_content_a)
    corr_b = pe.correlators.Corr(corr_content_b)

    fs = [lambda x: x[0] + x[1], lambda x: x[1] + x[0], lambda x: x[0] - x[1], lambda x: x[1] - x[0],
          lambda x: x[0] * x[1], lambda x: x[1] * x[0], lambda x: x[0] / x[1], lambda x: x[1] / x[0],
          lambda x: np.exp(x[0]), lambda x: np.sin(x[0]), lambda x: np.cos(x[0]), lambda x: np.tan(x[0]),
          lambda x: np.log(x[0] + 0.1), lambda x: np.sqrt(np.abs(x[0])),
          lambda x: np.sinh(x[0]), lambda x: np.cosh(x[0]), lambda x: np.tanh(x[0])]

    for i, f in enumerate(fs):
        t1 = f([corr_a, corr_b])
        for o_a, o_b, con in zip(corr_content_a, corr_content_b, t1.content):
            t2 = f([o_a, o_b])
            t2.gamma_method()
            assert np.isclose(con[0].value, t2.value)
            assert np.isclose(con[0].dvalue, t2.dvalue)
            assert np.allclose(con[0].deltas['t'], t2.deltas['t'])

def test_modify_correlator():
    corr_content = []
    for t in range(24):
        exponent = np.random.normal(3, 5)
        corr_content.append(pe.pseudo_Obs(2 + 10 ** exponent, 10 ** (exponent - 1), 't'))

    corr = pe.correlators.Corr(corr_content)

    with pytest.warns(RuntimeWarning):
        corr.symmetric()
    with pytest.warns(RuntimeWarning):
        corr.anti_symmetric()
    corr.roll(np.random.randint(100))
    corr.deriv(symmetric=True)
    corr.deriv(symmetric=False)
    corr.second_deriv()
