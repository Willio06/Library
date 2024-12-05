## CTF 1
the first ctf consists of finding a basis of signed words in order to sign a new linear dependent word with all the other's signatures. First lecture slide p22-25
## CTF 2
#### (a) 
just generate 24 random hexes and add your target to give to the hash oracle. didn't work, i put my target at the end of the list, why it doesnt work i dont know. changed it to random placement and worked instantly
#### (b)
juist hetzelfde probleem met randomness, werkte alleen dan. pak willekeurig een $k$, doe $a=k^2$ en $x=sqrt(a)$, als $k\neq x$ hebben we dat $(x-k)(x+k)=x^2-k^2 = 0\ mod\ n$ en dus $gcd(x+k,n)$ is een niet triviale factor
