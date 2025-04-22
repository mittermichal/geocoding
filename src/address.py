def format_address(record):
    toks = []
    # print(list(record.items()))
    if record['name']:
        toks.append(record['name'])
    if record['place']:
        toks.append(record['place'])
    if record['housenumber'] and record['street']:
        toks.append(f"{record['street']} {record['housenumber']}")
    elif record['street']:
        toks.append(record['street'])
    if record['postcode'] and record['city']:
        toks.append(f"{record['postcode']} {record['city']}")
    elif record['city']:
        toks.append(record['city'])
    if record['state']:
        toks.append(record['state'])
    if record['country']:
        toks.append(record['country'])
    if toks:
        return ', '.join(set(toks)) # remove duplicates
    else:
        "unnamed place"

