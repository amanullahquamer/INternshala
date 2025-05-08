#!/bin/bash

# Download the file
curl -s "https://www.amfiindia.com/spages/NAVAll.txt" -o nav_all.txt

# Extract the header line to find indices
HEADER=$(grep -m1 'Scheme Name' nav_all.txt)
IFS=';' read -ra FIELDS <<< "$HEADER"

# Get indices of relevant fields
for i in "${!FIELDS[@]}"; do
    if [[ "${FIELDS[$i]}" == "Scheme Name" ]]; then
        SCHEME_INDEX=$i
    elif [[ "${FIELDS[$i]}" == "Net Asset Value" ]]; then
        NAV_INDEX=$i
    fi
done

# Output file
OUTFILE="scheme_nav.tsv"
echo -e "Scheme Name\tNet Asset Value" > "$OUTFILE"

# Extract data lines
grep -A 1000000 '^Scheme Code' nav_all.txt | tail -n +2 | while IFS=';' read -ra LINE; do
    echo -e "${LINE[$SCHEME_INDEX]}\t${LINE[$NAV_INDEX]}" >> "$OUTFILE"
done

echo "✅ Data saved to $OUTFILE"
