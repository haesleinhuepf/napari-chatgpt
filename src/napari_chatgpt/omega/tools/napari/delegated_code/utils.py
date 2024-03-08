# Function that checks if the packages stardist or napari-stardist are installed:
from arbol import aprint


def check_stardist_installed() -> bool:
    try:
        import stardist
        return True
    except ImportError:
        return False

# Function that checks if the packages cellpose or cellpose-napari are installed:
def check_cellpose_installed() -> bool:
    try:
        import cellpose
        return True
    except ImportError:
        return False


def get_list_of_algorithms() -> str:

    algos = []
    if check_cellpose_installed():
        aprint("Cellpose is installed!")
        algos.append('cellpose')
    if check_stardist_installed():
        aprint("Stardist is installed!")
        algos.append('stardist')

    algos.append('classic')
    return algos

def get_description_of_algorithms() -> str:

    description = ''

    algos = get_list_of_algorithms()

    description += "For example, you can request to: "

    for algo in algos:
        if 'cellpose' in algo:
            description += "'segment cell nuclei in selected layer with StarDist', "

        elif 'stardist' in algo:
            description += "'segment cell's cytoplams in selected layer with Cellpose', "

        elif 'classic' in algo:
            description += "'segment cell nuclei in selected 3D image with Classic', "

    # remove last comma:
    description = description[:-2]

    description += ". Choose: "

    for algo in algos:
        if 'cellpose' in algo:
            description += "cellpose for the cell cytoplasm/membrane outline, "

        elif 'stardist' in algo:
            description += "stardist for segmenting nuclei, "

        elif 'classic' in algo:
            description += "classic for 3D images, "

    # remove last comma:
    description = description[:-2]

    description += ". "

    return description