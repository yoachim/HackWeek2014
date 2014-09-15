# Make a simple model galaxy for input to a fitting routine.

import numpy as np
import fsps
import matplotlib.pylab as plt

# load stellar pop model
sp = fsps.StellarPopulation(zmet=20,
                            sfh=1,
                            tau=1.0, #efolding time for SFH in Gyr
                            const=1.0, #mass frac formed in const SFH
                            sf_start=0.0, #start time of SFH in Gyr
                            tage=0.0, # output age
                            fburst=0.0, #fraction in instantaneous SF
                            tburst=0.0) #age of uni when burst occurs

lsun = 3.846e33
lam, lspecs = sp.get_spectrum(peraa=True)
spec = lspecs[-1]*lsun
mags = sp.get_mags()
plt.loglog(lam, spec)
bands = ['sdss_u', 
         'sdss_g',
         'sdss_r',
         'sdss_i',
         'sdss_z',
         'galex_fuv',
         'galex_nuv',
         '2mass_j',
         '2mass_h',
         '2mass_ks']
         
mags = sp.get_mags(bands=bands)
mag = mags[-1]


outfile = 'spec.dat'
f = open(outfile, 'w')
[f.write('{}\t{}\n'.format(l,s)) for l,s in zip(lam, spec)]
f.close()

outfile = 'mag.dat'
f = open(outfile, 'w')
[f.write('{}\t{}\n'.format(b,m)) for b,m in zip(bands, mag)]
f.close()
