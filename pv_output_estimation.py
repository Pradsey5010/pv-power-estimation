import pandas as pd
import matplotlib
matplotlib.use('Agg')  
import matplotlib.pyplot as plt
from pvlib.pvsystem import pvwatts_dc
from pvlib.location import Location
from pvlib.iotools import get_pvgis_tmy

latitude = 33.4212
longitude = -111.9330

site = Location(latitude, longitude)

tmy_data, metadata = get_pvgis_tmy(latitude, longitude, outputformat='json')[0:2]

print("Step 3: Weather data downloaded")
print(tmy_data.head())

tmy_data.index = pd.date_range(start='2024-01-01 00:00:00', periods=len(tmy_data), freq='H')

poa_irradiance = tmy_data['ghi']       
temp_air = tmy_data['temp_air']       

print("Step 4: Extracted irradiance and temperature")
print(poa_irradiance.head())
print(temp_air.head())

pdc0 = 5000           
gamma_pdc = -0.003    

print("Step 5: PV system parameters set")

dc_power = pvwatts_dc(poa_irradiance, temp_air, pdc0, gamma_pdc)

print("Step 6: DC power calculated")
print(dc_power.head())

plt.figure(figsize=(12, 5))
dc_power.plot()
plt.title('Estimated DC Power Output (W) Over One Year at ASU PRL')
plt.xlabel('Time')
plt.ylabel('Power Output (W)')
plt.grid(True)
plt.tight_layout()

plt.savefig('dc_power_output.png')

print("Step 7: Plot saved as 'dc_power_output.png'")