import time
import ipywidgets as widgets
from IPython.display import display, HTML
from threading import Thread

def run_with_progress_bar(code_block):
    """
    Runs a given code block with a progress bar that displays the percentage complete
    and the elapsed time.

    Parameters:
    code_block (function): The function containing the code block to be executed.
    
    Returns:
    The result of the executed code block.
    """
    
    # Create and display a full-width progress bar with percentage and time display
    progress_bar = widgets.IntProgress(
        min=0, max=100, description="0% Complete | Time: 0s",
        style={'description_width': 'initial'},
        layout=widgets.Layout(width='100%')  # Set width to fill the cell
    )
    
    # Use CSS to force full-width of the parent container
    display(HTML("<style>.widget-label { min-width: 0 !important; } </style>"))
    display(progress_bar)

    # Function to update progress bar based on estimated time
    def update_progress_bar(estimated_time, start_time):
        sleep_interval = estimated_time / 100
        for i in range(1, 101):
            time.sleep(sleep_interval)
            elapsed_time = int(time.time() - start_time)  # Calculate elapsed time in seconds
            progress_bar.value = i
            progress_bar.description = f"{i}% Complete | Time: {elapsed_time}s"

    # Start timing the process
    start_time = time.time()
    
    # Run the provided code block and capture its return value
    result = code_block()
    
    # Calculate the elapsed time for updating
    end_time = time.time()
    estimated_time = end_time - start_time
    
    # Start the progress bar update in a separate thread with the calculated time
    progress_thread = Thread(target=update_progress_bar, args=(estimated_time, start_time))
    progress_thread.start()
    
    # Wait for the progress bar thread to complete
    progress_thread.join()
    
    # Display a bold, green-colored completion message
    display(HTML('<h3 style="color: green; font-weight: bold;">✔️ Process complete!</h3>'))
    
    return result
