stats = [{'base_stat': 45, 'stat': {'name': 'speed'}}, {'base_stat': 95, 'stat': {'name': 'fire'}}]

for d in stats:
    base = d['base_stat']
    item = {k: v for k, v in d.items() if k == 'stat'}
    newd[f"{base}"]
