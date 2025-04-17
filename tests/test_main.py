import pytest
import pandas as pd
from unittest.mock import patch
from src.utils import toon_customers_basedOnAge,toon_customers_basedOnProvince



#Unit tests to verify function output

#Test toon customers based on age
def test_toon_customers_basedOnAge():
    # Sample test data
  
    data = pd.read_csv('../sample_data_set.csv', delimiter=';')

    # Expected output
    expected_counts = (1, 2, 1, 2)  # <25: 1, 25-35: 2, 35-45: 1, >45: 2

    # Patch plt.show to skip visualization during testing
    with patch("matplotlib.pyplot.show"):
        counts = toon_customers_basedOnAge(data)

    # Assert that the counts match the expected output
    assert counts == expected_counts

#Test toon customers based on province
def test_toon_customers_basedOnProvince():
    # Sample test data
  
    data = pd.read_csv('../sample_data_set.csv', delimiter=';')
    
    expected_counts = pd.Series({'GELDERLAND': 1, 'NOORD-BRABANT': 1,'NOORD-HOLLAND': 1,'ZUID-HOLLAND': 3})
    expected_counts.index.name = 'province'

    with patch("matplotlib.pyplot.show"):
        province_counts = toon_customers_basedOnProvince(data)


    # Sort indices before comparison

    pd.testing.assert_series_equal(province_counts.sort_index(), expected_counts.sort_index())


