from napari_chatgpt.omega.tools.napari_base_tool import NapariBaseTool
from contextlib import redirect_stdout
from io import StringIO

from napari import Viewer


_napari_assistant_functions_prompt = """
Task:
Given a plain text request, you either search for functions in the napari assistant or you execute a function if you know which one.
The napari assistant has a lot of functions available, sorted into categories.
If a function search leads to only a single function, or if one function is explicitly mentioned, you can directly execute it using competently written python code that executes the function in an already instantiated napari viewer instance.
The napari viewer instance is immediately available by using the variable: 'viewer'. 
Therefore, DO NOT use 'napari.Viewer()' or 'with napari.gui_qt():' in your code. 
DO NOT CREATE A NEW INSTANCE OF A NAPARI VIEWER, use the one provided in the variable: 'viewer'.
Make sure the calls to the viewer are correct.

{generic_codegen_instructions}

Executing napari assistant functions works like this:
import napari_assistant as na
from magicgui import magicgui
function = na._categories.find_function('Filtering / noise removal>Butterworth (scikit-image, nsbatwm)')
viewer.window.add_dock_widget(magicgui(function))

Searching for functions works like this:
from napari_chatgpt.omega.tools.napari_assistant_tool import list_functions
list_functions(query:str)

Request: 
{input}

Answer in markdown:
"""


class NapariAssistantFunctionSearchTool(NapariBaseTool):
    name = "NapariAssistantFunctionSearchTool"
    description = "Forward text to this tool in case you need information about one or more functions managed by the napari assistant."
    prompt = _napari_assistant_functions_prompt


    def _run_code(self, request: str, code: str, viewer: Viewer) -> str:
        code = super()._prepare_code(code)

        # Redirect output:
        f = StringIO()
        with redirect_stdout(f):
            # Running code:
            exec(code, globals(), {**locals(), 'viewer': viewer})

        captured_output = f.getvalue()

        return f"Success: request '{request}' satisfied:\n{captured_output}"


def list_functions(query:str):
    from napari_chatgpt.utils.napari_assistant import search_functions
    result = search_functions(query=query)

    print(result)

    return f"These napari assistant functions were found:\n* {result}"
