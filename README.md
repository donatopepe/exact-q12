# EXACT-Q12

**Italiano:** simulatore quantistico sperimentale a statevector con aritmetica simbolica esatta in base 12.

**English:** experimental statevector quantum simulator using exact symbolic base-12 arithmetic.

[![tests](https://github.com/donatopepe/exact-q12/actions/workflows/tests.yml/badge.svg)](https://github.com/donatopepe/exact-q12/actions/workflows/tests.yml)
[![rtl-sim](https://github.com/donatopepe/exact-q12/actions/workflows/rtl-sim.yml/badge.svg)](https://github.com/donatopepe/exact-q12/actions/workflows/rtl-sim.yml)

Repository: <https://github.com/donatopepe/exact-q12>

License: MIT

---

## Italiano

### Scopo

EXACT-Q12 nasce per esplorare un modo alternativo di rappresentare ampiezze quantistiche senza usare floating point binario nei calcoli interni.

Il progetto implementa una CLI Python capace di simulare piccoli circuiti quantistici usando numeri esatti nel campo:

```text
Q(√2, √3)
```

Ogni numero reale interno viene rappresentato come:

```text
x = (a + b√2 + c√3 + d√6) / 12^E
```

dove `a`, `b`, `c`, `d` sono interi signed ed `E` è l'esponente del denominatore in base 12.

Un'ampiezza complessa è rappresentata come:

```text
CQ12 = real + i·imag
```

dove `real` e `imag` sono entrambi valori `Q12`.

L'obiettivo principale della prima fase è avere un modello Python semplice, verificabile e completamente esatto per un insieme controllato di gate quantistici.

### Motivazione

I simulatori quantistici classici usano quasi sempre `float`, `double` o numeri complessi floating point. Questo è efficiente, ma introduce approssimazioni numeriche.

EXACT-Q12 sceglie invece una rappresentazione simbolica che può rappresentare esattamente molti valori comuni nei circuiti quantistici didattici e sperimentali:

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

Questo permette di simulare esattamente gate come:

```text
H, X, Z, S, T, P30, P60, CNOT, SWAP
```

La base 12 non è usata come semplice formato estetico di stampa. È parte della rappresentazione interna perché rende naturali denominatori come `2`, `3`, `4`, `6` e `12`, utili per molte fasi e ampiezze.

### Cosa non è

EXACT-Q12 non è pensato per essere un simulatore quantistico universale ad alte prestazioni.

Non rappresenta esattamente rotazioni arbitrarie come:

```text
RZ 17°
RX 23°
RY arbitrario
```

Per supportarle esattamente servirebbe estendere il campo simbolico con ulteriori radicali o con una rappresentazione algebrica più generale.

### Stato del progetto

Fase attuale: **Fase 5 iniziata, primi blocchi RTL combinatori aggiunti**.

Implementato:

- `Q12`: numero reale esatto in `Q(√2, √3)` con denominatore `12^E`.
- `CQ12`: numero complesso esatto costruito da due `Q12`.
- `Statevector`: simulatore a statevector per piccoli circuiti.
- Gate: `X`, `Z`, `H`, `S`, `T`, `P30`, `P60`, `CNOT`, `SWAP`.
- Parser minimale per file `.q12`.
- CLI `exactq12 run`.
- CLI `exactq12 bench` con output JSON e log JSONL.
- CLI `exactq12 repl`, `dump`, `export` e `fpga run` simulato.
- Export binario `bin` e ROM hex `memh`.
- `fpga run` accetta stream `.bin` e ROM `.memh`.
- `state-init` genera memoria iniziale `RESET n` per `statevector_mem.sv`.
- `state-export` e `state-dump` generano e ispezionano immagini memoria statevector RTL.
- Utility Python di packing RTL per `Q12` e `CQ12`.
- Primi moduli SystemVerilog combinatori in `rtl/`.
- Blocchi RTL add/sub per `Q12` e `CQ12`, inclusa variante con allineamento limitato degli esponenti.
- Primi blocchi RTL per datapath Hadamard su coppie di ampiezze.
- Wrapper RTL Hadamard per ampiezze `CQ12` impacchettate nel layout di memoria.
- Generatore indirizzi RTL per coppie Hadamard coerente con la convenzione Python `q0` bit più significativo.
- Step RTL combinatorio per applicare Hadamard a una coppia di payload memoria già letti.
- Prime memorie RTL e sequencer fetch/decode/halt in `rtl/`.
- Top-level RTL simulativo che collega ROM, sequencer e memoria statevector.
- Testbench SystemVerilog opzionali eseguibili con Icarus Verilog.
- Esempi `.q12`.
- Test pytest per aritmetica, numeri complessi, gate, parser, CLI, benchmark e circuiti obbligatori.

Non implementato in questa fase:

- Backend FPGA reale.
- Esecuzione gate RTL completa su memoria statevector, UART e vincoli Tang Nano 20K.
- Rotazioni arbitrarie.

### Teoria numerica

Ogni valore reale è una quadrupla di coefficienti interi più un esponente:

```text
Q12(a, b, c, d, E) = (a + b√2 + c√3 + d√6) / 12^E
```

Esempi fondamentali:

```text
0      = Q12(0, 0, 0, 0, 0)
1      = Q12(1, 0, 0, 0, 0)
1/2    = Q12(6, 0, 0, 0, 1)
√2 / 2 = Q12(0, 6, 0, 0, 1)
√3 / 2 = Q12(0, 0, 6, 0, 1)
```

La riduzione del denominatore viene applicata dopo ogni costruzione di un `Q12`:

```text
se a, b, c, d sono tutti divisibili per 12 ed E > 0:
    a = a / 12
    b = b / 12
    c = c / 12
    d = d / 12
    E = E - 1
```

Questo mantiene i coefficienti più piccoli senza perdere esattezza.

### Moltiplicazione esatta

Dati:

```text
x = a + b√2 + c√3 + d√6
y = e + f√2 + g√3 + h√6
```

il prodotto è:

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

Questa formula è il cuore del progetto. Tutte le fasi e i gate esatti dipendono da questa moltiplicazione simbolica.

### Numeri complessi

Un numero complesso `CQ12` contiene due `Q12`:

```text
CQ12(real, imag) = real + i·imag
```

La moltiplicazione complessa è quella standard:

```text
(a + ib)(c + id) = (ac - bd) + i(ad + bc)
```

ma ogni operazione reale interna è una moltiplicazione `Q12` esatta.

La probabilità di un'ampiezza è calcolata come:

```text
|z|² = real² + imag²
```

Il risultato è ancora un `Q12` esatto.

### Gate supportati

I gate supportati nella Fase 1 sono:

| Gate | Sintassi `.q12` | Descrizione |
|---|---|---|
| Reset | `RESET n` | Inizializza `n` qubit nello stato `|00...0>` |
| Pauli-X | `X q0` | Flip del qubit |
| Pauli-Z | `Z q0` | Cambia segno allo stato con qubit a `1` |
| Hadamard | `H q0` | Crea sovrapposizione esatta con fattore `√2/2` |
| Phase 90° | `S q0` | Applica fase `i` |
| T 45° | `T q0` | Applica fase `√2/2 + i√2/2` |
| Phase 30° | `P30 q0` | Applica fase `√3/2 + i/2` |
| Phase 60° | `P60 q0` | Applica fase `1/2 + i√3/2` |
| CNOT | `CNOT q0 q1` | NOT sul target se il controllo è `1` |
| SWAP | `SWAP q0 q1` | Scambia due qubit |
| Dump | `DUMP` | Stampa lo statevector simbolico |
| Probabilità | `PROB` | Stampa le probabilità esatte |
| Misura | `MEASURE q0` | Misura simulata pseudo-random |

### Convenzione sugli indici dei qubit

La simulazione usa etichette binarie nello stesso ordine mostrato nel dump.

Per `RESET 2`, gli stati sono:

```text
|00>
|01>
|10>
|11>
```

`q0` è il bit più significativo, `q1` il successivo.

Quindi:

```text
RESET 2
X q0
```

porta lo stato da `|00>` a `|10>`.

### Formato `.q12`

Un circuito è un file testuale semplice.

Esempio `examples/bell.q12`:

```asm
RESET 2

H q0
CNOT q0 q1

DUMP
PROB
```

Output atteso:

```text
|00> = (0 + 6√2 + 0√3 + 0√6) / 12
|01> = 0
|10> = 0
|11> = (0 + 6√2 + 0√3 + 0√6) / 12
P(|00>) = (6 + 0√2 + 0√3 + 0√6) / 12
P(|01>) = 0
P(|10>) = 0
P(|11>) = (6 + 0√2 + 0√3 + 0√6) / 12
```

Le righe vuote sono ignorate. I commenti sono supportati con `#`.

### Installazione

Clona il repository:

```bash
git clone https://github.com/donatopepe/exact-q12.git
cd exact-q12
```

Uso diretto senza installazione:

```bash
python3 -m exactq12.cli run examples/bell.q12
```

Installazione in modalità editable:

```bash
python3 -m pip install -e .
```

Dopo l'installazione:

```bash
exactq12 run examples/bell.q12
```

Comandi principali disponibili:

```bash
exactq12 run examples/bell.q12
exactq12 repl
exactq12 bench --qubits 4 --gates 100 --repetitions 5
exactq12 dump examples/bell.q12
exactq12 export examples/bell.q12 --format bin --out bell.bin
exactq12 export examples/bell.q12 --format memh --out bell.memh
exactq12 fpga run bell.bin
exactq12 fpga run bell.memh
exactq12 state-init --qubits 2 --out reset2.memh
exactq12 state-export examples/bell.q12 --out bell_state.memh
exactq12 state-dump bell_state.memh
```

`fpga run` in questa fase è una simulazione software del formato istruzioni binarie. Non esegue codice su hardware reale e non contiene SystemVerilog.

### Esecuzione dei test

Installa `pytest` se non è già disponibile:

```bash
python3 -m pip install pytest
```

Oppure installa le dipendenze di sviluppo dichiarate dal progetto:

```bash
python3 -m pip install -e '.[dev]'
```

Esegui i test:

```bash
python3 -m pytest
```

Verifica rapida senza pytest:

```bash
python3 -m compileall exactq12 tests
python3 -m exactq12.cli run examples/bell.q12
```

### Benchmark e log

La CLI include un benchmark sintetico riproducibile per misurare il costo del modello simbolico Python. Il benchmark applica una sequenza deterministica di gate esatti allo statevector e misura il tempo con `time.perf_counter_ns`, cioè un contatore ad alta risoluzione adatto a durate brevi.

Esecuzione base:

```bash
python3 -m exactq12.cli bench --qubits 4 --gates 100 --repetitions 5
```

Output JSON:

```json
{
  "amplitudes": 16,
  "average_gate_ns": 12345,
  "average_run_ns": 1234567,
  "elapsed_ns": 6172835,
  "gates": 100,
  "max_coefficient_digits": 8,
  "platform": "macOS-...",
  "python": "3.x.y",
  "qubits": 4,
  "repetitions": 5
}
```

Il valore `max_coefficient_digits` è utile perché l'aritmetica simbolica può far crescere i coefficienti interi. Non misura solo il tempo, ma anche una parte della pressione aritmetica del circuito.

Log JSONL completo:

```bash
python3 -m exactq12.cli bench --qubits 4 --gates 100 --repetitions 5 --log-jsonl logs/bench.jsonl
python3 -m exactq12.cli run examples/bell.q12 --log-jsonl logs/bell.jsonl
```

Ogni riga del log è un oggetto JSON indipendente. Questo formato è intenzionale: è facile da leggere in streaming, importare in strumenti dati, confrontare in test di regressione e analizzare senza parser custom.

Eventi principali del benchmark:

- `benchmark_start`: parametri iniziali.
- `benchmark_repetition_start`: inizio di una ripetizione.
- `benchmark_repetition_end`: fine di una ripetizione e dimensione dei coefficienti.
- `benchmark_end`: risultato aggregato.

Eventi principali di `run`:

- `run_start`: file circuito eseguito.
- `run_end`: numero di righe prodotte.

Questi benchmark non sono confronti assoluti con simulatori floating point. Servono soprattutto per seguire regressioni interne, crescita dei coefficienti, costo dei gate e impatto di future ottimizzazioni.

### Export binario e simulazione FPGA

La Fase 3 introduce un formato binario minimale a istruzioni da 3 byte:

```text
[opcode][arg0][arg1]
```

Esempi:

```text
H q0        = 0x03 0x00 0x00
CNOT q0 q1  = 0x08 0x00 0x01
```

Opcode supportati:

| Opcode | Istruzione |
|---:|---|
| `0x00` | `RESET` |
| `0x01` | `X` |
| `0x02` | `Z` |
| `0x03` | `H` |
| `0x04` | `S` |
| `0x05` | `T` |
| `0x06` | `P30` |
| `0x07` | `P60` |
| `0x08` | `CNOT` |
| `0x09` | `SWAP` |
| `0x0A` | `DUMP` |
| `0x0B` | `PROB` |
| `0x0C` | `MEASURE` |

Export:

```bash
exactq12 export examples/bell.q12 --format bin --out bell.bin
exactq12 export examples/bell.q12 --format memh --out bell.memh
```

Simulazione software del flusso binario:

```bash
exactq12 fpga run bell.bin
exactq12 fpga run bell.memh
```

Questa simulazione valida encoder, decoder e semantica delle istruzioni prima di qualunque backend hardware reale.

Il formato `memh` scrive una istruzione a 24 bit per riga, compatibile con `rtl/program_rom.sv` e `$readmemh`:

```text
000200
030000
080001
0a0000
0b0000
```

Per inizializzare `statevector_mem.sv` con lo stato `|00...0>`:

```bash
exactq12 state-init --qubits 2 --out reset2.memh
exactq12 state-export examples/bell.q12 --out bell_state.memh
exactq12 state-dump bell_state.memh
```

### RTL SystemVerilog

La Fase 5 è iniziata con i primi blocchi combinatori in `rtl/`:

- `rtl/q12_mul.sv`: moltiplicazione del numeratore `a + b√2 + c√3 + d√6`.
- `rtl/q12_complex_mul.sv`: moltiplicazione complessa usando quattro istanze di `q12_mul`.
- `rtl/q12_den_reduce.sv`: riduzione di un passo del denominatore in base 12.
- `rtl/exactq12_pkg.sv`: costanti opcode allineate all'encoder binario Python.
- `rtl/instruction_decoder.sv`: decoder combinatorio per istruzioni `[opcode][arg0][arg1]`.
- `rtl/program_rom.sv`: ROM generica per istruzioni a 24 bit caricata con `$readmemh`.
- `rtl/statevector_mem.sv`: memoria sincrona per ampiezze `CQ12` impacchettate.
- `rtl/exactq12_sequencer.sv`: scheletro fetch/decode/halt.
- `rtl/exactq12_top.sv`: shell simulativa che collega ROM, sequencer e memoria statevector.
- `rtl/q12_add.sv`: somma/sottrazione combinatoria per `Q12` con esponenti già allineati.
- `rtl/q12_complex_add.sv`: somma/sottrazione combinatoria per `CQ12` con due istanze `q12_add`.
- `rtl/q12_add_aligned.sv`: somma/sottrazione `Q12` che scala al denominatore comune `12^max(E0,E1)` fino a `MAX_SHIFT`.
- `rtl/q12_complex_add_aligned.sv`: somma/sottrazione `CQ12` con allineamento indipendente di parte reale e immaginaria.
- `rtl/q12_scale_sqrt_half.sv`: moltiplicazione esatta per `√2/2 = 6√2/12`.
- `rtl/q12_complex_scale_sqrt_half.sv`: scaling `CQ12` per `√2/2`.
- `rtl/hadamard_pair.sv`: butterfly combinatorio `(a+b)/√2`, `(a-b)/√2` per due ampiezze.
- `rtl/hadamard_pair_packed.sv`: wrapper del butterfly su payload `CQ12` impacchettati come `statevector_mem.sv`.
- `rtl/hadamard_address_pair.sv`: calcola gli indirizzi della coppia di ampiezze per un gate `H qN`.
- `rtl/hadamard_pair_step.sv`: combina indirizzi, payload letti e risultati Hadamard per una coppia.
- `rtl/bell.memh`: programma Bell in formato ROM hex.
- `rtl/tb/`: testbench SystemVerilog auto-verificanti opzionali.
- `rtl/Makefile`: target opzionali per simulazione locale con Icarus Verilog.
- `exactq12/rtl_pack.py`: packing/unpacking Python di `Q12` e `CQ12` nel layout usato dalla memoria RTL.

Questi moduli sono volutamente piccoli e verificabili. Non implementano ancora:

- integrazione della riduzione del denominatore nel datapath completo;
- esecuzione dei gate sul datapath statevector;
- UART;
- top-level Gowin/Tang Nano 20K;
- file constraint o progetto EDA.

Il sequencer RTL attuale decodifica istruzioni e si ferma su `DUMP` o opcode non valido; il top-level collega i blocchi ma non applica ancora gate alla memoria statevector. La verifica attuale è fatta con test Python che confrontano formule, opcode, ROM e riduzione attesa contro il modello Python esatto. Questo non sostituisce una simulazione SystemVerilog con Verilator/Icarus/Gowin, ma impedisce divergenze immediate tra specifica e RTL iniziale.

Simulazione HDL locale opzionale:

```bash
make -C rtl sim
```

Richiede `iverilog` e `vvp` installati localmente. Non è richiesta dalla suite pytest locale.

La simulazione RTL è però eseguita in un workflow GitHub Actions separato (`rtl-sim.yml`) che installa Icarus Verilog su Ubuntu e lancia `make -C rtl sim`.

### Batteria di test

La suite pytest copre:

- Riduzione del denominatore `Q12`.
- Somma con allineamento degli esponenti.
- Formula esatta di moltiplicazione in `Q(√2, √3)`.
- Moltiplicazione complessa e norma `abs2`.
- Gate singoli `X`, `Z`, `H` e `SWAP`.
- Circuiti obbligatori `H²`, `T⁸`, `S⁴`, `P30¹²`, `P60⁶`, Bell state.
- Parser `.q12`, commenti, maiuscole/minuscole e errori.
- CLI `run` con log JSONL.
- CLI `bench` e serializzazione JSON del risultato.
- CLI `repl`, `dump`, `export` e `fpga run` simulato.
- Roundtrip del formato binario e validazione degli opcode.
- Export `memh` e roundtrip del packing RTL `Q12`/`CQ12`.
- Export `state-init` per memoria statevector RTL.
- Roundtrip `state-export`/`state-dump` per immagini memoria RTL.
- Formule RTL `q12_mul`, `q12_complex_mul`, opcode, decoder, ROM, memoria e riduzione denominatore confrontati con il modello Python.
- Formule RTL add/sub `q12_add`, `q12_complex_add` e varianti aligned confrontate con il modello Python.
- Formule RTL per scaling `√2/2` e butterfly Hadamard confrontate con il modello Python.
- Layout RTL del wrapper Hadamard packed verificato contro il packing `CQ12`.
- Formula indirizzi RTL per Hadamard confrontata con l'indicizzazione Python dello statevector.
- Wiring statico dello step Hadamard RTL verificato dai test.
- Wiring statico del top-level RTL verificato dai test.
- Presenza di testbench SystemVerilog auto-verificanti e Makefile RTL.
- Conservazione esatta della normalizzazione dopo sequenze di gate supportati.

Quando si aggiunge un gate, il minimo richiesto è aggiungere un test di aritmetica della fase, un test sullo statevector e un test circuito end-to-end.

### Test matematici obbligatori

La Fase 1 deve passare questi circuiti prima di procedere a qualunque backend FPGA.

1. `H` due volte deve restituire lo stato iniziale:

```asm
RESET 1
H q0
H q0
DUMP
```

2. `T` otto volte deve essere identità:

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

3. `S` quattro volte deve essere identità:

```asm
RESET 1
X q0
S q0
S q0
S q0
S q0
DUMP
```

4. `P30` dodici volte deve essere identità:

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

5. `P60` sei volte deve essere identità:

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

6. Bell state:

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

### Struttura del progetto

```text
exact-q12/
├── exactq12/
│   ├── __init__.py
│   ├── benchmark.py
│   ├── binary.py
│   ├── cli.py
│   ├── complex_q12.py
│   ├── gates.py
│   ├── logging_utils.py
│   ├── parser.py
│   ├── q12.py
│   ├── repl.py
│   ├── rtl_pack.py
│   └── statevector.py
├── examples/
│   ├── bell.q12
│   ├── h2.q12
│   ├── p30_12.q12
│   ├── p60_6.q12
│   ├── s4.q12
│   └── t8.q12
├── tests/
│   ├── test_circuits.py
│   ├── test_binary_repl.py
│   ├── test_complex_q12.py
│   ├── test_gates.py
│   ├── test_parser_cli_benchmark.py
│   ├── test_rtl.py
│   ├── test_rtl_pack.py
│   └── test_q12.py
├── rtl/
│   ├── README.md
│   ├── README_TOP.md
│   ├── Makefile
│   ├── bell.memh
│   ├── exactq12_sequencer.sv
│   ├── exactq12_top.sv
│   ├── exactq12_pkg.sv
│   ├── hadamard_address_pair.sv
│   ├── hadamard_pair.sv
│   ├── hadamard_pair_packed.sv
│   ├── hadamard_pair_step.sv
│   ├── instruction_decoder.sv
│   ├── program_rom.sv
│   ├── q12_add.sv
│   ├── q12_add_aligned.sv
│   ├── q12_complex_add.sv
│   ├── q12_complex_add_aligned.sv
│   ├── q12_complex_scale_sqrt_half.sv
│   ├── q12_complex_mul.sv
│   ├── q12_den_reduce.sv
│   ├── q12_mul.sv
│   ├── q12_scale_sqrt_half.sv
│   ├── statevector_mem.sv
│   └── tb/
├── PROJECT_CONTEXT_EXACT_Q12.md
├── pyproject.toml
├── README.md
└── LICENSE
```

### Roadmap

Fase 1, completata nel modello iniziale:

- Modello Python esatto.
- Parser `.q12`.
- CLI `run`.
- CLI `bench` con output JSON e log JSONL.
- Test matematici obbligatori.
- CI GitHub Actions su Python 3.11, 3.12 e 3.13.

Fase 2, completata nel modello iniziale:

- REPL.
- Benchmark CLI.
- Miglioramenti ergonomici della CLI.

Fase 3, completata nel modello iniziale:

- Export binario dei circuiti.
- Export ROM hex `memh` per `$readmemh`.

Fase 4, iniziata:

- Simulatore software del flusso binario con `exactq12 fpga run`.

Fase 5, iniziata:

- Moduli SystemVerilog combinatori `q12_add`, `q12_add_aligned`, `q12_complex_add`, `q12_complex_add_aligned`, `q12_scale_sqrt_half`, `q12_complex_scale_sqrt_half`, `hadamard_address_pair`, `hadamard_pair`, `hadamard_pair_packed`, `hadamard_pair_step`, `q12_mul`, `q12_complex_mul`, `q12_den_reduce` e decoder istruzioni.
- Memorie RTL iniziali e sequencer fetch/decode/halt.
- Top-level RTL simulativo non board-specific.
- Testbench SystemVerilog opzionali per Icarus Verilog.
- Futuro: esecuzione gate sul datapath statevector, UART debug, top-level Tang Nano 20K.

Fase 6, futura:

- Esecuzione su Tang Nano 20K.

### Principi di sviluppo

- I calcoli interni non devono usare floating point.
- `float` è ammesso solo per debug, stampa approssimata o misura pseudo-random.
- Ogni gate dichiarato esatto deve rimanere esatto.
- Ogni operazione `Q12` deve ridurre il denominatore quando possibile.
- Il modello Python deve rimanere la fonte di verità prima di qualsiasi backend hardware.
- Il README deve essere aggiornato quando cambiano CLI, teoria, formati, esempi o roadmap.

### Workflow di manutenzione

Prima di ogni push eseguire:

```bash
python3 -m compileall exactq12 tests
python3 -m pytest
python3 -m exactq12.cli run examples/bell.q12
python3 -m exactq12.cli bench --qubits 2 --gates 10 --repetitions 2
python3 -m exactq12.cli export examples/bell.q12 --format bin --out bell.bin
python3 -m exactq12.cli export examples/bell.q12 --format memh --out bell.memh
python3 -m exactq12.cli fpga run bell.bin
python3 -m exactq12.cli fpga run bell.memh
python3 -m exactq12.cli state-init --qubits 2 --out reset2.memh
python3 -m exactq12.cli state-export examples/bell.q12 --out bell_state.memh
python3 -m exactq12.cli state-dump bell_state.memh
```

Se si modifica `rtl/`, aggiornare anche i test in `tests/test_rtl.py` o aggiungere una simulazione HDL dedicata quando viene introdotta una toolchain.

La CI GitHub Actions esegue gli stessi controlli principali su più versioni Python. Se una modifica cambia CLI, formato `.q12`, benchmark, log o teoria, aggiornare questo README nello stesso commit.

### Possibili estensioni per inferenza IA

EXACT-Q12 non è un framework di inferenza IA. Tuttavia la rappresentazione del progetto è interessante per sperimentare inferenza numerica non-floating-point, soprattutto in contesti didattici, embedded o hardware-oriented.

Possibili direzioni:

- Inferenza integer-only: usare `Q12` come formato esatto di riferimento per verificare pipeline quantizzate con coefficienti interi.
- Golden model per acceleratori: confrontare un backend C, SIMD, FPGA o ASIC contro il modello Python esatto.
- Reti piccole simboliche: implementare layer lineari, funzioni di attivazione limitate e normalizzazioni razionali quando i pesi appartengono a un sottoinsieme rappresentabile.
- Verifica di quantizzazione: confrontare output floating point, integer-only e `Q12` per stimare errore e drift numerico.
- Inferenza quantistica ibrida: usare lo statevector esatto per circuiti quantistici piccoli integrati in pipeline classiche.

Limiti importanti:

- Le funzioni non algebriche comuni nelle reti neurali, come `exp`, `gelu`, `softmax` e molte normalizzazioni, non sono rappresentabili esattamente in `Q(√2, √3)`.
- L'aritmetica simbolica cresce più velocemente della floating point arithmetic.
- Per modelli IA grandi, `Q12` ha senso come riferimento, test oracle o formato sperimentale, non come sostituto diretto di GPU/TPU.

Una linea concreta di sviluppo potrebbe essere `exactq12.nn`, con tensori piccoli di `Q12`, layer `Linear`, attivazioni razionali semplici e confronto contro inferenza quantizzata integer-only.

### Riferimenti consultati

- Python `time`: `perf_counter_ns` è indicato per misurare intervalli brevi con contatore ad alta risoluzione.
- Python `json`: JSON è un formato di interscambio leggero e adatto a output benchmark e log JSONL.
- Python `logging`: il logging standard usa logger gerarchici e handler configurabili; EXACT-Q12 usa JSONL minimale per restare semplice e dipendenza-zero.
- IBM/Qiskit `Statevector`: riferimento terminologico per statevector, probabilità, misura e simulazione da circuiti.
- Jacob et al., “Quantization and Training of Neural Networks for Efficient Integer-Arithmetic-Only Inference”, arXiv:1712.05877: riferimento per la motivazione dell'inferenza integer-only.

---

## English

### Purpose

EXACT-Q12 is an experimental quantum statevector simulator built around exact symbolic arithmetic instead of binary floating point arithmetic.

The project implements a Python CLI that simulates small quantum circuits using exact values in the field:

```text
Q(√2, √3)
```

Every internal real number is represented as:

```text
x = (a + b√2 + c√3 + d√6) / 12^E
```

where `a`, `b`, `c`, and `d` are signed integers and `E` is the base-12 denominator exponent.

A complex amplitude is represented as:

```text
CQ12 = real + i·imag
```

where both `real` and `imag` are `Q12` values.

The main goal of Phase 1 is a simple, testable, fully exact Python model for a controlled set of quantum gates.

### Motivation

Classical quantum simulators usually use `float`, `double`, or floating point complex numbers. This is efficient, but it introduces numerical approximation.

EXACT-Q12 uses a symbolic representation that can exactly encode many values that appear in educational and experimental quantum circuits:

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

This makes the following gates exact:

```text
H, X, Z, S, T, P30, P60, CNOT, SWAP
```

Base 12 is not just a display format. It is part of the internal representation because denominators such as `2`, `3`, `4`, `6`, and `12` are natural in this system.

### What This Is Not

EXACT-Q12 is not intended to be a high-performance universal quantum simulator.

It does not exactly represent arbitrary rotations such as:

```text
RZ 17°
RX 23°
arbitrary RY
```

Exact support for these operations would require extending the symbolic field with additional radicals or switching to a more general algebraic representation.

### Project Status

Current phase: **Phase 5 started, first combinational RTL blocks added**.

Implemented:

- `Q12`: exact real number in `Q(√2, √3)` with denominator `12^E`.
- `CQ12`: exact complex number built from two `Q12` values.
- `Statevector`: exact statevector simulator for small circuits.
- Gates: `X`, `Z`, `H`, `S`, `T`, `P30`, `P60`, `CNOT`, `SWAP`.
- Minimal `.q12` parser.
- `exactq12 run` CLI command.
- `exactq12 bench` CLI command with JSON output and JSONL logs.
- `exactq12 repl`, `dump`, `export`, and simulated `fpga run` CLI commands.
- Binary `bin` and ROM hex `memh` export.
- `fpga run` accepts `.bin` streams and `.memh` ROM files.
- `state-init` generates initial `RESET n` memory for `statevector_mem.sv`.
- `state-export` and `state-dump` generate and inspect RTL statevector memory images.
- Python RTL packing utilities for `Q12` and `CQ12`.
- First combinational SystemVerilog modules in `rtl/`.
- RTL add/sub blocks for `Q12` and `CQ12`, including a variant with limited exponent alignment.
- First RTL Hadamard datapath blocks over pairs of amplitudes.
- RTL Hadamard wrapper for packed `CQ12` amplitudes using the memory layout.
- RTL Hadamard pair address generator matching the Python `q0` most-significant-bit convention.
- Combinational RTL step for applying Hadamard to one already-read memory payload pair.
- First RTL memories and fetch/decode/halt sequencer in `rtl/`.
- Simulation-oriented RTL top-level wiring ROM, sequencer, and statevector memory.
- Optional SystemVerilog testbenches runnable with Icarus Verilog.
- `.q12` examples.
- Pytest tests for arithmetic, complex numbers, gates, parser, CLI, benchmark, and required circuits.

Not implemented in this phase:

- Real FPGA backend.
- Complete RTL gate execution over statevector memory, UART, and Tang Nano 20K constraints.
- Arbitrary rotations.

### Numerical Theory

Each real value is an integer coefficient tuple plus one exponent:

```text
Q12(a, b, c, d, E) = (a + b√2 + c√3 + d√6) / 12^E
```

Core examples:

```text
0      = Q12(0, 0, 0, 0, 0)
1      = Q12(1, 0, 0, 0, 0)
1/2    = Q12(6, 0, 0, 0, 1)
√2 / 2 = Q12(0, 6, 0, 0, 1)
√3 / 2 = Q12(0, 0, 6, 0, 1)
```

Denominator reduction is applied whenever a `Q12` value is built:

```text
if a, b, c, d are all divisible by 12 and E > 0:
    a = a / 12
    b = b / 12
    c = c / 12
    d = d / 12
    E = E - 1
```

This keeps coefficients smaller without losing exactness.

### Exact Multiplication

Given:

```text
x = a + b√2 + c√3 + d√6
y = e + f√2 + g√3 + h√6
```

the product is:

```text
x · y = A + B√2 + C√3 + D√6
```

with:

```text
A = ae + 2bf + 3cg + 6dh
B = af + be + 3ch + 3dg
C = ag + ce + 2bh + 2df
D = ah + de + bg + cf
```

This formula is the core of the project. All exact phases and gates depend on it.

### Complex Numbers

A `CQ12` complex number contains two `Q12` values:

```text
CQ12(real, imag) = real + i·imag
```

Complex multiplication is standard:

```text
(a + ib)(c + id) = (ac - bd) + i(ad + bc)
```

but every internal real operation is an exact `Q12` operation.

The probability of an amplitude is:

```text
|z|² = real² + imag²
```

The result is still an exact `Q12` value.

### Supported Gates

The Phase 1 gate set is:

| Gate | `.q12` Syntax | Description |
|---|---|---|
| Reset | `RESET n` | Initializes `n` qubits to `|00...0>` |
| Pauli-X | `X q0` | Flips the qubit |
| Pauli-Z | `Z q0` | Negates states where the qubit is `1` |
| Hadamard | `H q0` | Creates exact superposition with factor `√2/2` |
| Phase 90° | `S q0` | Applies phase `i` |
| T 45° | `T q0` | Applies phase `√2/2 + i√2/2` |
| Phase 30° | `P30 q0` | Applies phase `√3/2 + i/2` |
| Phase 60° | `P60 q0` | Applies phase `1/2 + i√3/2` |
| CNOT | `CNOT q0 q1` | Applies NOT to target if control is `1` |
| SWAP | `SWAP q0 q1` | Swaps two qubits |
| Dump | `DUMP` | Prints the symbolic statevector |
| Probability | `PROB` | Prints exact probabilities |
| Measure | `MEASURE q0` | Simulated pseudo-random measurement |

### Qubit Index Convention

The simulator uses binary labels in the same order shown by `DUMP`.

For `RESET 2`, states are:

```text
|00>
|01>
|10>
|11>
```

`q0` is the most significant bit, `q1` is the next bit.

Therefore:

```text
RESET 2
X q0
```

moves the state from `|00>` to `|10>`.

### `.q12` File Format

A circuit is a simple text file.

Example `examples/bell.q12`:

```asm
RESET 2

H q0
CNOT q0 q1

DUMP
PROB
```

Expected output:

```text
|00> = (0 + 6√2 + 0√3 + 0√6) / 12
|01> = 0
|10> = 0
|11> = (0 + 6√2 + 0√3 + 0√6) / 12
P(|00>) = (6 + 0√2 + 0√3 + 0√6) / 12
P(|01>) = 0
P(|10>) = 0
P(|11>) = (6 + 0√2 + 0√3 + 0√6) / 12
```

Blank lines are ignored. Comments are supported with `#`.

### Installation

Clone the repository:

```bash
git clone https://github.com/donatopepe/exact-q12.git
cd exact-q12
```

Run directly without installation:

```bash
python3 -m exactq12.cli run examples/bell.q12
```

Install in editable mode:

```bash
python3 -m pip install -e .
```

After installation:

```bash
exactq12 run examples/bell.q12
```

Main available commands:

```bash
exactq12 run examples/bell.q12
exactq12 repl
exactq12 bench --qubits 4 --gates 100 --repetitions 5
exactq12 dump examples/bell.q12
exactq12 export examples/bell.q12 --format bin --out bell.bin
exactq12 export examples/bell.q12 --format memh --out bell.memh
exactq12 fpga run bell.bin
exactq12 fpga run bell.memh
exactq12 state-init --qubits 2 --out reset2.memh
exactq12 state-export examples/bell.q12 --out bell_state.memh
exactq12 state-dump bell_state.memh
```

At this stage, `fpga run` is a software simulation of the binary instruction format. It does not execute on real hardware and does not contain SystemVerilog.

### Running Tests

Install `pytest` if needed:

```bash
python3 -m pip install pytest
```

Or install the project development dependencies:

```bash
python3 -m pip install -e '.[dev]'
```

Run the test suite:

```bash
python3 -m pytest
```

Quick verification without pytest:

```bash
python3 -m compileall exactq12 tests
python3 -m exactq12.cli run examples/bell.q12
```

### Benchmark and Logs

The CLI includes a reproducible synthetic benchmark for measuring the symbolic Python model. The benchmark applies a deterministic sequence of exact gates to the statevector and measures elapsed time with `time.perf_counter_ns`, a high-resolution counter suitable for short durations.

Basic execution:

```bash
python3 -m exactq12.cli bench --qubits 4 --gates 100 --repetitions 5
```

JSON output:

```json
{
  "amplitudes": 16,
  "average_gate_ns": 12345,
  "average_run_ns": 1234567,
  "elapsed_ns": 6172835,
  "gates": 100,
  "max_coefficient_digits": 8,
  "platform": "macOS-...",
  "python": "3.x.y",
  "qubits": 4,
  "repetitions": 5
}
```

`max_coefficient_digits` is useful because symbolic arithmetic can increase integer coefficient size. It gives a simple signal for arithmetic pressure, not only runtime.

Full JSONL logs:

```bash
python3 -m exactq12.cli bench --qubits 4 --gates 100 --repetitions 5 --log-jsonl logs/bench.jsonl
python3 -m exactq12.cli run examples/bell.q12 --log-jsonl logs/bell.jsonl
```

Each log line is an independent JSON object. This is intentional: JSONL is easy to stream, import into data tools, compare in regression tests, and analyze without a custom parser.

Main benchmark events:

- `benchmark_start`: initial parameters.
- `benchmark_repetition_start`: start of one repetition.
- `benchmark_repetition_end`: end of one repetition and coefficient size.
- `benchmark_end`: aggregate result.

Main `run` events:

- `run_start`: circuit file being executed.
- `run_end`: number of produced output lines.

These benchmarks are not absolute comparisons against floating point simulators. They are mainly for tracking internal regressions, coefficient growth, gate cost, and future optimization impact.

### Binary Export and FPGA Simulation

Phase 3 introduces a minimal binary format with 3-byte instructions:

```text
[opcode][arg0][arg1]
```

Examples:

```text
H q0        = 0x03 0x00 0x00
CNOT q0 q1  = 0x08 0x00 0x01
```

Supported opcodes:

| Opcode | Instruction |
|---:|---|
| `0x00` | `RESET` |
| `0x01` | `X` |
| `0x02` | `Z` |
| `0x03` | `H` |
| `0x04` | `S` |
| `0x05` | `T` |
| `0x06` | `P30` |
| `0x07` | `P60` |
| `0x08` | `CNOT` |
| `0x09` | `SWAP` |
| `0x0A` | `DUMP` |
| `0x0B` | `PROB` |
| `0x0C` | `MEASURE` |

Export:

```bash
exactq12 export examples/bell.q12 --format bin --out bell.bin
exactq12 export examples/bell.q12 --format memh --out bell.memh
```

Software simulation of the binary stream:

```bash
exactq12 fpga run bell.bin
exactq12 fpga run bell.memh
```

This simulation validates encoder, decoder, and instruction semantics before any real hardware backend.

The `memh` format writes one 24-bit instruction per line, compatible with `rtl/program_rom.sv` and `$readmemh`:

```text
000200
030000
080001
0a0000
0b0000
```

To initialize `statevector_mem.sv` with the `|00...0>` state:

```bash
exactq12 state-init --qubits 2 --out reset2.memh
exactq12 state-export examples/bell.q12 --out bell_state.memh
exactq12 state-dump bell_state.memh
```

### SystemVerilog RTL

Phase 5 has started with the first combinational blocks in `rtl/`:

- `rtl/q12_mul.sv`: numerator multiplication for `a + b√2 + c√3 + d√6`.
- `rtl/q12_complex_mul.sv`: complex multiplication using four `q12_mul` instances.
- `rtl/q12_den_reduce.sv`: one-step denominator reduction by base 12.
- `rtl/exactq12_pkg.sv`: opcode constants aligned with the Python binary encoder.
- `rtl/instruction_decoder.sv`: combinational decoder for `[opcode][arg0][arg1]` instructions.
- `rtl/program_rom.sv`: generic 24-bit instruction ROM loaded with `$readmemh`.
- `rtl/statevector_mem.sv`: synchronous memory for packed `CQ12` amplitudes.
- `rtl/exactq12_sequencer.sv`: fetch/decode/halt skeleton.
- `rtl/exactq12_top.sv`: simulation shell wiring ROM, sequencer, and statevector memory.
- `rtl/q12_add.sv`: combinational add/subtract for `Q12` values with already aligned exponents.
- `rtl/q12_complex_add.sv`: combinational add/subtract for `CQ12` values using two `q12_add` instances.
- `rtl/q12_add_aligned.sv`: `Q12` add/subtract that scales to the common denominator `12^max(E0,E1)` up to `MAX_SHIFT`.
- `rtl/q12_complex_add_aligned.sv`: `CQ12` add/subtract with independent real and imaginary exponent alignment.
- `rtl/q12_scale_sqrt_half.sv`: exact multiply by `√2/2 = 6√2/12`.
- `rtl/q12_complex_scale_sqrt_half.sv`: `CQ12` scaling by `√2/2`.
- `rtl/hadamard_pair.sv`: combinational butterfly `(a+b)/√2`, `(a-b)/√2` over two amplitudes.
- `rtl/hadamard_pair_packed.sv`: butterfly wrapper over packed `CQ12` payloads matching `statevector_mem.sv`.
- `rtl/hadamard_address_pair.sv`: computes the amplitude pair addresses for an `H qN` gate.
- `rtl/hadamard_pair_step.sv`: combines addresses, read payloads, and Hadamard results for one pair.
- `rtl/bell.memh`: Bell program in ROM hex format.
- `rtl/tb/`: optional self-checking SystemVerilog testbenches.
- `rtl/Makefile`: optional local Icarus Verilog simulation targets.
- `exactq12/rtl_pack.py`: Python packing/unpacking for `Q12` and `CQ12` using the RTL memory layout.

These modules are intentionally small and easy to inspect. They do not yet implement:

- gate execution over the statevector datapath;
- UART;
- Gowin/Tang Nano 20K top-level;
- constraint files or EDA project files.

The current RTL sequencer decodes instructions and halts on `DUMP` or invalid opcodes; the top-level wires blocks together but does not yet apply gates to statevector memory. Current verification uses Python tests that compare formulas, opcodes, ROM contents, and expected reduction behavior against the exact Python model. This does not replace SystemVerilog simulation with Verilator/Icarus/Gowin, but it prevents immediate divergence between the specification and the initial RTL.

Optional local HDL simulation:

```bash
make -C rtl sim
```

This requires `iverilog` and `vvp` to be installed locally. It is not required by the local pytest suite.

RTL simulation is also run by a separate GitHub Actions workflow (`rtl-sim.yml`) that installs Icarus Verilog on Ubuntu and runs `make -C rtl sim`.

### Test Battery

The pytest suite covers:

- `Q12` denominator reduction.
- Addition with exponent alignment.
- Exact multiplication formula in `Q(√2, √3)`.
- Complex multiplication and `abs2` norm.
- Individual `X`, `Z`, `H`, and `SWAP` gates.
- Required circuits `H²`, `T⁸`, `S⁴`, `P30¹²`, `P60⁶`, Bell state.
- `.q12` parser, comments, case-insensitive opcodes, and errors.
- `run` CLI with JSONL logging.
- `bench` CLI and JSON result serialization.
- `repl`, `dump`, `export`, and simulated `fpga run` CLI commands.
- Binary format roundtrip and opcode validation.
- `memh` export and RTL `Q12`/`CQ12` packing roundtrip.
- `state-init` export for RTL statevector memory.
- `state-export`/`state-dump` roundtrip for RTL memory images.
- RTL formulas for `q12_mul`, `q12_complex_mul`, opcodes, decoder, ROM, memory, and denominator reduction compared against the Python model.
- RTL add/sub formulas for `q12_add`, `q12_complex_add`, and aligned variants compared against the Python model.
- RTL formulas for `√2/2` scaling and Hadamard butterfly compared against the Python model.
- Packed Hadamard RTL wrapper layout verified against `CQ12` packing.
- RTL Hadamard address formula compared against Python statevector indexing.
- Static RTL Hadamard step wiring verified by tests.
- Static RTL top-level wiring verified by tests.
- Presence of self-checking SystemVerilog testbenches and RTL Makefile.
- Exact normalization preservation after supported gate sequences.

When a gate is added, the minimum expected coverage is an arithmetic test for its phase, a statevector test, and an end-to-end circuit test.

### Required Mathematical Tests

Phase 1 must pass these circuits before moving to any FPGA backend.

1. Applying `H` twice must return the initial state:

```asm
RESET 1
H q0
H q0
DUMP
```

2. Applying `T` eight times must be identity:

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

3. Applying `S` four times must be identity:

```asm
RESET 1
X q0
S q0
S q0
S q0
S q0
DUMP
```

4. Applying `P30` twelve times must be identity:

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

5. Applying `P60` six times must be identity:

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

6. Bell state:

```asm
RESET 2
H q0
CNOT q0 q1
DUMP
```

Expected result:

```text
|00> = √2/2
|01> = 0
|10> = 0
|11> = √2/2
```

### Project Layout

```text
exact-q12/
├── exactq12/
│   ├── __init__.py
│   ├── benchmark.py
│   ├── binary.py
│   ├── cli.py
│   ├── complex_q12.py
│   ├── gates.py
│   ├── logging_utils.py
│   ├── parser.py
│   ├── q12.py
│   ├── repl.py
│   ├── rtl_pack.py
│   └── statevector.py
├── examples/
│   ├── bell.q12
│   ├── h2.q12
│   ├── p30_12.q12
│   ├── p60_6.q12
│   ├── s4.q12
│   └── t8.q12
├── tests/
│   ├── test_circuits.py
│   ├── test_binary_repl.py
│   ├── test_complex_q12.py
│   ├── test_gates.py
│   ├── test_parser_cli_benchmark.py
│   ├── test_rtl.py
│   ├── test_rtl_pack.py
│   └── test_q12.py
├── rtl/
│   ├── README.md
│   ├── README_TOP.md
│   ├── Makefile
│   ├── bell.memh
│   ├── exactq12_sequencer.sv
│   ├── exactq12_top.sv
│   ├── exactq12_pkg.sv
│   ├── hadamard_address_pair.sv
│   ├── hadamard_pair.sv
│   ├── hadamard_pair_packed.sv
│   ├── hadamard_pair_step.sv
│   ├── instruction_decoder.sv
│   ├── program_rom.sv
│   ├── q12_add.sv
│   ├── q12_add_aligned.sv
│   ├── q12_complex_add.sv
│   ├── q12_complex_add_aligned.sv
│   ├── q12_complex_scale_sqrt_half.sv
│   ├── q12_complex_mul.sv
│   ├── q12_den_reduce.sv
│   ├── q12_mul.sv
│   ├── q12_scale_sqrt_half.sv
│   ├── statevector_mem.sv
│   └── tb/
├── PROJECT_CONTEXT_EXACT_Q12.md
├── pyproject.toml
├── README.md
└── LICENSE
```

### Roadmap

Phase 1, completed in the initial model:

- Exact Python model.
- `.q12` parser.
- `run` CLI.
- `bench` CLI with JSON output and JSONL logs.
- Required mathematical tests.
- GitHub Actions CI on Python 3.11, 3.12, and 3.13.

Phase 2, completed in the initial model:

- REPL.
- CLI benchmark.
- CLI usability improvements.

Phase 3, completed in the initial model:

- Binary circuit export.
- ROM hex `memh` export for `$readmemh`.

Phase 4, started:

- Software simulator for the binary stream with `exactq12 fpga run`.

Phase 5, started:

- Combinational SystemVerilog modules `q12_add`, `q12_add_aligned`, `q12_complex_add`, `q12_complex_add_aligned`, `q12_scale_sqrt_half`, `q12_complex_scale_sqrt_half`, `hadamard_address_pair`, `hadamard_pair`, `hadamard_pair_packed`, `hadamard_pair_step`, `q12_mul`, `q12_complex_mul`, `q12_den_reduce`, and instruction decoder.
- Initial RTL memories and fetch/decode/halt sequencer.
- Non-board-specific simulation RTL top-level.
- Optional SystemVerilog testbenches for Icarus Verilog.
- Future: gate execution over the statevector datapath, UART debug, Tang Nano 20K top-level.

Phase 6, future:

- Execution on Tang Nano 20K.

### Development Principles

- Internal calculations must not use floating point arithmetic.
- `float` is allowed only for debug output, approximate display, or pseudo-random measurement.
- Every gate declared exact must remain exact.
- Every `Q12` operation must reduce the denominator when possible.
- The Python model remains the source of truth before any hardware backend.
- This README must be updated whenever CLI behavior, theory, formats, examples, or roadmap change.

### Maintenance Workflow

Before each push, run:

```bash
python3 -m compileall exactq12 tests
python3 -m pytest
python3 -m exactq12.cli run examples/bell.q12
python3 -m exactq12.cli bench --qubits 2 --gates 10 --repetitions 2
python3 -m exactq12.cli export examples/bell.q12 --format bin --out bell.bin
python3 -m exactq12.cli fpga run bell.bin
```

If `rtl/` changes, update `tests/test_rtl.py` as well or add dedicated HDL simulation when a toolchain is introduced.

GitHub Actions CI runs the main checks on multiple Python versions. If a change affects the CLI, `.q12` format, benchmark, logs, or theory, update this README in the same commit.

### Possible AI Inference Extensions

EXACT-Q12 is not an AI inference framework. Still, its representation is useful for experimenting with non-floating-point inference, especially in educational, embedded, or hardware-oriented contexts.

Possible directions:

- Integer-only inference: use `Q12` as an exact reference format for checking integer-coefficient quantized pipelines.
- Golden model for accelerators: compare a C, SIMD, FPGA, or ASIC backend against the exact Python model.
- Small symbolic networks: implement linear layers, restricted activations, and rational normalizations when weights belong to a representable subset.
- Quantization verification: compare floating point, integer-only, and `Q12` outputs to estimate numerical error and drift.
- Hybrid quantum inference: use the exact statevector for small quantum circuits integrated into classical pipelines.

Important limits:

- Common non-algebraic neural-network functions such as `exp`, `gelu`, `softmax`, and many normalization schemes are not exactly representable in `Q(√2, √3)`.
- Symbolic arithmetic grows faster than floating point arithmetic.
- For large AI models, `Q12` is more useful as a reference, test oracle, or experimental format than as a direct replacement for GPU/TPU inference.

A concrete development path could be `exactq12.nn`, with small `Q12` tensors, `Linear` layers, simple rational activations, and comparisons against integer-only quantized inference.

### References Consulted

- Python `time`: `perf_counter_ns` is suitable for measuring short intervals with a high-resolution counter.
- Python `json`: JSON is a lightweight interchange format suitable for benchmark output and JSONL logs.
- Python `logging`: standard logging uses hierarchical loggers and configurable handlers; EXACT-Q12 uses minimal JSONL logs to stay simple and dependency-free.
- IBM/Qiskit `Statevector`: terminology reference for statevectors, probabilities, measurement, and circuit-based simulation.
- Jacob et al., “Quantization and Training of Neural Networks for Efficient Integer-Arithmetic-Only Inference”, arXiv:1712.05877: reference motivation for integer-only inference.
