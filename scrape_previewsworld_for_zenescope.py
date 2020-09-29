from datetime import datetime as dt
import json
import requests

URL = "https://www.previewsworld.com/Search/SearchFull"

# JSON data for the search request, pulled this out of the web interface
# Only missing releaseStartDate and releaseEndDate, added later
json_data = { "mode":"A",
            "terms":"",
            "category":"",
            "batchType":"ALL",
            "batchYear":"2020",
            "batchMonth":None,
            "publisher":"ZENESCOPE ENTERTAINMENT INC",
            "creatorName1":"",
            "creatorName2":"",
            "availability":""
            }

resulting_items = [ ]

# Zenescope started in 2005 so only start in that year
for yr in range(2005, dt.now().year + 1):
    for mo in range(1, 12+1):

        # Update date range in the search query
        if mo == 12:
            json_data["releaseStartDate"] = f"{yr}-{mo}-01"
            json_data["releaseEndDate"] = f"{yr+1}-01-01"
        else:
            json_data["releaseStartDate"] = f"{yr}-{mo}-01"
            json_data["releaseEndDate"] = f"{yr}-{mo+1}-01"

        # Perform search
        res = requests.post(URL, data=json_data)
        j = res.json()
        
        # Check it returned everything
        if j["LimitReached"]:
            print(f"Limit reached for {yr}-{mo} - aborting to avoid missing items")
            break
        else:
            print(f"Acquired data for {yr}-{mo}")

        # Add to list
        got_count = 0
        for c in ["CatItems","UpCItems","OtherItems","Available","NewToOrder"]:
            for i in j[c]:
                got_count += 1
                resulting_items.append(i)
        print(f"Currently at {len(resulting_items)} items, got {got_count} for {yr}-{mo}")

# Save
print(f"Acquired {len(resulting_items)} total items")
with open("zenescope_data.json", "w") as fp:
    json.dump(resulting_items, fp)
print("Data saved")