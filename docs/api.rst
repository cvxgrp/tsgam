.. Copyright (c) 2025 Alliance for Sustainable Energy, LLC and Nimish Telang
.. SPDX-License-Identifier: BSD-3-Clause

API Reference
=============

Import both estimators and their configuration classes from ``tsgam``.

.. code-block:: python

   from tsgam import Estimator, ForecastEstimator

Time-series decomposition
-------------------------

Use ``Estimator`` to fit a series and inspect its fitted components
through ``decomposition_``.

.. autoclass:: tsgam.Estimator
   :members: fit, predict, sample, score
   :undoc-members:

Direct multi-horizon forecasting
--------------------------------

Use ``ForecastEstimator`` to predict several horizons from each forecast
origin. Each output row corresponds to one origin, with a column per horizon.

.. autoclass:: tsgam.ForecastEstimator
   :members: fit, predict
   :undoc-members:

Configuration and utilities
---------------------------

.. automodule:: tsgam
   :members:
   :exclude-members: Estimator, ForecastEstimator
   :undoc-members:
   :show-inheritance:

