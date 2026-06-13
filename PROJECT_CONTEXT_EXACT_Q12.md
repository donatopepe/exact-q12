# EXACT-Q12 — Project Context

## Nome progetto

**EXACT-Q12**

Nome cartella consigliato:

```bash
exact-q12
```

Nome package Python:

```text
exactq12
```

---

## Obiettivo

Sviluppare una **CLI Python** e, in una fase successiva, un possibile core **FPGA/SystemVerilog per Tang Nano 20K**.

Il progetto deve simulare piccoli circuiti quantistici usando **aritmetica simbolica esatta** basata su:

```text
x = (a + b√2 + c√3 + d√6) / 12^E
```

La base 12 deve essere usata **internamente nei calcoli**, non come semplice output estetico.

Non interessa generare output romano.  
L’obiettivo è avere un formato numerico alternativo, esatto per un insieme controllato di gate quantistici.

---

## Definizione matematica

Ogni numero reale interno appartiene al campo:

```text
Q(√2, √3)
```

ed è rappresentato come:

```text
Q12 = (a + b√2 + c√3 + d√6) / 12^E
```

dove:

```text
a, b, c, d = coefficienti interi signed
E = esponente del denominatore 12^E
```

Un numero complesso è:

```text
CQ12 = real + i·imag
```

dove:

```text
real = Q12
imag = Q12
```

Quindi ogni ampiezza quantistica complessa contiene:

```text
real: a, b, c, d
imag: a, b, c, d
```

Totale:

```text
8 coefficienti interi per ampiezza
```

---

## Perché il formato è utile

Questo formato rappresenta esattamente valori come:

```text
1/2
1/3
1/4
1/6
1/12
√2/2
√3/2
√6/4
```

Quindi permette di rappresentare esattamente gate come:

```text
H
S
T
P30
P60
P90
P120
P180
X
Z
CNOT
SWAP
```

Non rappresenta esattamente rotazioni arbitrarie come:

```text
RZ 17°
RX 23°
RY arbitrario
```

a meno di estendere ulteriormente il campo simbolico.

---

## Formula fondamentale di moltiplicazione

Dati:

```text
x = a + b√2 + c√3 + d√6
y = e + f√2 + g√3 + h√6
```

allora:

```text
x · y = A + B√2 + C√3 + D√6
```

con:

```text
A = ae + 2bf + 3cg + 6dh
B = af + be + 3ch + 3dg
C = ag + ce + 2bh + 2df
D = ah + de + bg + cf
```

Questa formula è il cuore del progetto.

---

## Riduzione del denominatore

Dopo ogni operazione, se tutti i coefficienti sono divisibili per 12, bisogna ridurre:

```text
se a, b, c, d sono tutti divisibili per 12:
    a = a / 12
    b = b / 12
    c = c / 12
    d = d / 12
    E = E - 1
```

Questo mantiene i coefficienti più piccoli senza perdere esattezza.

---

## Costanti principali

### Zero

```text
0 = (0 + 0√2 + 0√3 + 0√6) / 12^0
```

### Uno

```text
1 = (1 + 0√2 + 0√3 + 0√6) / 12^0
```

### Un mezzo

```text
1/2 = 6 / 12
```

Formato:

```text
Q12(a=6, b=0, c=0, d=0, E=1)
```

### √2 / 2

```text
√2 / 2 = 6√2 / 12
```

Formato:

```text
Q12(a=0, b=6, c=0, d=0, E=1)
```

### √3 / 2

```text
√3 / 2 = 6√3 / 12
```

Formato:

```text
Q12(a=0, b=0, c=6, d=0, E=1)
```

---

## Gate da supportare nella prima versione

