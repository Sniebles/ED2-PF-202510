import csv

# Read CSV and turn it to a diccionary list
def read_csv(route: str):
    """
    Reads csv file and turns it into a dictionary list
    Parameters:
        route (str): Filepath
    """
    with open(route, newline='') as archive:
        reader = csv.DictReader(archive)
        return list(reader)
    
# Record diccionary list in the CSV    
def record_csv(route: str, data: list, fields: list):
    """
    Saves a dictionary list into a csv file
    Parameters:
        route (str): Filepath
        data (list): Dictionary list
        fields (list): Column names
    """
    with open(route, mode="w", newline='') as archive:
        writer = csv.DictWriter(archive, fieldnames=fields)
        writer.writeheader()
        writer.writerows(data)
