Putting together some simple data that we could try to fit.

Looking at NGC 6155:
1) in SDSS
2) has SDSS central fiber spectra.  3" diameter fiber if SDSS, 2" if BOSS.
from astropy.io import fits
spec = fits.open('spec-0625-52145-0196.fits')

3) in 2MASS:  from here http://irsa.ipac.caltech.edu/applications/2MASS/IM/interactive.html
4) in GALEX:  
   notes on how to convert galex images to mags:
http://galexgi.gsfc.nasa.gov/docs/galex/FAQ/counts_background.html

