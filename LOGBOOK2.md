
# ENLBufferPwn

## Identification

- ENLBufferPwn (CVE-2022-47949) is a formerly present vulnerability in the shared network code of many Nintendo games.
- It exploits a C++ class previously within their network library, whose functions could cause a buffer overflow.
- This vulnerability allowed an exploiter to execute code on the victim's console simply by playing an online game with them.


## Tabulation

- This vulnerability was discovered by a multitude of users, who chose to keep the information private.
- It was disclosed safely to Nintendo by ["PabloMK7"](https://github.com/PabloMK7), ["Rambo6Glaz"](https://github.com/EpicUsername12) and ["Fishguy6564"](https://github.com/fishguy6564) in 2021.
- The vulnerability has a CVSS score of 9.8/10, thus classifying as critical.


## Exploit 

- The class `NetworkBuffer` is used as a generic container to share data between the players of an online game using it.
- Two of its methods, `Set` and `Add`, do not check whether their provided data fits in the buffer size.
- This allows an exploiter to freely send payloads to the victim.


## Attacks

- The consequences of such an attack depend on the game used to perform it.
- Using this exploit, an attacker could go as far as to have full control over the victim's console.
- Games on the Nintendo 3DS, due to its lack of security measures, are susceptible to the most severe consequences.


---
### Sources
- https://github.com/PabloMK7/ENLBufferPwn
- https://nvd.nist.gov/vuln/detail/CVE-2022-47949
