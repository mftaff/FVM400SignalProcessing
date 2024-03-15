# Raw is taken at 1kHz (10s*10_000samples)
# Snp is taken by the FVM directly at 4Hz? (check sample count in 7 seconds for reference)

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy import signal

from helpers import resample

# Read in raw data
raw_df = pd.read_csv('FVM400Raw-2024-03-12 18-26-41.csv')

# put raw into numpy
rawData = raw_df.to_numpy()

i_0 = 550
i_f = -1850
z_raw = rawData[i_0:i_f]
z_raw = resample(np.reshape(z_raw, z_raw.size), 1024, 4)
x_raw = np.linspace(0,len(z_raw)-1,len(z_raw))

# read in snapshot
# snp_df = pd.read_csv('FVM400Snp-2024-03-12 18-26-41.txt', sep="\r", header=None)
file = open("FVM400Snp-2024-03-12 18-26-41.txt", "r")
snp = file.read()
file.close()

snp = snp.replace("b'AS00","")
snp = snp.replace("\\rD\\x04'","")

# split .txt into array of strings: 'x,y,z'
snpAll = list(map(lambda x: x.split(','), snp.split("\\r")))

# separate x,y,z, and convert to int
snpData = [[],[],[]]
for s in snpAll:
    for i in range(3):
        snpData[i].append(int(s[i]))

snpData = np.array(snpData)

z_snp = -1*snpData[2]
z_snp = resample(np.reshape(z_snp, z_snp.size), 4, 4)
x_snp = np.linspace(0,len(3.5*z_raw)-1,len(z_snp))

# xcorr = np.correlate(np.reshape(3.5*z_raw, z_raw.size), np.reshape(z_snp, z_snp.size))

# # Sine sample with some noise and copy to y1 and y2 with a 1-second lag
# sr = 1024
# y = np.linspace(0, 2*np.pi, sr)
# y = np.tile(np.sin(y), 5)
# y += np.random.normal(0, 5, y.shape)
# y1 = y[sr:4*sr]
# y2 = y[:3*sr]
# n = len(y1)

# corr = signal.correlate(y2, y1, mode='same') / np.sqrt(signal.correlate(y1, y1, mode='same')[int(n/2)] * signal.correlate(y2, y2, mode='same')[int(n/2)])

# delay_arr = np.linspace(-0.5*n/sr, 0.5*n/sr, n)
# delay = delay_arr[np.argmax(corr)]
# print('y2 is ' + str(delay) + ' behind y1')

# plt.figure()
# plt.plot(delay_arr, corr)
# plt.title('Lag: ' + str(np.round(delay, 3)) + ' s')
# plt.xlabel('Lag')
# plt.ylabel('Correlation coeff')
# plt.show()

# plots
plt.scatter(x_raw, 3.5*z_raw, s=1, c='black', alpha=0.5)
plt.scatter(x_snp, z_snp, s=2, c='red', alpha=0.75)
plt.xlabel('ms')
plt.ylabel('3.5*mv or nT')
plt.title('Raw Bz (w/ LP10Hz) vs Processed Bz. 03-12-24. (Signals unsynced. Raw amplitude scalar: 3.5)')
plt.legend(["Raw signal [mv]", "Processed [nT]"], loc="upper right")
plt.show()