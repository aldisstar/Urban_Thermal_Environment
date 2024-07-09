#%%
# Liberys
import rasterio
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm

# Open file .tif
lcz_path = r'C:\Users\Aldis\Documents\Master Data Science\GitHub\Urban_Thermal_Environment\Data\Buenos Aires\LCZ_BsAs.tif'
lst_path = r'C:\Users\Aldis\Documents\Master Data Science\GitHub\Urban_Thermal_Environment\Data\Buenos Aires\LST_BuenosAires.tif'
ndvi_path = r'C:\Users\Aldis\Documents\Master Data Science\GitHub\Urban_Thermal_Environment\Data\Buenos Aires\NDVI_BuenosAires.tif'
#%%


# List of colors same as GGE
lcz_colors = [
    '8c0000', 'd10000', 'ff0000', 'bf4d00', 'ff6600',
    'ff9955', 'faee05', 'bcbcbc', 'ffccaa', '555555',
    '006a00', '00aa00', '648525', 'b9db79', '000000',
    'fbf7ae', '6a6aff'
]

with rasterio.open(lcz_path) as lcz_dataset:
    lcz = lcz_dataset.read(1)  

with rasterio.open(lst_path) as lst_dataset:
    lst = lst_dataset.read(1)  

with rasterio.open(ndvi_path) as ndvi_dataset:
    ndvi = ndvi_dataset.read(1)  

# Same dimensions?
if lcz.shape != lst.shape or lcz.shape != ndvi.shape:
    raise ValueError("Los archivos LCZ, LST y NDVI no tienen las mismas dimensiones")
#%%

# DataFrame and eliminate NaN
lcz_flat = lcz.flatten()
lst_flat = lst.flatten()
ndvi_flat = ndvi.flatten()

df = pd.DataFrame({
    'LCZ': lcz_flat,
    'LST': lst_flat,
    'NDVI': ndvi_flat
})

# Eliminate NaN and zone 0
df = df.dropna()
df = df[df['LCZ'] != 0]
df.head()
#%%

# Mean of LST and NDVI for the differents zones
mean_values_by_lcz = df.groupby('LCZ').agg({'LST': 'mean', 'NDVI': 'mean'}).reset_index()

# Show the DataFrame
print("Promedio de LST y NDVI por zona de LCZ:")
print(mean_values_by_lcz.head())
#%%

# Graph mean LST and NDVI for different climate zones
fig, ax1 = plt.subplots(figsize=(12, 6))

# Bar graph
bars = ax1.bar(mean_values_by_lcz['LCZ'], mean_values_by_lcz['LST'], 
               color=[f'#{lcz_colors[int(lcz)-1]}' for lcz in mean_values_by_lcz['LCZ']], label='Mean LST')

# Labels
for bar in bars:
    yval = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width() / 2, yval, f'{yval:.2f}', ha='center', va='bottom', fontsize=8)

# NDVI label
ax2 = ax1.twinx()
line, = ax2.plot(mean_values_by_lcz['LCZ'], mean_values_by_lcz['NDVI'], color='#BF83FF', marker='o', label='Mean NDVI')

for i, txt in enumerate(mean_values_by_lcz['NDVI']):
    ax2.annotate(f'{txt:.2f}', (mean_values_by_lcz['LCZ'][i], mean_values_by_lcz['NDVI'][i]), textcoords="offset points", xytext=(0,5), ha='center', fontsize=8)

# Title
ax1.set_title('Promedio de LST y NDVI por Zona de LCZ en Buenos Aires')
ax1.set_xlabel('Zona de LCZ')
ax1.set_ylabel('Promedio de LST (°C)')
ax2.set_ylabel('Promedio de NDVI')

# x ax
ax1.set_xticks(np.arange(1, 18, step=1))
ax1.set_xticklabels(np.arange(1, 18, step=1))

# Leyend
fig.legend(loc='upper right')

# Plot
plt.tight_layout()
plt.show()
# %%
