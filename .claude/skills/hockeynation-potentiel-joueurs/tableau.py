import json,collections
rows=json.load(open('pot.json',encoding='utf-8'))
def grade(p):
    m=p['min']
    g='Fort' if m>=74 else 'Solide' if m>=68 else 'Moyen' if m>=58 else 'Nul'
    return g+(' ↑' if p['max']-p['min']>=15 and p['age']<=23 else '')
def futur(p):
    mn,mx,a=p['min'],p['max'],p['age']
    if mn>=64: return 'PRO'
    if a<=23 and mn>=55 and mx>=80: return 'PRO'
    if mn>=52: return 'FRM'
    if a<=23 and mx>=75: return 'FRM'
    return 'VIRER'
out=[];cnt=collections.Counter()
for i,p in enumerate(rows,1):
    f=futur(p);cnt[(p['t'],f)]+=1
    out.append(f"| {i} | {p['t']} | {p['name']} | {p['age']} | {p['pos']} | {p['r']} | {p['min']} | {p['max']} | {p['sp'].replace(',',', ') or '—'} | {grade(p)} | **{f}** |")
open('table.md','w',encoding='utf-8').write('\n'.join(out))
print('\n'.join(out));print(dict(cnt))
