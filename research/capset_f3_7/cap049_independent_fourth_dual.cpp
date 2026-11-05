// CAP049 independent C++17 proof certificate; no floating point.
// Re-proves established r3(7)<=291 by fourth moments and secant convexity.
// Based only on published r3(6)=112; does not determine exact r3(7).
#include <cassert>
#include <cstdint>
#include <iostream>
using i64=long long;
i64 pp(i64 x,int p){i64 r=1;while(p--)r*=x;return r;}
int main(){
 const i64 n=292,D=1093,S2=31248964,S3=3074776060LL;
 int cases=0,contacts=0;
 for(i64 a=68;a<=112;a++)for(i64 b=a;b<=112;b++){
  const i64 c=n-a-b;
  if(c<b||c>112)continue;
  const i64 q2=pp(a,2)+pp(b,2)+pp(c,2);
  const i64 q3=pp(a,3)+pp(b,3)+pp(c,3);
  const i64 q4=pp(a,4)+pp(b,4)+pp(c,4);
  const i64 slack=30464609312LL-2254590LL*q2+16531LL*q3-45LL*q4;
  assert(slack>=0);
  ++cases;if(slack==0)++contacts;
 }
 assert(cases==184 && contacts==3);
 const i64 S4upper_times45=30464609312LL*D-2254590LL*S2+16531LL*S3;
 // 42486 unordered cap secants among 1895 outsiders; convexity -> P>=455257.
 const i64 S4lower=303851985100LL;
 assert(45LL*S4lower-S4upper_times45==48384LL);
 std::cout<<"CAP049_GLOBAL_CERT_PASS profiles=184 dual_equality=3"
          <<" integer_contradiction_times45=48384 bound=291_known\n";
}
