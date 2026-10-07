#!/usr/bin/env python3
"""
Build-time data for the website, from vigilo-conf:

- _generated/data/instances.json: every production instance of
  vigilo-conf/main/citylist.json, completed with what its API says
  (get_scope.php) when it answers
- _generated/data/categories.json: vigilo-conf/main/categorielist.json
- _generated/content/villes/<slug>/_index.fr.md: one page per instance

_generated/ is mounted into Hugo's content and data (see config.yaml).
Only the Python standard library is used.
"""
import concurrent.futures
import datetime
import json
import os
import re
import shutil
import sys
import unicodedata
import urllib.request

CONF_URL = os.environ.get("VIGILO_CONF_URL", "https://raw.githubusercontent.com/jesuisundesdeux/vigilo-conf/main/main/")
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
OUT = os.path.join(ROOT, "_generated")
TIMEOUT = 15

COUNTRIES = {"France": "fr", "Belgique": "be"}


def get_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": "vigilo-website build"})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
        return json.loads(resp.read().decode("utf-8"))


def slugify(text):
    """Same URLs as the previous generator: lower case, no accents, '-' separators."""
    text = unicodedata.normalize("NFKD", text.lower())
    text = "".join(c for c in text if not unicodedata.combining(c))
    text = re.sub(r"['\"/.]", "-", text)
    text = "-".join(text.split())
    # "Toulon - Var" -> "toulon-var", not "toulon---var"
    return re.sub(r"-{2,}", "-", text).strip("-")


def to_float(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def instance_data(name, conf):
    api_path = conf["api_path"].replace("%3A%2F%2F", "://").rstrip("/")
    country = conf.get("country", "France")
    data = {
        "name": name,
        "country": country,
        "api_path": api_path,
        "scope": conf["scope"],
        "online": False,
        "display_name": name,
    }
    try:
        scope = get_json("%s/get_scope.php?scope=%s" % (api_path, conf["scope"]))
        if not isinstance(scope, dict) or "display_name" not in scope:
            raise ValueError("unexpected answer")
    except Exception as e:
        print("  %s: unreachable (%s)" % (name, e), file=sys.stderr)
        scope = None

    if scope:
        lat = [to_float(scope.get("coordinate_lat_min")), to_float(scope.get("coordinate_lat_max"))]
        lon = [to_float(scope.get("coordinate_lon_min")), to_float(scope.get("coordinate_lon_max"))]
        data.update({
            "online": True,
            "display_name": scope["display_name"] or name,
            "backend_version": scope.get("backend_version", ""),
            "contact_email": scope.get("contact_email") or "",
            "cities": sorted(c.get("name", "") for c in scope.get("cities") or [] if c.get("name")),
        })
        if None not in lat + lon:
            data["bbox"] = [lat[0], lon[0], lat[1], lon[1]]
        center = (scope.get("map_center_string") or "").split(",")
        if len(center) == 2 and None not in map(to_float, center):
            data["center"] = [to_float(center[0]), to_float(center[1])]
        elif "bbox" in data:
            data["center"] = [(lat[0] + lat[1]) / 2, (lon[0] + lon[1]) / 2]
        try:
            last = get_json("%s/get_issues.php?scope=%s&count=1" % (api_path, conf["scope"]))
            if last:
                data["last_observation"] = datetime.datetime.fromtimestamp(
                    int(last[0]["time"]), datetime.timezone.utc).date().isoformat()
        except Exception:
            pass

    data["slug"] = slugify("%s-%s" % (data["display_name"], COUNTRIES.get(country, "fr")))
    return data


def write_page(instance):
    folder = os.path.join(OUT, "content", "villes", instance["slug"])
    os.makedirs(folder, exist_ok=True)
    front = {
        "title": instance["display_name"],
        "layout": "instance",
        "instance": instance["name"],
    }
    with open(os.path.join(folder, "_index.fr.md"), "w", encoding="utf-8") as f:
        f.write("---\n%s\n---\n" % "\n".join("%s: %s" % (k, json.dumps(v, ensure_ascii=False)) for k, v in front.items()))


def main():
    print("Reading vigilo-conf from %s" % CONF_URL)
    citylist = get_json(CONF_URL + "citylist.json")
    categories = get_json(CONF_URL + "categorielist.json")

    prod = [(name, conf) for name, conf in citylist.items() if conf.get("prod")]
    with concurrent.futures.ThreadPoolExecutor(max_workers=16) as pool:
        instances = list(pool.map(lambda item: instance_data(*item), prod))
    instances.sort(key=lambda i: i["display_name"].lower())

    # make sure two instances never share a page
    seen = {}
    for instance in instances:
        if instance["slug"] in seen:
            instance["slug"] += "-" + slugify(instance["scope"])
        seen[instance["slug"]] = True
        if instance["online"]:
            instance["url"] = "/fr/villes/%s/" % instance["slug"]

    shutil.rmtree(OUT, ignore_errors=True)
    os.makedirs(os.path.join(OUT, "data"))
    with open(os.path.join(OUT, "data", "instances.json"), "w", encoding="utf-8") as f:
        json.dump(instances, f, ensure_ascii=False, indent=1)
    with open(os.path.join(OUT, "data", "categories.json"), "w", encoding="utf-8") as f:
        json.dump(categories, f, ensure_ascii=False, indent=1)
    # a page per instance that answers (an unreachable one stays listed, without page)
    for instance in instances:
        if instance["online"]:
            write_page(instance)

    online = sum(1 for i in instances if i["online"])
    print("%d production instances, %d online" % (len(instances), online))


if __name__ == "__main__":
    main()