| Gate | Comando `.q12` | Esatto |
|---|---|---|
| Reset | `RESET n` | sì |
| Pauli-X | `X q0` | sì |
| Pauli-Z | `Z q0` | sì |
| Hadamard | `H q0` | sì |
| Phase 90° | `S q0` | sì |
| T 45° | `T q0` | sì |
| Phase 30° | `P30 q0` | sì |
| Phase 60° | `P60 q0` | sì |
| CNOT | `CNOT q0 q1` | sì |
| SWAP | `SWAP q0 q1` | sì |
| Dump stato | `DUMP` | sì |
| Probabilità | `PROB` | sì |
| Misura simulata | `MEASURE q0` | pseudo-random |

---

## Gate Hadamard

Il gate Hadamard è:

```text
H = 1/√2 · [ 1   1
             1  -1 ]
```

Nel formato EXACT-Q12:

```text
1/√2 = √2 / 2 = 6√2 / 12
```

Quindi è rappresentato esattamente.

Applicazione su una coppia di ampiezze:

```text
out0 = (√2/2) · (in0 + in1)
out1 = (√2/2) · (in0 - in1)
```

---

## Gate T

Il gate T applica a `|1>` la fase 45°:

```text
e^(iπ/4) = √2/2 + i√2/2
```

Nel formato EXACT-Q12:

```text
real = 6√2 / 12
imag = 6√2 / 12
```

Quindi è esatto.

---

## Gate P30

Fase 30°:

```text
e^(iπ/6) = √3/2 + i·1/2
```

Nel formato EXACT-Q12:

```text
real = 6√3 / 12
imag = 6 / 12
```

Quindi è esatto.

---

## Gate P60

Fase 60°:

```text
e^(iπ/3) = 1/2 + i√3/2
```

Nel formato EXACT-Q12:

```text
real = 6 / 12
imag = 6√3 / 12
```

Quindi è esatto.

---

## File `.q12`

Formato circuito testuale semplice.

Esempio `bell.q12`:

```asm
RESET 2

H q0
CNOT q0 q1

DUMP
PROB
```

Risultato atteso:

```text
|00> = √2/2
|01> = 0
|10> = 0
|11> = √2/2
```

---

## CLI desiderata

La CLI deve chiamarsi:

```bash
exactq12
```

Comandi principali:

```bash
exactq12 run examples/bell.q12
exactq12 repl
exactq12 bench --qubits 8 --gates 100
exactq12 dump examples/bell.q12
exactq12 export examples/bell.q12 --format bin --out bell.bin
```

In futuro:

```bash
exactq12 fpga run examples/bell.q12 --port /dev/ttyUSB0
```

Su macOS la porta potrebbe essere simile a:

```bash
/dev/tty.usbserial-XXXX
```

---

## Output CLI

### Output simbolico

```text
|00> = (0 + 6√2 + 0√3 + 0√6) / 12 + i(0)
|01> = 0
|10> = 0
|11> = (0 + 6√2 + 0√3 + 0√6) / 12 + i(0)
```

### Output decimale solo per debug

```text
|00> ≈ 0.707106781 + i0
|01> = 0
|10> = 0
|11> ≈ 0.707106781 + i0
```

Il calcolo interno deve restare simbolico, non floating point.

---

## Struttura progetto

```text
exact-q12/
├── exactq12/
│   ├── __init__.py
│   ├── cli.py
│   ├── q12.py
│   ├── complex_q12.py
│   ├── statevector.py
│   ├── gates.py
│   ├── parser.py
│   ├── benchmark.py
│   └── fpga_uart.py
├── examples/
│   ├── bell.q12
│   ├── h2.q12
│   ├── t8.q12
│   ├── s4.q12
│   ├── p30_12.q12
│   └── p60_6.q12
├── tests/
│   ├── test_q12.py
│   ├── test_complex_q12.py
│   ├── test_gates.py
│   └── test_circuits.py
├── pyproject.toml
└── README.md
```

---

## Test matematici obbligatori

Il progetto non deve passare a FPGA finché questi test non passano.

### Test 1 — Hadamard doppio

