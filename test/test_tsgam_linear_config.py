# Copyright (c) 2025 Alliance for Sustainable Energy, LLC and Nimish Telang
# SPDX-License-Identifier: BSD-3-Clause

"""
Test LinearConfig support in Estimator.

Tests that LinearConfig works correctly for fit, predict, and sample,
both alone and mixed with SplineConfig.
"""

import numpy as np
import pandas as pd
import pytest
from signaldecomp import make_offset_basis

from tsgam import (
    ArConfig,
    Estimator,
    EstimatorConfig,
    LinearConfig,
    MultiPeriodicConfig,
    SolverConfig,
    SplineConfig,
)


def _make_data(n_samples=500, n_exog=1, seed=42):
    rng = np.random.default_rng(seed)
    timestamps = pd.date_range("2020-01-01", periods=n_samples, freq="1h")
    exog = {f"x{i}": rng.standard_normal(n_samples) for i in range(n_exog)}
    X = pd.DataFrame(exog, index=timestamps)
    y = 3.0 + 0.5 * X.iloc[:, 0].values + rng.standard_normal(n_samples) * 0.1
    return X, y


def test_exogenous_offset_sign_convention():
    """Negative offsets select past rows; positive offsets select future rows."""
    values = np.arange(5.0).reshape(-1, 1)
    lag = make_offset_basis(values, offsets=(1,))
    lead = make_offset_basis(values, offsets=(-1,))
    np.testing.assert_equal(
        np.where(lag.valid_mask[:, None], lag.design, np.nan).ravel(),
        np.array([np.nan, 0.0, 1.0, 2.0, 3.0]),
    )
    np.testing.assert_equal(
        np.where(lead.valid_mask[:, None], lead.design, np.nan).ravel(),
        np.array([1.0, 2.0, 3.0, 4.0, np.nan]),
    )


def test_explicit_spline_knots_fit_and_are_preserved():
    X, y = _make_data(n_samples=80)
    knots = np.linspace(X["x0"].min(), X["x0"].max(), 5)
    estimator = Estimator(
        EstimatorConfig(
            multi_periodic_config=None,
            exog_config=[SplineConfig(n_knots=None, knots=knots)],
        )
    ).fit(X, y)

    np.testing.assert_allclose(estimator.exog_knots_[0], knots)


@pytest.fixture
def solver_config():
    return SolverConfig(solver="CLARABEL", verbose=False)


class TestLinearConfigFitPredict:
    def test_single_linear_exog(self, solver_config):
        X, y = _make_data()
        config = EstimatorConfig(
            multi_periodic_config=None,
            exog_config=[LinearConfig(lags=[0])],
            solver_config=solver_config,
        )
        est = Estimator(config=config)
        est.fit(X, y)
        preds = est.predict(X)
        assert preds.shape == (len(X),)
        assert not np.any(np.isnan(preds))

    def test_linear_exog_with_lags(self, solver_config):
        X, y = _make_data()
        config = EstimatorConfig(
            multi_periodic_config=None,
            exog_config=[LinearConfig(lags=[-1, 0, 1])],
            solver_config=solver_config,
        )
        est = Estimator(config=config)
        est.fit(X, y)
        preds = est.predict(X)
        assert preds.shape == (len(X),)
        assert np.all(np.isfinite(preds[1:-1]))
        assert np.all(np.isnan(preds[[0, -1]]))

    def test_linear_with_fourier(self, solver_config):
        X, y = _make_data()
        config = EstimatorConfig(
            multi_periodic_config=MultiPeriodicConfig(
                num_harmonics=[3], periods=[24]
            ),
            exog_config=[LinearConfig(lags=[0])],
            solver_config=solver_config,
        )
        est = Estimator(config=config)
        est.fit(X, y)
        preds = est.predict(X)
        assert preds.shape == (len(X),)
        assert not np.any(np.isnan(preds))

    def test_mixed_spline_and_linear(self, solver_config):
        X, y = _make_data(n_exog=2)
        config = EstimatorConfig(
            multi_periodic_config=None,
            exog_config=[
                SplineConfig(n_knots=5, lags=[0]),
                LinearConfig(lags=[0]),
            ],
            solver_config=solver_config,
        )
        est = Estimator(config=config)
        est.fit(X, y)
        preds = est.predict(X)
        assert preds.shape == (len(X),)
        assert not np.any(np.isnan(preds))

    def test_linear_with_ar(self, solver_config):
        X, y = _make_data()
        config = EstimatorConfig(
            multi_periodic_config=None,
            exog_config=[LinearConfig(lags=[0])],
            ar_config=ArConfig(lags=[1]),
            solver_config=solver_config,
        )
        est = Estimator(config=config)
        est.fit(X, y)
        preds = est.predict(X)
        assert preds.shape == (len(X),)
        assert not np.any(np.isnan(preds))

    def test_linear_sample(self, solver_config):
        X, y = _make_data()
        config = EstimatorConfig(
            multi_periodic_config=None,
            exog_config=[LinearConfig(lags=[0])],
            ar_config=ArConfig(lags=[1]),
            solver_config=solver_config,
            random_state=np.random.RandomState(0),
        )
        est = Estimator(config=config)
        est.fit(X, y)
        samples = est.sample(X, n_samples=5)
        assert samples.shape == (5, len(X))
        assert not np.any(np.isnan(samples))

    def test_linear_coef_shape(self, solver_config):
        """Linear config should produce (1, num_lags) coefficient matrix."""
        X, y = _make_data()
        lags = [-1, 0, 1]
        config = EstimatorConfig(
            multi_periodic_config=None,
            exog_config=[LinearConfig(lags=lags)],
            solver_config=solver_config,
        )
        est = Estimator(config=config)
        est.fit(X, y)
        coef = est.decomposition_["values"]["exog_0_beta"]
        assert coef.shape == (len(lags),)
