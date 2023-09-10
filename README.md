# Mano Microprogram Simulator
> An assembler and hardware simulator for the Mano Basic Computer which uses Microprogram architecture.
 
This is a Python application that writes microprogram codes into microprogram memory and then compiles assembly code for
runs and simulation of Mano's Computer.

## Usage
1. Install Python Programming Language 
2. Install PyQt6 via this command:
   ```sh
   $ pip install -r requirements.txt
   ```
3. Run via Python Interpreter
    ```sh
   $ python main.py
   ```
## Example
For example if you want to write a sub program you can add this code to program text field
```
ORG 0
LDA X I
SUB Y
STORE RES
HLT
X, HEX 10
Y, DEC 5
RES, DEC 0
ORG 10
DEC 20
END
```
and as you can see, a Compilation Error occurs, because there is no command called `SUB` and `LDA`.

To fix this you need to add `SUB` and `LDA` command into microprogram memory by adding this code:
```
ORG 20
SUB: NOP I CALL INDRCT
READ U JMP NEXT
SUB U JMP FETCH
ORG 24
LDA: NOP I CALL INDRCT
READ U JMP NEXT
DRTAC U JMP FETCH
```
and then press write button to write this code in memory.
Now back to Program tab and compile again first and then press run button.

You can see the result in `RES` cell which is `HEX F` = `20 - 5 = 15`.
