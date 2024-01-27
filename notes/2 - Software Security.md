# Software Security

## Countermeasures

### Operating System

#### Data Execution Prevention

Also known as **W ^ X**, this countermeasure guarantees that **memory** can never simultaneously:
* Be **writable** by a program
* Contain **executable** code

It can be implemented in hardware (NX bit) or emulated in software.

##### Limitations

* By itslef
