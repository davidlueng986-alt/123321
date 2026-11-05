// CAP050 independent C++17 exact-integer global <=290 certificate checker.
// Uses external published: AG6 maximal112 unique centrally symmetric,
// PG(6,3) projective cap maximum <=136. Exact r3(7) still OPEN.
#include <cassert>
#include <cstdint>
#include <iostream>
using I=long long;
I ip(I a,int n){I p=1;while(n--)p*=a;return p;}
int main(){
 const I N=291,D=1093;
 const I S2=31036023,S3=3043505853LL;
 int profiles=0,zero1=0,zero2=0;
 for(I a=67;a<=112;a++)for(I b=a;b<=112;b++){
  I c=N-a-b;if(c<b||c>112)continue;
  I q2=ip(a,2)+ip(b,2)+ip(c,2);
  I q3=ip(a,3)+ip(b,3)+ip(c,3);
  I q4=ip(a,4)+ip(b,4)+ip(c,4);
  I ind=(c==112);
  I p1=1350*ind+5080860-277*q2+q3;
  I p2=9957864606LL-743397*q2+5482*q3-15*q4;
  assert(p1>=0 && p2>=0);
  if(p1==0)zero1++;
  if(p2==0)zero2++;
  profiles++;
 }
 assert(profiles==192 && zero1==3);
 I Tlower1350=-5080860LL*D+277*S2-S3;
 assert(Tlower1350==92538 && Tlower1350>68*1350);
 const I T=69;
 for(I d=0;d<=136;d++){
  const I delta=(d-22)*(d-23)/2;
  assert(delta>=0);
  if(d<56)continue;
  const I k=(d-2)/3;
  const I numerator=40*d*(d-1)*(d-2)+(2-2*k)*121*d*(d-1)+k*(k-1)*364*d;
  const I denominator=56*(56-k)*(55-k);
  assert(numerator>=0 && denominator>0);
  const I slack=delta*denominator-46*numerator;
  assert(slack>=0);
  if(d==136){assert(k==44&&slack>0);}
 }
 const I Pmin=448602+46*T;
 assert(Pmin==451776);
 assert(Pmin*1215-548600572LL==307268);
 std::cout<<"CAP050_CERT_PASS profiles="<<profiles
          <<" equality_h112="<<zero1<<" equality_S4="<<zero2
          <<" degrees_checked=137 exact_contradiction_over1215="
          <<Pmin*1215-548600572LL
          <<" projective_cap_upper=136 global_bound_candidate=290\n";
}
