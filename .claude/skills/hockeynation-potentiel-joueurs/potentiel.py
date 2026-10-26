import json
def parse(line):
    t,name,age,pos,rt,sk,st,wk,sp=line.rstrip('\n').split('|')
    S={}
    for tok in sk.split():
        mx=tok.endswith('*'); tok=tok.rstrip('*'); S[tok[:3]]=(int(tok[3:]),mx)
    return dict(t=t,name=name,age=int(age),pos=pos,r=int(rt),S=S,strong=st.split(','),weak=wk,sp=sp)
def bounds(p):
    S=p['S'];strong=p['strong'];weak=p['weak']
    wl,wm=S[weak]
    Wmin=wl if wm else wl+1
    su=[s for s in strong if not S[s][1]]
    sm=[S[s][0] for s in strong if S[s][1]]
    if len(su)==0: C=min(sm)
    elif len(su)==1: C=sm[0]
    else: C=10
    normals=[k for k in S if k not in strong and k!=weak]
    C=max([C]+[S[k][0] for k in normals if S[k][1]])
    lo={};hi={}
    for k in S:
        l,m=S[k]
        if m: lo[k]=hi[k]=l
        elif k==weak: lo[k]=l+1
        elif k in strong:
            lo[k]=l
            hi[k]=10 if len(su)==2 else max(l+1,sm[0])
        else:
            lo[k]=max(l,Wmin); hi[k]=max(C,l+1)
    if not wm:
        others=[hi[k] for k in S if k!=weak]
        hi[weak]=max(Wmin,min(others)-1)
        # floor on weak is Wmin, normals floor uses Wmin
    else:
        lo[weak]=hi[weak]=wl
    cur=sum(S[k][0] for k in S)
    rmin=p['r']+sum(lo[k]-S[k][0] for k in S)
    rmax=p['r']+sum(hi[k]-S[k][0] for k in S)
    return rmin,rmax
rows=[]
for l in open('players.txt',encoding='utf-8'):
    if l.strip():
        p=parse(l);p['min'],p['max']=bounds(p);rows.append(p)
rows.sort(key=lambda p:(-p['min'],-p['max']))
json.dump(rows,open('pot.json','w',encoding='utf-8'),ensure_ascii=False)
for p in rows:
    print(p['t'],p['name'],p['age'],p['pos'],p['r'],p['min'],p['max'],p['sp'])
