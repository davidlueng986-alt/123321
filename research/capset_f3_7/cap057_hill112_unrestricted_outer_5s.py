"""Direct 237 existence with an EXACT 112-point 6D Hill slice.

All 729+729 outer point variables free; not restricted to an affine
image of the known two-slice 236 construction. This is a CONDITIONAL
branch, not an unsat proof of arbitrary 7D 237 caps.
"""
import os,time,json
os.environ['OPENBLAS_NUM_THREADS']='1'
import numpy as np
from scipy.sparse import coo_matrix,csr_matrix,vstack
from scipy.optimize import milp,Bounds,LinearConstraint
S=[l.strip() for l in open('/mnt/data/capset_v5/witness236.txt') if len(l.strip())==7]
assert len(S)==236 and len(set(S))==236
A0={int(t[1:],3) for t in S if t[0]=='0'}
A1={int(t[1:],3) for t in S if t[0]=='1'}
A2={int(t[1:],3) for t in S if t[0]=='2'}
assert tuple(map(len,[A0,A1,A2]))==(112,112,12)
N=729
D=np.array([[int(v) for v in np.base_repr(i,3).zfill(6)] for i in range(N)],dtype=np.int8)
weights=(3**np.arange(5,-1,-1)).astype(np.int32)
THIRD=((6-D[:,None,:]-D[None,:,:])%3)@weights
assert np.array_equal(THIRD,THIRD.T)
# All 6D lines: choose a<b<c third(a,b)=c
p,q=np.triu_indices(N,k=1)
z=THIRD[p,q]
mask=z>q
P=p[mask];Q=q[mask];R=z[mask];L=len(P)
assert L==88452, L
start=time.monotonic()
# one 3AP constraint per line separately in each B/C slice
row_idx=np.repeat(np.arange(2*L,dtype=np.int32),3)
col_idx=np.concatenate([np.stack([P,Q,R],axis=1).ravel(),(np.stack([P,Q,R],axis=1)+N).ravel()]).astype(np.int32)
assert len(col_idx)==len(row_idx)
upper=np.full(2*L,2.,dtype=float)
# For x in B, every a in fixed H and y=-a-x in C is forbidden.
A0sorted=np.array(sorted(A0),dtype=np.int32)
B=np.repeat(np.arange(N,dtype=np.int32),len(A0))
AA=np.tile(A0sorted,N)
C=THIRD[B,AA]
crossn=len(B)
assert crossn==81648
rowscross=np.repeat(np.arange(2*L,2*L+crossn,dtype=np.int32),2)
colscross=np.stack([B,N+C],axis=1).ravel().astype(np.int32)
allrow=np.concatenate([row_idx,rowscross])
allcol=np.concatenate([col_idx,colscross])
allupper=np.r_[upper,np.ones(crossn)]
M=coo_matrix((np.ones(len(allrow)),(allrow,allcol)),shape=(2*L+crossn,2*N)).tocsr()
# exact 125 selected outer, 112 in slice H -> 237. B>=C wlog by swapping layers.
rows=[];cols=[];vals=[]
for a in range(2*N):rows.append(0);cols.append(a);vals.append(1.)
for a in range(2*N):rows.append(1);cols.append(a);vals.append(1. if a<N else -1.)
for a in range(N):rows.append(2);cols.append(a);vals.append(1.)
for a in range(N,2*N):rows.append(3);cols.append(a);vals.append(1.)
extra=coo_matrix((vals,(rows,cols)),shape=(4,2*N)).tocsr()
M=vstack([M,extra],format='csr')
lower=np.r_[np.full(2*L+crossn,-np.inf),[125,0,0,0]]
upper=np.r_[allupper,[125,np.inf,112,112]]
# Check actual 236 cap is valid at target 124, reject source mistakes
witness=np.zeros(2*N,dtype=np.float64)
witness[list(A1)]=1;witness[N+np.array(list(A2),dtype=int)]=1
baseout=M@witness
assert max(baseout[:2*L+crossn]-allupper)<=1e-12
assert baseout[2*L+crossn]==124
print('SOURCE_CONTROL',json.dumps({'slice_H112':112,'B':len(A1),'C':len(A2),'source_target':'124 (known 236cap)','source_3AP_cross_valid':True}),flush=True)
print('GLOBAL_HILL_SUBCASE',json.dumps({'matrix_rows':int(M.shape[0]),'variables':2*N,'nonzeros':M.nnz,'sixD_lines':int(L),'cross_edges':crossn,'build_s':round(time.monotonic()-start,3),'target_size':237,'fixed_slice':112}),flush=True)
res=milp(c=np.zeros(2*N),integrality=np.ones(2*N),bounds=Bounds(np.zeros(2*N),np.ones(2*N)),constraints=LinearConstraint(M,lower,upper),options={'time_limit':5.,'disp':True,'mip_rel_gap':0.0})
out={'status':int(res.status),'message':res.message,'solver_fun':None if res.fun is None else res.fun,'solver_dual_bound':None if res.mip_dual_bound is None else res.mip_dual_bound,'elapsed_total_s':round(time.monotonic()-start,3)}
if res.x is not None:
 selected=np.flatnonzero(res.x>0.5)
 candidate=A0|{N+i for i in selected if i<N}|{2*N+(i-N) for i in selected if i>=N}
 codes=[]
 for t in A0:codes.append('0'+np.base_repr(t,3).zfill(6))
 for i in selected:codes.append(('1' if i<N else '2')+np.base_repr(i%N,3).zfill(6))
 assert len(codes)==237
 X={tuple(map(int,t)) for t in codes}
 assert len(X)==237
 for a in X:
  for b in X:
   if a!=b:assert tuple((-a[k]-b[k])%3 for k in range(7)) not in X
 open('/mnt/data/capset_v5/CAP057_NEW_237_CAP.txt','w').write('n: 7\n'+'\n'.join(codes)+'\n')
 out['verified_237_witness']=True
else:out['verified_237_witness']=False
print('RESULT',json.dumps(out),flush=True)
open('/mnt/data/capset_v5/hill_unrestricted_result.json','w').write(json.dumps(out,indent=2)+'\n')
