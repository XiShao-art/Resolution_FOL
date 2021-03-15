# Resolution_FOL

## Basic
Use a programming language of your choice to implement a domain-specific language for first order logic. The domain-specific language must allow for specifying a signature and then specifying a theory (knowledge base) using this signature. Raise an error if symbols in the theory do not correspond to the signature. It should be possible to specify arbitrary first order formulas (i.e., do not limit the theory to formulas in a particular normal form).

Note: you can decide the syntax of this language and use either infix, prefix, or postfix (reverse Polish) notation; prefix notation

 (e.g.: (exists x (and (P x) (Q x)))) will likely be the easiest to implement (you can implement this as a list and will only have to call head to find the main logical operator).

## CNF
Implement an algorithm to convert your theory into conjunctive normal form and then into Skolem normal form.

## MGU
Implement an algorithm that finds a most general unifier for a set of literals.

## Resolution
We can formulate queries to a theory as formulas in the same
signature as the theory that are either entailed or not. Implement resolution for first order logic to determine if a theory entails a query formula
or not. Use this system to:
– Formalize in first order logic (using B(x) for “x is a barber” and
S(x, y) for “x shaves y”):
1. A barber shaves all persons who do not shave themselves.
2. No barber shaves someone who shaves himself.
3. There is no barber.
Show using your algorithm that (3) is a consequence of (1) and (2).