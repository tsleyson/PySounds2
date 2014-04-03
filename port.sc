# Whee! Another comment!
VOWEL=a e i o u
C=p t c q b d g m n l r h s
F=i e
B=o u
-STOP=p t c
+STOP=b d g

s//_#
m//_#
e//[VOWEL]r_#
v//[VOWEL](')_[VOWEL]
u/o/_#
gn/nh/_
[-STOP]/[+STOP]/[VOWEL](')_[VOWEL]
c/i/[F]_t
c/u/[B]_t
#c//!#_
p//[VOWEL]_(')t
ii/i/_
e//[C]_r[VOWEL]
[VOWEL]/@/!'([C])([C])_
h//#_
