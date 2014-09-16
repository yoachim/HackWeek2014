#!/usr/bin/env python
# encoding: utf-8
"""
Demonstration of parallelized ipython running python-fsps.

See `the iPython documentation for cluster computing
<http://ipython.org/ipython-doc/dev/parallel/parallel_multiengine.html>`_.

To run, in a terminal start up the cluster on the given number of local CPUs::

    ipcluster start -n 4

Then execute this script.
"""

from __future__ import division, print_function

from IPython.parallel import Client

from fsps import StellarPopulation

SP = None


def init_fsps():
    """Server side code to initialize FSPS (called once on each server)."""
    global SP
    SP = StellarPopulation(compute_vega_mags=False)


def compute_mags(args):
    """Server side code to compute magnitudes in a stellar population.

    ``args`` is a tuple of job_id, bands, and a dictionary of FSPS parameters.
    """
    # global SP
    job_id, bands, stellarpop = args
    for name, val in stellarpop.iteritems():
        SP.params[name] = val
    return job_id, SP.get_mags(bands=bands, tage=13.7)


def client_setup():
    """Client-side cluster setup code."""
    # Set up the interface to the ipcluster.
    c = Client()
    dview = c[:]  # a DirectView object

    # Here we send objects to each compute server. These make up the
    # environment for using python-fsps
    dview.push({"init_fsps": init_fsps,
                "compute_mags": compute_mags})
    # and execute import statements
    # NOTE: could also use synced imports, with dview.sync_imports():
    dview.execute("from fsps import StellarPopulation")
    # initialize a global StellarPopulation
    dview.execute("SP = None")
    dview.execute("init_fsps()")
    return dview


if __name__ == '__main__':
    dview = client_setup()

    # Compute an i-band mag for each metallicity in the Padova isochrones
    args = [(job_id, ['sdss_i'], {'zmet': zmet})
            for job_id, zmet in enumerate(range(1, 23))]
    results = dview.map(compute_mags, args)
    print("Without dust")
    for result in results:
        job_id, mags = result
        print("Job {0:d} mag_i={1:.2f}".format(job_id, mags[0]))

    # Now Compute an i-band mag for each metallicity in the Padova isochrones
    # with some dust
    args = [(job_id, ['sdss_i'], {'zmet': zmet, "dust2": 1.})
            for job_id, zmet in enumerate(range(1, 23))]
    results = dview.map(compute_mags, args)
    print("\nNow with dust")
    for result in results:
        job_id, mags = result
        print("Job {0:d} mag_i={1:.2f}".format(job_id, mags[0]))
