import rasterio
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def main():
    print("All imports were successful!")
    print(f"rasterio version: {rasterio.__version__}")
    print(f"numpy version: {np.__version__}")
    print(f"pandas version: {pd.__version__}")
    print(f"matplotlib version: {plt.__version__}")

if __name__ == "__main__":
    main()
