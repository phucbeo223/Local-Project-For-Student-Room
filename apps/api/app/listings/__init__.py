"""Listing package.

Import the router explicitly from ``app.listings.router``. Keeping package
initialization side-effect free lets schemas and repositories be reused by
offline evaluation without importing crawler-only dependencies.
"""
