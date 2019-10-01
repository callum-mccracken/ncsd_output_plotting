"""
Contains functions for grabbing data from TUNL.

- we download the necessary pdf from TUNL

- then look through the PDF and pick out important values using tabula

- we do all of this within a try statement so if people don't want to bother
    with the bugginess of this code, they don't have to
"""

from .ncsd_output_reader import element_name
from os import mkdir
from os.path import join, realpath, split, exists

# I've done something gross here by putting some imports inside functions
# rather than up here... The reason for that is that some packages,
# especially tabula, are not always going to be installed.
# This way, if the user wants to install them they can,
# but if not, the code in this package still works.

# a place to save all the pdfs we download, we'll overwrite for new files
this_dir = split(realpath(__file__))[0]
save_dir = realpath(join(this_dir, '..'))
if not exists(save_dir):
    mkdir(save_dir)
pdf_save_path = join(save_dir, 'TUNL.pdf')


def parse_tunl_pdf(pdf_url):
    """returns Ex column of pdf from TUNL, without uncertainties"""
    import urllib.request
    import requests
    from lxml import html
    import tabula
    print("\nThe feature to grab data from TUNL is still very experimental,\n"+\
        "please ensure you end up with the right values!\n"+\
        "Also be sure to manually adjust J and T values.\n\n")
    print("downloading PDF")
    # saves url file to a local destination
    urllib.request.urlretrieve(pdf_url, pdf_save_path)
    print("pdf saved as "+pdf_save_path)
    print("reading into dataframe")
    # read in the PDF file that contains data
    df = tabula.read_pdf(pdf_save_path, pages="all")
    # I tried a couple things but wasn't sure how to get the J or T values...
    # get the relevent column
    try:
        Ex_strings = df["Ex (MeV± keV)"]
    except KeyError:
        Ex_strings = df["E x"]
    Ex_strings.dropna(inplace = True)  # drop all NaN entries
    
    Exs = []  # to store the Ex values
    for Ex_string in list(Ex_strings):
        # there are so many things that could go wrong with this...
        # but let's try anyway!
        
        # first off, sometimes we just get random integers.
        # let's ignore those by ensuring all lines have a decimal point
        # except for sometimes the first value is zero and I assume we want that
        if "." not in Ex_string and Ex_string != "0":
            continue
        
        try:
            Ex = float(Ex_string)
            Exs.append(Ex)
            continue
        except ValueError:
            pass
        # if we're still here, 
        # we could not convert string to float for some reason...

        # there are sometimes artifacts in the data from super/subscripts
        # thankfully those always seem to come with + or - signs, e.g. 1+
        # and they're just 1 character as far as I've seen
        for abomination in ["-", "+"]:
            while abomination in Ex_string:
                index = Ex_string.index(abomination)
                # I assume none of these + or - occur right at the start
                before = Ex_string[:index-1]  # also ignore the char before
                after = Ex_string[index+1:]
                Ex_string = before + after
        try:
            Ex = float(Ex_string)
            Exs.append(Ex)
            continue
        except ValueError:
            pass    

        # remove uncertainties from the string
        if "±" in Ex_string:
            index = Ex_string.index("±")
            before = Ex_string[:index]
            after = Ex_string[index+1:]
            Ex_string = before  # just take the stuff before the ±
        try:
            Ex = float(Ex_string)
            Exs.append(Ex)
            continue
        except ValueError:
            pass

        # if it STILL doesn't work, just remove all nonsensical characters
        # and hope that works
        new_string = ""
        for char in Ex_string:
            if (not char.isdigit()) and (char != "."):
                pass
            else:
                new_string += char
        if new_string != "":
            Ex = float(new_string)
            Exs.append(Ex)
    return Exs

def get_tunl_data_wrapper(n_states, Z, N):
    """This tries to get tunl data,
    but doesn't break everything if it fails.
    Instead, filler data is returned.
    """
    try:
        return get_tunl_data(n_states, Z, N)
    except Exception as e:
        print("EXCEPTION RAISED WHILE TRYING TO GET DATA FROM TUNL")
        print("(this is tunl_scraper.py, in get_tunl_data_wrapper() )")
        print(e)
        print("Returning filler data instead")
        filler_data = {
            "expt_spectrum": {
                "Expt": {
                    n+1: [1,1,1, 0.0]
                    for n in range(n_states)
                }       
            }       
        }
        return filler_data

def get_tunl_data(n_states, Z, N):
    """Function to get data from TUNL. Currently only gets energies,
    but if you have any ideas about how to get J, T, parity let me know!"""
    import urllib.request
    import requests
    from lxml import html
    import tabula
    
    A = Z + N
    element = element_name(Z)
    print("getting TUNL data for "+element+str(A))
    # get page for elements with our A value
    page = requests.get(
        "http://www.tunl.duke.edu/nucldata/chain/{A}.shtml".format(A=A))
    tree = html.fromstring(page.content)

    # find all elements with the right element name, e.g. "Li" or "B"
    elements = tree.xpath("//*[text()='{element}']".format(element=element))

    # find all possible pdf files associated with this element
    possible_files = []
    for element in elements:
        link = element.attrib.get('href')
        if ".pdf" in link:
            possible_files.append(link)
    
    # check that we only got one
    if len(possible_files) != 1:
        print("Possible PDF files found on this page:")
        print(possible_files)
        raise ValueError(
            "Wrong number of files found on TUNL: "+str(len(possible_files)))
    
    # then take that file, open it, and look inside for values
    pdf_url = possible_files[0]
    Ex_values = parse_tunl_pdf(pdf_url)  # list of floats
    
    # format the data for use later
    data = {
        "expt_spectrum": {
            "Expt": {
                n+1: [1,1,1, Ex_values[n]]
                for n in range(n_states) # assuming we want the first few
            }       
        }       
    }
    return data

if __name__ == "__main__":
    print(get_tunl_data_wrapper(10, Z=5, N=6))
