"""Module for helping to deal with data from NCSD output files,
and export that data to different formats."""

from sub_modules import scraper
from sub_modules import ncsd_output_reader
from sub_modules import plotter
from os.path import realpath, dirname, join

### INPUT SECTION

# relative path to file you want to take data from
this_dir = dirname(__file__)
rel_paths = [
    "ncsd_output_files/Li9_n3lo-NN3Nlnl-srg2.0_Nmax0-6.20",
    "ncsd_output_files/Li9_n3lo-NN3Nlnl-srg2.0_Nmax8.20"]
real_paths = [realpath(join(this_dir, rel_path)) for rel_path in rel_paths]

# if there are any Nmax values you want to skip, put them here,
# e.g. [0,2,4]. If you don't want to skip any, use []
skip_Nmax = [0]

# if you have 10 states and only want to plot 8, use this.
# if you don't want a max state, set max_state to some huge number, e.g. 1e100
max_state = 6

# output_type is the kind(s) of output you want, in a list
# possible output types: xmgrace, csv, matplotlib
# FYI, the output is saved in the plot_files directory.
output_types = ["xmgrace", "matplotlib"]

### END OF INPUT SECTION

def process_file(filenames, out_types, skip_Nmax, max_state):
    """
    This takes ncsd output filenames,
    and exports the data to each format listed in out_types.
    
    skip_Nmax = list of Nmax values to skip

    max_state = maximum numbered state to consider
    """    
    # grab input from output of ncsd
    ncsd_data = ncsd_output_reader.read_all_ncsd_output(real_paths)
    # tries to get energy spectrum from online, but doesn't break if it fails
    experimental_data = scraper.get_online_data_wrapper(ncsd_data)
    
    # combine ncsd_data and experimental_data
    data = ncsd_data
    data["expt_spectrum"] = experimental_data["expt_spectrum"]
    data["skip_Nmax"] = skip_Nmax
    data["max_state"] = max_state   

    # do something with the data, whether that's plotting or just making files
    for out_type in out_types:
        print("exporting as type "+out_type)
        plotter.export_data(data, out_type=out_type)

process_file(real_paths, output_types, skip_Nmax, max_state)
