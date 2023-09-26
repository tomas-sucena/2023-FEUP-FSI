
# ENLBufferPwn

## Identification

- ENLBufferPwn ([CVE-2022-47949](https://nvd.nist.gov/vuln/detail/CVE-2022-47949)) is a vulnerability that used to be present in the shared network code of many Nintendo games.
- It exploits a C++ class previously within their network library, whose functions could cause a buffer overflow.
- This vulnerability allowed attackers to execute code on the victim's console simply by playing an online game with them.


## Tabulation

- This vulnerability was discovered by a multitude of users, who opted to keep the information private.
- It was disclosed safely to Nintendo by ["PabloMK7"](https://github.com/PabloMK7), ["Rambo6Glaz"](https://github.com/EpicUsername12) and ["Fishguy6564"](https://github.com/fishguy6564) in 2021.
- The vulnerability has a CVSS score of 9.8/10, thus classifying as critical.


## Exploit 

- The class `NetworkBuffer` represents a buffer which stores data exchanged between players during an online game.
- Two of its methods, `Set` and `Add`, update the network buffer, filling it with data coming from other players.
- However, neither of these methods check whether or not the input data fits within the network buffer. 
- As such, due to this oversight, attackers could freely exploit buffer overflows to send payloads to the victim.

```cpp
class NetworkBuffer
{
public:
    u8	bufferType;
    u8* dataPtr;
    u32 dataSize;
    u32 currentSize;

    void Set(u8* newData, u32 newDataSize);
    void Add(u8* newData, u32 newDataSize);
}

void NetworkBuffer::Set(u8* newData, u32 newDataSize)
{
    memcpy(this->dataPtr, newData, newDataSize);
    this->currentSize = newDataSize;
}

void NetworkBuffer::Add(u8* newData, u32 newDataSize)
{
    memcpy(this->dataPtr + this->currentSize, newData, newDataSize);
    this->currentSize += newDataSize;
}
```

## Attacks

- The consequences of such an attack depend on the game used to perform it.
- Using this exploit, an attacker could go as far as to have full control over the victim's console.
- Games on the Nintendo 3DS, due to its lack of security measures, are susceptible to the most severe consequences.


---
### Sources
- https://github.com/PabloMK7/ENLBufferPwn
- https://nvd.nist.gov/vuln/detail/CVE-2022-47949
