import csv, json, sys

ALWAYS_KEEP = {"scheduling_general","definition","classification_scheme","legal_basis","scope",
 "signage","film_carryover","access_control","audience_information","trailers","human_dignity",
 "serious_harm","commercial_conditions","channel_override","data_protection"}

AGNOSTIC = {"all_linear_tv","all_avms"}

def toks(s):
    return {t.strip() for t in s.split(';') if t.strip()}

def build(path, countries, service_tokens, observed_cats, asset_implied=()):
    rows = list(csv.DictReader(open(path)))
    keep = []
    for x in rows:
        if x['status'] != 'approved':
            continue
        if x['country'] not in countries:
            continue
        st = toks(x['service_type'])
        service_ok = bool(st & service_tokens) or bool(st & AGNOSTIC)
        cat = x['content_category']
        prohibition = (x['classification'] == 'prohibited') or (x['time_rule_machine'] == 'prohibited')
        cat_ok = cat in observed_cats or cat in ALWAYS_KEEP or cat in asset_implied or prohibition
        if service_ok and cat_ok:
            keep.append(x)
    return keep

if __name__ == '__main__':
    import pathlib
    HERE = pathlib.Path(__file__).resolve().parent
    path = str(HERE.parent / 'rules' / 'csv' / 'Rules.csv')
    case = sys.argv[1]
    if case == 'TC-09':
        cats = {"violence","imitable_behaviour","drugs_alcohol_smoking"}
    else:
        cats = {"sexual_content","nudity"}
    countries = {"UK","FR","EU"}
    svc = {"free_to_air"}
    keep = build(path, countries, svc, cats)
    out = str(HERE / f'{case}_slice.json')
    json.dump(keep, open(out,'w'), indent=1, ensure_ascii=False)
    import collections
    print(case, 'kept', len(keep), collections.Counter(k['country'] for k in keep))
    print(sorted({k['content_category'] for k in keep}))
    print([k['rule_id'] for k in keep])
