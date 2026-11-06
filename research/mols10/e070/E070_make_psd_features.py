#!/usr/bin/env python3
"""Precompute branch-specific 19-point root Schur PSD features for C++ DLX.
This file is exploratory: floating PSD rejection is not a formal proof unless
an exact negative integer witness is independently validated.
"""
from pathlib import Path
import numpy as np,struct,json,sys
ROOT=Path(__file__).resolve().parent
R=[json.loads(x) for x in (ROOT/'E064_12_representatives.jsonl').read_text().splitlines()]
i=int(sys.argv[1]) if len(sys.argv)>1 else 0
f,g=R[i]['B_col0'],R[i]['C_col0']
points=np.array([(0,c,c,c,c) for c in range(10)]+[(r,0,r,f[r],g[r])for r in range(1,10)],int)
match=(points[:,None,:]==points[None,:,:]).any(2).astype(float)
np.fill_diagonal(match,0)
Q=25*np.eye(19)-5*match+2*np.ones((19,19))
eig,U=np.linalg.eigh(Q);valid=eig>1e-7;assert int(valid.sum())==17
allpoints=np.indices((10,10,10,10,10),dtype=np.int16).reshape(5,-1).T
cross=2-5*(allpoints[:,None,:]==points[None,:,:]).any(2).astype(float)
W=(cross@U[:,valid])/np.sqrt(eig[valid])[None,:]
name=ROOT/f'E070_branch{i}_psd_features.bin'
with open(name,'wb')as out:
 out.write(struct.pack('<2i',len(W),W.shape[1]))
 out.write(W.astype('<f8',copy=False).tobytes())
 Pinv=(U[:,valid]/eig[valid])@U[:,valid].T
 out.write(Pinv.astype('<f8',copy=False).tobytes())
print(json.dumps({'branch':i,'root_rank':int(valid.sum()),'allpoint_tuples':len(W),'feature_dim':W.shape[1],'bytes':name.stat().st_size}))
