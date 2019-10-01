# ncsd_output_plotting

Python modules to make it easier to plot the output from `ncsd-it.exe`.

You give it an output file, a couple parameters (e.g. do you want to exclude Nmax=0?), and an output format (xmgrace by default) and it creates a plot / plot file.

## Getting Started

`git clone` this, or if you're on Cedar you can find a clone in `exch`. `git pull origin master` to get the latest version.

However, you may not be able to run this on Cedar, I had issues downloading Java there, which is needed.

Then you'll need to open `ncsd_output_plotter.py` and tell it where to find your ncsd output file.

You'll also enter those couple parameters here. Run `ncsd_output_plotter.py` when you're finished!

### Prerequisites

1. Python (3.7.4 ideally, other versions may work)
2. NCSD output files
3. If you want to get data from TUNL:
  - an internet connection
  - a Java SDK
    - if you type `java` in the terminal and get sensible output, you probably have it
  - A few python libraries:
    - `tabula`, install with `pip install --user tabula-py`
    - `requests`, install with `pip install --user requests`
    - `lxml`, install with `pip install --user lxml`
    - `matplotlib`, install with `pip install --user matplotlib`

