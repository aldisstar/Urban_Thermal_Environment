#%%
# Libery
import rasterio
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Path .tif
ndvi_path = r'C:\Users\Aldis\Documents\Master Data Science\GitHub\Urban_Thermal_Environment\Data\Buenos Aires\NDVI_BuenosAires.tif'
lst_path = r'C:\Users\Aldis\Documents\Master Data Science\GitHub\Urban_Thermal_Environment\Data\Buenos Aires\LST_BuenosAires.tif'

# Open and read .tif
with rasterio.open(ndvi_path) as ndvi_dataset:
    ndvi = ndvi_dataset.read(1)  # Leer la primera banda

with rasterio.open(lst_path) as lst_dataset:
    lst = lst_dataset.read(1)  # Leer la primera banda

# Same dimension?
if ndvi.shape != lst.shape:
    raise ValueError("Los archivos NDVI y LST no tienen las mismas dimensiones")

# DataFrame and remuve NaN
ndvi_flat = ndvi.flatten()
lst_flat = lst.flatten()

df = pd.DataFrame({
    'NDVI': ndvi_flat,
    'LST': lst_flat
})

# NaN = 0
df = df.fillna(0)

# Show DataFrame
print("Primeras filas del DataFrame:")
print(df.head())

# Correlation NDVI and LST
correlation = df['NDVI'].corr(df['LST'])
print(f"\nCorrelación entre NDVI y LST: {correlation}")

# Plot
fig, ax = plt.subplots(1, 2, figsize=(12, 6))
ax[0].imshow(ndvi, cmap='viridis')
ax[0].set_title('NDVI')
ax[1].imshow(lst, cmap='plasma')
ax[1].set_title('LST')
plt.show()
# %%

