"""Erzwungene Ausrichtung ohne Spracherkennung: Skript mit Piper sprechen lassen und per DTW
(MFCC) auf die echte Aufnahme legen. Liefert Satzgrenzen + Kosten (niedrig = Aufnahme passt zum Skript).
Erfahrungswerte: passendes Skript ≈ 0,55–0,60, falsches Skript ≈ 0,70."""
import sys, json, subprocess, numpy as np, librosa, tempfile
SR=16000
def piper_wav(text):
    with tempfile.NamedTemporaryFile(suffix='.wav') as f:
        subprocess.run([sys.executable,'-m','piper','-m','/root/tts/de-thorsten-low.onnx','--sentence-silence','0','--noise-w','0','--noise-scale','0','-f',f.name],input=text.encode(),stderr=subprocess.DEVNULL,check=True)
        y,_=librosa.load(f.name,sr=SR); return y
def feats(y,hop=160):
    m=librosa.feature.mfcc(y=y,sr=SR,n_mfcc=20,hop_length=hop)[1:]
    m=(m-m.mean(1,keepdims=True))/(m.std(1,keepdims=True)+1e-6); return m
def align(audio, sentences):
    ref=[];bounds=[];t=0
    for s in sentences:
        y=piper_wav(s); y,_=librosa.effects.trim(y,top_db=35); ref.append(y); t+=len(y); bounds.append(t)
    R=np.concatenate(ref); Y,_=librosa.load(audio,sr=SR)
    # Lange Aufnahmen: gröbere Auflösung, damit die DTW-Matrix in den Speicher passt (max. ~12 Mio. Zellen)
    hop=160
    while (len(R)/hop)*(len(Y)/hop) > 12e6: hop*=2
    A=feats(R,hop); B=feats(Y,hop)
    D,wp=librosa.sequence.dtw(X=A,Y=B,metric='cosine',step_sizes_sigma=np.array([[1,1],[0,1],[1,0]]))
    wp=wp[::-1]; cost=D[-1,-1]/len(wp)
    out=[]
    for b in bounds[:-1]:
        fr=b//hop; idx=np.searchsorted(wp[:,0],fr); out.append(round(float(wp[min(idx,len(wp)-1),1])*hop/SR,3))
    return out,float(cost)
if __name__=='__main__':
    audio=sys.argv[1]; sk=json.load(open(sys.argv[2]))['saetze']
    b,c=align(audio,[s['sprechtext'] for s in sk]); print('cost',round(float(c),4),'grenzen',b)
