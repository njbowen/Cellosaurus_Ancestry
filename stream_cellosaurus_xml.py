import xml.etree.ElementTree as ET
import csv
import pandas as pd
import requests

def stream_and_extract_ancestries_from_url(xml_url, output_csv, output_excel):
    # Open the XML stream directly from the FTP URL
    print("Streaming XML file...")

    response = requests.get(xml_url, stream=True)
    
    # Check if the request is successful
    if response.status_code == 200:
        print("Streaming successful. Processing the XML data...")

        # Initialize iterparse to stream the XML content incrementally
        context = ET.iterparse(response.raw, events=("start", "end"))
        context = iter(context)
        _, root = next(context)  # Get the root element

        # A set to store all ancestry names dynamically
        all_ancestries = set()

        # First pass to collect all unique ancestry types
        for event, elem in context:
            if event == "end" and elem.tag == "cell-line":
                for child in elem:
                    if child.tag == "genome-ancestry":
                        population_list = child.find("population-list")
                        if population_list is not None:
                            for population in population_list:
                                all_ancestries.add(population.attrib.get('population-name'))
                root.clear()  # Clear element to free memory

        # Reset the iterparse for the second pass
        response = requests.get(xml_url, stream=True)
        context = ET.iterparse(response.raw, events=("start", "end"))
        context = iter(context)
        _, root = next(context)

        data = []

        # Second pass to extract the full data
        for event, elem in context:
            if event == "end" and elem.tag == "cell-line":
                row = {
                    "Cell Line Name": None,
                    "Disease Site": "Unknown",
                    "Sex": elem.attrib.get("sex", "Unknown"),
                    "Age": elem.attrib.get("age", "Unknown"),
                    "Derived From Site": "Unknown"
                }

                # Initialize ancestry percentages to 0
                ancestry_percentages = {ancestry: 0.0 for ancestry in all_ancestries}

                # Extract relevant data for the row
                for child in elem:
                    if child.tag == "name-list":
                        row["Cell Line Name"] = child.find("name").text if child.find("name") is not None else "Unknown"
                    
                    if child.tag == "genome-ancestry":
                        population_list = child.find("population-list")
                        if population_list is not None:
                            for population in population_list:
                                pop_name = population.attrib.get('population-name')
                                pop_percentage = float(population.attrib.get('population-percentage', 0))
                                if pop_name in ancestry_percentages:
                                    ancestry_percentages[pop_name] = pop_percentage
                    
                    if child.tag == "disease-list":
                        row["Disease Site"] = child.find("xref/label").text if child.find("xref/label") is not None else "Unknown"
                    
                    if child.tag == "derived-from-site-list":
                        row["Derived From Site"] = child.find("derived-from-site/site").text.strip() if child.find("derived-from-site/site") is not None else "Unknown"

                # Combine ancestry data with the row
                row.update(ancestry_percentages)
                
                # Check if all ancestry percentages are zero (filter out those entries)
                if any(percentage > 0 for percentage in ancestry_percentages.values()):
                    data.append(row)

                root.clear()  # Free memory after processing each element

        # Convert the data to a pandas DataFrame
        df = pd.DataFrame(data)

        # Write the filtered data to CSV
        df.to_csv(output_csv, index=False)

        # Sort the data by African ancestry in descending order
        if "African" in df.columns:
            df_sorted = df.sort_values(by="African", ascending=False)

            # Write the sorted data to an Excel file
            df_sorted.to_excel(output_excel, index=False)
        
        print(f"Processing complete. CSV saved to {output_csv}, Excel saved to {output_excel}.")
    
    else:
        print("Failed to stream the XML file. Please check the URL or your internet connection.")

# Call the function to stream the XML from URL and save results to CSV and Excel
stream_and_extract_ancestries_from_url(
    xml_url="https://ftp.expasy.org/databases/cellosaurus/cellosaurus.xml",
    output_csv="filtered_cell_lines_stream.csv",
    output_excel="filtered_cell_lines_stream_sorted_by_african_ancestry.xlsx"
)
