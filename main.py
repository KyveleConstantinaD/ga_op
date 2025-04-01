import tkinter as tk
from tkinter import font
import run

# Function to handle the selection and run the external module's function
def submit_selection(var_runSet, var_initPop, var_parentSelection, root):
    runSet = var_runSet.get()
    initPop = var_initPop.get()
    parentSelection = var_parentSelection.get()

    # Close the window but continue running the program
    root.destroy()

    # Execute the run function from the run module with runSet as the parameter
    run.run(runSet, initPop, parentSelection)
    print(f"Run Set: {runSet}, Init Pop: {initPop}, Parent Selection: {parentSelection}")

# Function to close the window
def close_window(root):
    root.destroy()

# Main function to create the window
def create_gui():
    root = tk.Tk()
    root.title("GA for OP")
    root.geometry("500x350")  # Set the window size to 500x350
    root.configure(bg='white')

    # Create custom fonts
    title_font = font.Font(family="Helvetica", size=12, weight="bold")
    button_font = font.Font(family="Helvetica", size=10, weight="bold")

    # Variables to store selections
    var_runSet = tk.IntVar(value=1)
    var_initPop = tk.IntVar(value=1)
    var_parentSelection = tk.IntVar(value=1)

    # Section 1: Set Selection
    section1_frame = tk.Frame(root, bg="white")
    section1_frame.grid(row=0, column=0, sticky="w", padx=20, pady=10)
    tk.Label(section1_frame, text="Set Selection:", font=title_font, fg="dark red", bg="white").grid(row=0, column=0, sticky="w")
    radio1 = tk.Radiobutton(section1_frame, text="Tsiligirides 1", variable=var_runSet, value=1, bg="white", fg="blue")
    radio2 = tk.Radiobutton(section1_frame, text="Tsiligirides 2", variable=var_runSet, value=2, bg="white", fg="blue")
    radio3 = tk.Radiobutton(section1_frame, text="Set 130", variable=var_runSet, value=130, bg="white", fg="blue")
    radio1.grid(row=1, column=0, sticky="w")
    radio2.grid(row=2, column=0, sticky="w")
    radio3.grid(row=3, column=0, sticky="w")

    # Section 2: Initial Population Generation
    section2_frame = tk.Frame(root, bg="white")
    section2_frame.grid(row=1, column=0, sticky="w", padx=20, pady=10)
    tk.Label(section2_frame, text="Initial Population Generation:", font=title_font, fg="dark red", bg="white").grid(row=0, column=0, sticky="w")
    radio4 = tk.Radiobutton(section2_frame, text="Heuristic (Method 1)", variable=var_initPop, value=1, bg="white", fg="blue")
    radio5 = tk.Radiobutton(section2_frame, text="Random (Method 2)", variable=var_initPop, value=2, bg="white", fg="blue")
    radio4.grid(row=1, column=0, sticky="w")
    radio5.grid(row=2, column=0, sticky="w")

    # Section 3: Parent Selection
    section3_frame = tk.Frame(root, bg="white")
    section3_frame.grid(row=2, column=0, sticky="w", padx=20, pady=10)
    tk.Label(section3_frame, text="Parent Selection:", font=title_font, fg="dark red", bg="white").grid(row=0, column=0, sticky="w")
    radio6 = tk.Radiobutton(section3_frame, text="Tournament Selection (Method a)", variable=var_parentSelection, value=1, bg="white", fg="blue")
    radio7 = tk.Radiobutton(section3_frame, text="Quality Score (Method b)", variable=var_parentSelection, value=2, bg="white", fg="blue")
    radio6.grid(row=1, column=0, sticky="w")
    radio7.grid(row=2, column=0, sticky="w")

    # Buttons on the right side (Submit and Close)
    button_frame = tk.Frame(root, bg="white")
    button_frame.grid(row=0, column=1, rowspan=3, padx=20, pady=20)

    # Submit button
    submit_button = tk.Button(button_frame, text="Submit", font=button_font, bg="dark red", fg="white",
                              command=lambda: submit_selection(var_runSet, var_initPop, var_parentSelection, root))
    submit_button.pack(pady=10)

    # Close button to close the window
    close_button = tk.Button(button_frame, text="Close", font=button_font, bg="dark red", fg="white",
                             command=lambda: close_window(root))
    close_button.pack(pady=10)

    root.mainloop()

# Main entry point
def main():
    create_gui()

# Call main if this script is executed directly
if __name__ == "__main__":
    main()
