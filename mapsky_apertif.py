# MapSky APERTIF: Plot ra/dec positions on northern sky map
# Example usage: >> python mapsky_apertif.py
# V.A. Moss (vmoss.astro@gmail.com)
# Background image: NHI_ZEA_mir.fits from EBHIS
# Reference: EBHIS spectra and HI column density maps (Winkel+, 2016)
# From: ftp://cdsarc.u-strasbg.fr/pub/cats/J/A%2BA/585/A41/nhi/NHI_ZEA.fit

__author__ = "V.A. Moss"
__date__ = "$29-mar-2018 12:00:00$"
__version__ = "0.1"

import os
import sys
import matplotlib
from pylab import *
from matplotlib import rc
rc('text', usetex=True)
rc('font',**{'family':'serif','serif':['serif'],'size':14})
import aplpy
from astropy.io import ascii

def ra2dec(ra):
    if not ra:
        return None
      
    r = ra.split(':')
    if len(r) == 2:
        r.append(0.0)
    return (float(r[0]) + float(r[1])/60.0 + float(r[2])/3600.0)*15

def dec2dec(dec):
    if not dec:
        return None
    d = dec.split(':')
    if len(d) == 2:
        d.append(0.0)
    if d[0].startswith('-') or float(d[0]) < 0:
        return float(d[0]) - float(d[1])/60.0 - float(d[2])/3600.0
    else:
        return float(d[0]) + float(d[1])/60.0 + float(d[2])/3600.0


# Read in the background sky image
f = aplpy.FITSFigure('NHI_ZEA_mir.fits',convention='calabretta')
f.show_colorscale(cmap='Greys',stretch='arcsinh')
f.hide_xaxis_label()
f.hide_xtick_labels()
f.hide_yaxis_label()
f.hide_ytick_labels()
f.set_frame_linewidth(0)
f.recenter(0,90,110)
f.add_label(0,230,'{\\bf APERTIF: Current RFI Status}')

# Plot LST lines on the plot (RA)
for i in range(0,360,15):
    poscloud = np.array([[i,i],[-5,90]])
    f.show_lines([poscloud],linewidth=1,color='k',alpha=0.3)#color=cm.Spectral(i/360.))
    f.add_label(i,-18,'%02d:00' % (i/15),color='k',horizontalalignment='center',verticalalignment='center',fontsize=12)

# Read in the RFI pointing positions
dd = ascii.read('APERTIF Observation Record - happili.csv')

# Plot each as a marker
for i in range(0,len(dd)):
    name = dd['Data'][i]

    # only RFI
    if 'RFI' not in name:
        continue

    rat = ra2dec(dd['RA'][i])
    dect = dec2dec(dd['Dec'][i])

    f.show_markers(rat,dect,marker='o',facecolor=cm.Spectral(float(i)/len(dd)),edgecolor='k',s=50,alpha=0.7)#,label=name)

# Save the figure
savefig('APERTIF_RFISkyPointings.jpg',bbox_inches='tight',dpi=200)