```asm
RESET 1
H q0
H q0
DUMP
```

Risultato atteso:

```text
|0> = 1
|1> = 0
```

Verifica:

```text
H²|0> = |0>
```

---

### Test 2 — T otto volte

```asm
RESET 1
X q0
T q0
T q0
T q0
T q0
T q0
T q0
T q0
T q0
DUMP
```

Risultato atteso:

```text
|0> = 0
|1> = 1
```

Verifica:

```text
T⁸ = I
```

---

### Test 3 — S quattro volte

```asm
RESET 1
X q0
S q0
S q0
S q0
S q0
DUMP
```

Risultato atteso:

```text
|0> = 0
|1> = 1
```

Verifica:

```text
S⁴ = I
```

---

### Test 4 — P30 dodici volte

```asm
RESET 1
X q0
P30 q0
P30 q0
P30 q0
P30 q0
P30 q0
P30 q0
P30 q0
P30 q0
P30 q0
P30 q0
P30 q0
P30 q0
DUMP
```

Risultato atteso:

```text
|0> = 0
|1> = 1
```

Verifica:

```text
P30¹² = I
```

---

### Test 5 — P60 sei volte

```asm
RESET 1
X q0
P60 q0
P60 q0
P60 q0
P60 q0
P60 q0
P60 q0
DUMP
```

Risultato atteso:

```text
|0> = 0
|1> = 1
```

Verifica:

```text
P60⁶ = I
```

---

### Test 6 — Bell state

```asm
RESET 2
H q0
CNOT q0 q1
DUMP
```

Risultato atteso:

```text
|00> = √2/2
|01> = 0
|10> = 0
|11> = √2/2
```

---

## Benchmark simulato indicativo

Ipotesi:

```text
target: Tang Nano 20K
clock simulato: 50 MHz
formato: Q(√2, √3) con coefficienti 32 bit
ampiezza: 8 coefficienti x 32 bit = 256 bit = 32 byte
```

### Memoria stimata

| Qubit | Ampiezze | Memoria statevector |
|---:|---:|---:|
| 4 | 16 | 512 B |
| 8 | 256 | 8 KB |
| 10 | 1024 | 32 KB |
| 12 | 4096 | 128 KB |
| 14 | 16384 | 512 KB |
| 16 | 65536 | 2 MB |
| 17 | 131072 | 4 MB |
| 18 | 262144 | 8 MB |

La Tang Nano 20K ha circa 8 MB di SDRAM, quindi 18 qubit sono teorici e molto stretti.  
Target realistico iniziale: 2, 4, 8 qubit.

---

## Benchmark stimato per gate ottimizzati

| Qubit | H singolo | Phase/T singolo | CNOT |
|---:|---:|---:|---:|
| 8 | 15.36 µs | 10.24 µs | 5.12 µs |
| 10 | 61.44 µs | 40.96 µs | 20.48 µs |
| 12 | 245.76 µs | 163.84 µs | 81.92 µs |
| 14 | 983.04 µs | 655.36 µs | 327.68 µs |
| 16 | 3.93 ms | 2.62 ms | 1.31 ms |

Questi numeri sono solo una stima architetturale, non risultati di sintesi.

---

## Backend FPGA futuro

Il backend FPGA sarà successivo al modello Python.

Target:

```text
Tang Nano 20K
Gowin GW2AR-LV18
SystemVerilog
UART come interfaccia iniziale
niente HDMI nella prima versione
```

Formato istruzioni binarie futuro:

| Opcode | Istruzione |
|---:|---|
| `0x00` | RESET |
| `0x01` | X |
| `0x02` | Z |
| `0x03` | H |
| `0x04` | S |
| `0x05` | T |
| `0x06` | P30 |
| `0x07` | P60 |
| `0x08` | CNOT |
| `0x09` | SWAP |
| `0x0A` | DUMP |
| `0x0B` | PROB |
| `0x0C` | MEASURE |

