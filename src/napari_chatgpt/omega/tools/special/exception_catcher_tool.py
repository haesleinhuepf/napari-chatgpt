"""A tool for opening ome-zarr files in napari"""
import queue
import sys
import traceback

from arbol import aprint, asection

from napari_chatgpt.omega.tools.async_base_tool import AsyncBaseTool
from napari_chatgpt.utils.python.exception_description import \
    exception_description

# Create a queue to store exception information
exception_queue = queue.Queue()

# existing exception handler:
_original_exception_handler = sys.excepthook


# New handler:
def _uncaught_exception_handler(exctype, value, _traceback):
    # Store the exception information in the queue

    enqueue_exception(value)
    aprint(value)
    traceback.print_exc()

    # if _original_exception_handler != sys.__excepthook__:
    #     # Call the existing uncaught exception handler
    #     _original_exception_handler(exctype, value, traceback)


def enqueue_exception(exception):
    exception_queue.put(exception)


# Set the new uncaught exception handler
sys.excepthook = _uncaught_exception_handler


class ExceptionCatcherTool(AsyncBaseTool):
    """A tool that catches all uncaught exceptions and makes them available to Omega"""

    name = "ExceptionCatcherTool"
    description = (
        "This tool is usefull when the user is having problems with a widget ."
        "This tool returns information about the exception and traceback that happened."
        #"No input needed for this tool."

    )
    prompt: str = None

    def _run(self, query: str) -> str:
        """Use the tool."""

        with asection('ExceptionCatcherTool: List of caught exceptions:'):
            text = "Here is the list of exceptions that occurred:\n\n"

            while exception_queue.qsize() > 0:
                value = exception_queue.get_nowait()

                description = exception_description(value)

                text += description

                aprint(description)

            return text
