"""Module for helping to deal with data from NCSD output files,
and export that data to different formats."""

from sub_modules.tunl_scraper import get_tunl_data_wrapper
from sub_modules.ncsd_output_reader import read_ncsd_output
from sub_modules.plotter import export_data

### INPUT SECTION

# path to file you want to take data from
ncsd_out_filename = "/Users/callum/Desktop/rough_python/ncsd_output_plotting/ncsd_output_files/B11_n3lo-NN3Nlnl-srg2.0_Nmax0-8.20_IT"

# if there are any Nmax values you want to skip, put them here,
# e.g. [0,2,4]. If you don't want to skip any, use []
skip_Nmax = [0]

# if you have 10 states and only want to plot 8, use this.
# if you don't want a max state, set max_state to some huge number, e.g. 1e100
max_state = 8

# output_type is the kind(s) of output you want, in a list
# possible output types: xmgrace, csv, matplotlib
# FYI, the output is saved in the plot_files directory.
output_types = ["xmgrace", "csv", "matplotlib"]

### END OF INPUT SECTION

def process_file(filename, out_types, skip_Nmax, max_state):
    """
    This takes an ncsd output filename,
    and exports the data to each format listed in out_types.
    
    skip_Nmax = list of Nmax values to skip

    max_state = maximum numbered state to consider
    """    
    # grab input from output of ncsd
    ncsd_data = read_ncsd_output(filename)
    Z = ncsd_data["Z"]
    N = ncsd_data["N"]
    
    # tries to get energy spectrum from TUNL, but doesn't break if it fails
    experimental_data = get_tunl_data_wrapper(ncsd_data["n_states"], Z, N)

    # combine ncsd_data and experimental_data
    data = ncsd_data
    data["expt_spectrum"] = experimental_data["expt_spectrum"]
    data["skip_Nmax"] = skip_Nmax
    data["max_state"] = max_state   

    # do something with the data, whether that's plotting or just making files
    for out_type in out_types:
        print("exporting as type "+out_type)
        export_data(data, out_type=out_type)

process_file(ncsd_out_filename, output_types, skip_Nmax, max_state)