Formato base:

```text
[opcode][arg0][arg1]
```

Esempi:

```text
H q0        = 0x03 0x00 0x00
CNOT q0 q1  = 0x08 0x00 0x01
```

---

## Modulo SystemVerilog fondamentale

Primo modulo hardware da implementare in futuro:

```systemverilog
module q12_mul #(
    parameter W = 32
)(
    input  logic signed [W-1:0] a,
    input  logic signed [W-1:0] b,
    input  logic signed [W-1:0] c,
    input  logic signed [W-1:0] d,

    input  logic signed [W-1:0] e,
    input  logic signed [W-1:0] f,
    input  logic signed [W-1:0] g,
    input  logic signed [W-1:0] h,

    output logic signed [(2*W)+3:0] A,
    output logic signed [(2*W)+3:0] B,
    output logic signed [(2*W)+3:0] C,
    output logic signed [(2*W)+3:0] D
);

    always_comb begin
        A = (a*e) + 2*(b*f) + 3*(c*g) + 6*(d*h);
        B = (a*f) + (b*e) + 3*(c*h) + 3*(d*g);
        C = (a*g) + (c*e) + 2*(b*h) + 2*(d*f);
        D = (a*h) + (d*e) + (b*g) + (c*f);
    end

endmodule
```

---

## Roadmap

### Fase 1 — Modello Python

Obiettivo:

```bash
exactq12 run examples/bell.q12
```

Deliverable:

```text
Q12
CQ12
Statevector
Gate base
Parser .q12
CLI run
Test pytest
```

---

### Fase 2 — REPL e benchmark

Obiettivo:

```bash
exactq12 repl
exactq12 bench --qubits 8 --gates 100
```

---

### Fase 3 — Export binario

Obiettivo:

```bash
exactq12 export examples/bell.q12 --format bin --out bell.bin
```

---

### Fase 4 — Backend FPGA simulato

Obiettivo:

```text
generare istruzioni compatibili con il futuro core hardware
```

---

### Fase 5 — SystemVerilog

Obiettivo:

```text
q12_mul
q12_complex_mul
statevector register file
sequencer
UART debug
```

---

### Fase 6 — Tang Nano 20K

Obiettivo minimo:

```text
RESET 2
H q0
CNOT q0 q1
DUMP
```

eseguito realmente su FPGA.

---

## Istruzioni per Codex

Prima attività per Codex:

```text
1. creare il progetto Python
2. implementare Q12
3. implementare CQ12
4. implementare statevector per 1-2 qubit
5. implementare gate H, X, Z, S, T, P30, P60, CNOT
6. creare parser .q12 minimo
7. creare CLI run/repl/bench
8. creare test pytest
9. verificare tutti i test matematici
10. non passare a FPGA finché il modello Python non è corretto
```

Vincoli:

```text
- non usare float per i calcoli interni
- il decimale è ammesso solo per stampa/debug
- tutti i gate dichiarati esatti devono restare esatti
- ogni operazione Q12 deve ridurre il denominatore quando possibile
- test obbligatori prima di aggiungere feature
- codice semplice, leggibile, modulare
```

---

## Comandi iniziali consigliati

```bash
mkdir exact-q12
cd exact-q12
codex
```

Prompt iniziale per Codex:

```text
Leggi PROJECT_CONTEXT.md e sviluppa la Fase 1 del progetto EXACT-Q12.
Prima implementa il modello Python esatto, poi i test pytest.
Non passare al backend FPGA.
```

---

## Definizione breve del progetto

**EXACT-Q12** è un simulatore quantistico esatto sperimentale che rappresenta le ampiezze non con floating point binario, ma con coefficienti simbolici in:

```text
(a + b√2 + c√3 + d√6) / 12^E
```

Il progetto è pensato prima come CLI Python verificabile e poi come possibile architettura FPGA su Tang Nano 20K.
