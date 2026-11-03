# CAP-045 — Hostile logical audit of CAP-019's 110-to-111 completion bridge

Date: 2026-11-03 UTC. Scope: one theorem-level dependency in the provisional r3(7)<=287 argument; **not** a new bound, proof of the full CAP-019 theorem, or a solver result.

## Abstract completion lemma (self-contained)

Let C be a cap in a finite affine geometry, |C|=N, and assume **every point p outside C lies on at least k pairwise vertex-disjoint secants of C** (each secant is an unordered pair of distinct points of C whose third point is p). If B subset C and |C\B|<k, then every point p extending B to a cap lies in C.

Proof: suppose p outside C and B union {p} is a cap. Each of the k vertex-disjoint secants through p must lose at least one endpoint when C is restricted to B, otherwise that endpoint pair with p is a forbidden 3-term progression. Since their endpoint sets are disjoint, at least k points must be deleted, contradicting |C\B|<k. QED.

Corollary (uniqueness): If B is contained in two N-caps C and C' each satisfying the k-disjoint-secant property and |C\B|<k, then C=C'. Indeed any p in C'\C extends B and hence belongs to C. Thus C' subset C, and equal sizes imply equality. This proof does not require assuming uniqueness in advance.

## Application to CAP-019

Use the external Thackeray 2022 statement that every 110-cap in AG(6,3) embeds into some 112-cap C, and CAP-010A's claimed independently checked lower bound of at least 10 vertex-disjoint secants through every p outside a 112-cap (requires the published affine uniqueness of 112-caps to transfer from the canonical representative). Here N=112, k=10, |C\B|=2<10.

For a 111-cap T, remove any point p in T to obtain B of size 110. Thackeray supplies C containing B. Since B union {p}=T is a cap, the abstract lemma forces p in C. Therefore T subset C, without assuming a priori that 110-caps have unique completion. In fact uniqueness follows as a corollary.

Thus the logical implication in CAP-019 is valid **conditional on the external classification and CAP-010A secant-stability premises**. This audit does not independently re-run Thackeray's classification, CAP-010A's 729-point arithmetic, the Fourier common-tangent lemma, or the 28-case residue certificate. The bound <=287 must remain provisional.

## Adversarial checks / failure modes

- Mere existence of a 112 completion is not enough to prove 111 completion; the k-disjoint-secant property is essential.
- A count of k secants without vertex-disjointness would not suffice: one deleted point could block many overlapping secants.
- The threshold is strict: |C\B|<k. Equality is insufficient in general.
- The affine uniqueness of 112-caps is used only to propagate the verified k property from a representative, not in the abstract lemma.
- Source novelty: the hitting-set argument is elementary; no novelty claimed. Public source rechecked 2026-11-03: https://arxiv.org/abs/2206.09804 (abstract asserts 110-cap completion; does not itself certify the local CAP-010A computation).
- No GPU, paid compute, random seeds, solver or candidate-point experiment. This is a deductive proof audit; reproducibility is the displayed proof, not a claimed CI arithmetic run.

## Meta-audit

CAP-044 was a low-leverage orbit regression. CAP-045 instead closes a *logical* dependency in a potentially stronger global bound, while explicitly leaving the major risk (independent 110-cap classification and Fourier/tangent referee) unresolved. Next work: external proof-source review or bounded proof-logged SAT on a complete global root leaf. Exact r3(7) OPEN; no >=237 witness, no new verified upper bound.
