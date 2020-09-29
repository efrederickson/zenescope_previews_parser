import datetime as dt
import json
import re

# I don't actually know if this is accurate
# Just assuming based on how I've seen the previews website react
cat_to_type = {
    "1": "Single Issue",
    "3": "Graphic Novel",
}

# category to type str
def c2t(x):
    return x in cat_to_type and cat_to_type[x] or "Other"

# Read data
loaded = [ ]
with open("zenescope_data.json", "r") as fp:
    loaded = json.load(fp)

# Parse date without raising errors
def tryparse_date(s):
    try:
        return dt.datetime.strptime(s, '%b %d, %Y')
    except:
        return None

# Sort items by release date
print(f"Loaded {len(loaded)} items")
ls = sorted(loaded, key=lambda i: tryparse_date(i["ShipDate"]) or dt.datetime.strptime("2199-01-01", "%Y-%m-%d"))

# Used to strip out diamond codes, like AUG141842
p = re.compile(r"\(\w+\d+\)")

def normalize(t: str) -> str:
    # This doesn't really work exactly how it's supposed to, 
    # but I got the data "good enough" and added it to a 
    # different tracker, so I no longer care. 
    title_normalized: str = t.replace("(RES)", "").replace("(MR)","").replace("(O/A)","").strip()
    title_normalized = title_normalized.replace("(BOOK MARKET ED)", "").replace("(DIRECT MARKET ED)","").strip()
    title_normalized = p.sub("", title_normalized).strip()

    # Attempt to strip covers from single issues (CVR A, CVR B, etc)
    if title_normalized.startswith("("):
        title_normalized = title_normalized[title_normalized.index(")")+2:]
    try:
        title_normalized = title_normalized[0:title_normalized.index("CVR")].strip()
    except ValueError:
        pass
    for e in [ " A", " B", " C", " D" ]:
        if title_normalized.endswith(e):
            title_normalized = title_normalized[0:-2]

    # Remove excess whitespace
    title_normalized = title_normalized.strip()
    return title_normalized

# Write the data to csv outfile to import into Excel
written = []
with open("normalized.csv", "w") as fp2:
    for item in ls:
        title = normalize(item["Title"])
        if title in written: # dedupe
            continue
        dp = tryparse_date(item["ShipDate"])
        if dp is not None:
            d = dp.strftime("%Y-%m-%d")
        diamond_code = item["DiamdNo"]
        cost = item["SRP"]
        cat = c2t(item["Cat"])
        print(f"{d or 'TBD'},{title},{diamond_code},{cost},{cat}", file=fp2)
        written.append(title)

print(f"Wrote {len(written)} items")
