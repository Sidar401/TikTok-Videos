"""Stichprobe nach sync.py: passt jeder Satz an seiner Stelle besser als an der Nachbarstelle?
Aufruf: python3 scripts/stichprobe.py videos/<name>/ 5 20 50 ... (Satz-Indizes, 0-basiert). OK = richtig ausgerichtet."""
import sys, json, numpy as np, librosa
sys.path.insert(0, __import__('os').path.dirname(__file__))
from dtw_align import piper_wav, feats, SR
v=sys.argv[1]
t=json.load(open(v+'timings.json'))['saetze']; sk={s['id']:s for s in json.load(open(v+'skript.json'))['saetze']}
Y,_=librosa.load(v+'assets/voice.wav',sr=SR)
def cost(a,b):
    D,wp=librosa.sequence.dtw(X=a,Y=b,metric='cosine'); return D[-1,-1]/len(wp)
for i in [int(x) for x in sys.argv[2:]]:
    ref=feats(librosa.effects.trim(piper_wav(sk[t[i]['id']]['sprechtext']),top_db=35)[0])
    row=[]
    for j in (i-1,i,i+1):
        c=Y[int(t[j]['start']*SR):int(t[j]['end']*SR)]
        row.append(round(cost(ref,feats(c)),3))
    print(t[i]['id'], row, 'OK' if row[1]==min(row) else '??', sk[t[i]['id']]['sprechtext'][:40])
