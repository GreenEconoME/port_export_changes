# Define functions to handle the row and cell formatting in the changed report

def highlight_rows(row):
    """
    Row-level styling:
      - If RowStatus == 'NEW', entire row is lightgreen
      - If RowStatus == 'DELETED', entire row is salmon
      - Otherwise, no row-level background
    Returns a list of CSS strings for each cell in the row.
    """
    status = row["RowStatus"]
    if status == "NEW":
        return ["background-color: lightgreen;"] * len(row)
    elif status == "DELETED":
        return ["background-color: salmon;"] * len(row)
    else:
        return [""] * len(row)


def highlight_changes(val):
    """
    Cell-level styling:
    - If cell has ' → ', highlight it in yellow
    """
    if " → " in str(val):
        return "background-color: yellow;"
    else:
        return ""
    
def display_progress_list(sheet_status):
    """
    Returns formatted text to display sheet processing progress with color coding.
    - 🔴 Red = Pending
    - 🟠 Orange = Processing
    - 🟢 Green = Completed
    """
    status_colors = {
        "Pending": "🔴",
        "Processing": "🟠",
        "Completed": "🟢"
    }

    progress_text = "### Processing Status:\n"
    for sheet, status in sheet_status.items():
        progress_text += f"{status_colors[status]} **{sheet}**  \n"

    return progress_text