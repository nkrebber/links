import numpy as np, wave
sr=48000; T=120; N=sr*T; rng=np.random.default_rng(3)
L=np.zeros(N); R=np.zeros(N)
f=lambda m:440*2**((m-69)/12)
def put(sig,t0,pan=.5,g=1):
    i=int(t0*sr); n=min(len(sig),N-i)
    if n>0: L[i:i+n]+=sig[:n]*g*np.cos(pan*np.pi/2); R[i:i+n]+=sig[:n]*g*np.sin(pan*np.pi/2)
def pad(m,d):
    t=np.arange(int(d*sr))/sr; s=0
    for det in(-.07,0,.06):
        for h,a in((1,1),(2,.35),(3,.18),(4,.07)): s=s+a*np.sin(2*np.pi*f(m+det)*h*t+rng.random()*6)
    a=1.8; env=np.clip(t/a,0,1)*np.clip((d-t)/2.5,0,1); return s*env*(1+.15*np.sin(2*np.pi*.23*t))
def pluck(m,d=3.0):
    n=int(sr/f(m)); buf=rng.uniform(-1,1,n); k=int(d*sr); out=np.empty(k)
    reps=k//n+1; cur=buf
    chunks=[]
    for _ in range(reps):
        chunks.append(cur); cur=.996*.5*(cur+np.roll(cur,1))
    out=np.concatenate(chunks)[:k]; return out*np.exp(-np.arange(k)/sr/1.4)
# D dorian progression, 8 s per chord
prog=[(50,[62,65,69]),(48,[60,64,67]),(46,[58,62,65]),(45,[57,60,64]),(50,[62,65,69]),(53,[60,65,69]),(55,[59,62,67]),(45,[57,61,64])]
scale=[62,64,65,67,69,71,72,74,76,77]
bar=8.0
for i in range(15):
    root,ch=prog[i%8]; t0=i*bar
    put(pad(root-12,bar+3),t0,.5,.10); put(pad(root,bar+3),t0,.5,.07)
    for j,m in enumerate(ch): put(pad(m,bar+3),t0,.25+.25*j,.05)
    if 1<=i<14:
        # lute arpeggio
        pat=[ch[0],ch[1],ch[2],ch[1]+12 if i%2 else ch[2],ch[2],ch[1],ch[0]+12,ch[1]]
        for j,m in enumerate(pat): put(pluck(m),t0+j*1.0+rng.normal(0,.012),.35+.3*rng.random(),.16)
    if 3<=i<13:
        # melody (flute-like sine with vibrato)
        idx=4+int(rng.integers(-2,3))
        tt=0
        while tt<bar:
            d=float(rng.choice([1,1,2,2,3])); idx=int(np.clip(idx+rng.integers(-2,3),0,9)); m=scale[idx]
            if m%12 not in [(c%12) for c in ch] and rng.random()<.5: m=ch[int(rng.integers(0,3))]+12
            t=np.arange(int((d+.6)*sr))/sr; ph=2*np.pi*f(m)*t+.9*np.sin(2*np.pi*5*t)*np.clip(t-.3,0,1)*.6
            s=(np.sin(ph)+.25*np.sin(2*ph)+.08*np.sin(3*ph))*np.clip(t/.12,0,1)*np.clip((d+.6-t)/.5,0,1)
            put(s,t0+tt,.6,.085 if 8<=i<10 else .07); tt+=d
# simple reverb (feedback delays)
def rev(x):
    y=x.copy()
    for dl,g in((.031,.45),(.047,.4),(.083,.35),(.127,.3),(.211,.25),(.337,.2)):
        k=int(dl*sr); z=np.zeros_like(x); z[k:]=y[:-k]; y=y+g*z
    return y
L=rev(L); R=rev(R[::-1])[::-1]*0+rev(R)
t=np.arange(N)/sr; env=np.clip(t/3,0,1)*np.clip((T-t)/5,0,1)
st=np.stack([L,R],1)*env[:,None]; st/=np.abs(st).max()/.82
w=wave.open('music.wav','wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr); w.writeframes((st*32767).astype('<i2').tobytes()); w.close()
print('ok')
