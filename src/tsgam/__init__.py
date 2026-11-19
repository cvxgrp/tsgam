# Copyright (c) 2025 Alliance for Sustainable Energy, LLC and Nimish Telang
# SPDX-License-Identifier: BSD-3-Clause

from importlib.metadata import PackageNotFoundError, version

from ._sklearn import make_supported_scorer

from ._estimator import (
    PERIOD_DAILY_YEARLY,
    PERIOD_HOURLY_DAILY,
    PERIOD_HOURLY_WEEKLY,
    PERIOD_HOURLY_YEARLY,
    PERIOD_MONTHLY_YEARLY,
    PERIOD_QUARTERLY_YEARLY,
    PERIOD_WEEKLY_YEARLY,
    PERIOD_YEARLY_YEARLY,
    SolverOptionValue,
    TrendType,
    ArConfig,
    Estimator,
    EstimatorConfig,
    LinearConfig,
    MultiPeriodicConfig,
    OutlierConfig,
    SolverConfig,
    SplineConfig,
    TrendConfig,
    get_recommended_periods,
)
from ._forecast import (
    ForecastArConfig,
    ForecastConfig,
    ForecastCouplingConfig,
    ForecastEstimator,
)
from ._forecast_plotting import (
    forecast_to_long_dataframe,
    plot_forecast_horizon,
    plot_forecast_origin,
)

try:
    __version__ = version("tsgam")
except PackageNotFoundError:
    __version__ = "0.1.0"

__all__ = [
    "make_supported_scorer",
    "__version__",
    "Estimator",
    "ForecastEstimator",
    "EstimatorConfig",
    "ForecastConfig",
    "ForecastArConfig",
    "ForecastCouplingConfig",
    "forecast_to_long_dataframe",
    "plot_forecast_origin",
    "plot_forecast_horizon",
    "MultiPeriodicConfig",
    "SplineConfig",
    "LinearConfig",
    "ArConfig",
    "TrendConfig",
    "OutlierConfig",
    "SolverConfig",
    "SolverOptionValue",
    "TrendType",
    "get_recommended_periods",
    "PERIOD_HOURLY_DAILY",
    "PERIOD_HOURLY_WEEKLY",
    "PERIOD_HOURLY_YEARLY",
    "PERIOD_DAILY_YEARLY",
    "PERIOD_WEEKLY_YEARLY",
    "PERIOD_MONTHLY_YEARLY",
    "PERIOD_QUARTERLY_YEARLY",
    "PERIOD_YEARLY_YEARLY",
]
