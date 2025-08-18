import os
import json
from iracingdataapi.client import irDataClient

# Login via GitHub Secrets
username = os.environ["IR_USERNAME"]
password = os.environ["IR_PASSWORD"]

idc = irDataClient(username, password)

# Læs kørere fra drivers.json
with open("drivers.json", "r") as f:
    drivers = json.load(f)

def parse_sr(val):
    if not val:
        return None, None
    val = str(val)
    lic_map = {1: "R", 2: "D", 3: "C", 4: "B", 5: "A", 6: "Pro"}
    license_class = lic_map.get(int(val[0]), "?")
    sr = round(int(val[1:]) / 100, 2)
    return license_class, sr

updated_drivers = []

for d in drivers:
    cid = d["cust_id"]
    name = d.get("name", "")
    try:
        member = idc.member(cust_id=cid)
        name = member.get("display_name", name)

        entry = {"cust_id": cid, "name": name}

        for cat_id, key in [(6, "formula"), (5, "sportscar")]:
            ir_data = idc.member_chart_data(cust_id=cid, category_id=cat_id, chart_type=1)
            sr_data = idc.member_chart_data(cust_id=cid, category_id=cat_id, chart_type=3)

            ir = ir_data["data"][-1]["value"] if ir_data["data"] else None
            sr_val = sr_data["data"][-1]["value"] if sr_data["data"] else None
            lic, sr = parse_sr(sr_val)

            entry[key] = {"irating": ir, "sr": sr, "license": lic}

        updated_drivers.append(entry)
        print(f"Opdateret {name} ({cid})")

    except Exception as e:
        print(f"Fejl ved {cid}: {e}")

# Gem opdateret JSON
with open("drivers.json", "w") as f:
    json.dump(updated_drivers, f, indent=2, ensure_ascii=False)
