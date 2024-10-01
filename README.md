# Cellosaurus_Ancestry
"A Python script to stream, filter, and process the  Cellosaurus XML for cell line ancestry values"
# Cellosaurus XML Processor

This project contains a Python script to stream and process the XML file from the [Cellosaurus database](https://ftp.expasy.org/databases/cellosaurus/). The script filters cell lines with for ancestry data and outputs relevant data, including disease site, ancestry percentages, and other key information.


## Generated Files
 [output csv](https://github.com/njbowen/Cellosaurus_Ancestry/blob/main/output/filtered_cell_lines_stream.csv)
 
 [output xlsx](https://github.com/njbowen/Cellosaurus_Ancestry/blob/main/output/filtered_cell_lines_stream_sorted_by_african_ancestry.xlsx)


## Features
- **Streaming**: Efficiently process large XML files without loading them entirely into memory.
- **Filtering**: Filter cell lines based on presence of ancestry data. 
- **Output**: Generates CSV and Excel files with sorted data by African ancestry.

## Installation

Clone this repository and install the required dependencies:

```bash
git clone https://github.com/YOUR-USERNAME/cellosaurus-xml-processor.git
cd cellosaurus-xml-processor
pip install pandas openpyxl requests
