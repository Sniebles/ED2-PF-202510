import csv

# Read CSV and turn it to a diccionary list
def read_csv(route):
    with open(route, newline='') as archive:
        reader = csv.DictReader(archive)
        return list(reader)
    
# Record diccionary list in the CSV    
def record_csv(route, data, fields):
    with open(route, mode="w", newline='') as archive:
        writer = csv.DictWriter(archive, fieldnames=fields)
        writer.writeheader()
        writer.writerows(data)
