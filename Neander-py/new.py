from variables import *
from functions import read_file, check_diff, translate_list, log_color
from colorama import Fore as fr, Style as st, init
import sys

init(autoreset=True)


def operação_NOP():
    None


def operação_STA(end):
    global AC, MEM, LOG
    LOG += f"{PC}.\tSTA: Stored {AC} from AC in [{end}]."
    MEM[end] = AC


def operação_LDA(end):
    global AC, MEM, LOG
    LOG += f"{PC}.\tLDA: Loaded {MEM[end]} from [{end}] to AC."
    AC = MEM[end]


def operação_ADD(end):
    global AC, MEM, LOG
    LOG += f"{PC}.\tADD: Added {MEM[end]} from [{end}] to {AC} from AC."
    AC = AC + MEM[end]


def operação_OR(end):
    global AC, MEM, LOG
    LOG += f"{PC}.\tOR: Binary operation between {AC} from AC and {MEM[end]} from [{end}]."
    AC = AC | MEM[end]


def operação_AND(end):
    global AC, MEM, LOG
    LOG += f"{PC}.\tAND: Binary operation between {AC} from AC and {MEM[end]} from [{end}]."
    AC = AC & MEM[end]


def operação_NOT():
    global AC, LOG
    LOG += f"{PC}.\tNOT: Inverted bits of {AC} from AC."
    AC = ~AC


def operação_JMP(end):
    global PC, LOG
    LOG += f"{PC}.\tJMP: Unconditional jump from ({PC}) to [{end}]."
    PC = end


def operação_JN(end):
    global AC, PC, MEM, LOG
    if AC < 0:
        LOG += f"{PC}.\tJN:  Conditional jump on negative from [{PC}] to [{end}]."
        PC = end
    else:
        LOG += f"{PC}.\tJN:  Conditional jump on negative to [{end}] failed."
        PC += 2


def operação_JZ(end):
    global AC, PC, MEM, LOG
    if AC == 0:
        LOG += f"{PC}.\tJZ:  Conditional jump on zero from [{PC}] to [{end}]."
        PC = end
    else:
        LOG += f"{PC}.\tJZ:  Conditional jump on zero to [{end}] failed."
        PC += 2


def operação_HLT():
    global PC, LOG, EXEC
    EXEC = False
    LOG += f"{PC}.\tHLT: Program halted."


def interpretador():
    global PC, MEM, LOG
    instruction = MEM[PC]
    logthis = True
    try:
        end = MEM[PC + 1]
    except:
        return
    match instruction:
        case 16:
            operação_STA(end)
            PC += 2
        case 32:
            operação_LDA(end)
            PC += 2
        case 48:
            operação_ADD(end)
            PC += 2
        case 64:
            operação_OR(end)
            PC += 2
        case 80:
            operação_AND(end)
            PC += 2
        case 96:
            operação_NOT()
            PC += 1
        case 128:
            operação_JMP(end)
        case 144:
            operação_JN(end)
        case 160:
            operação_JZ(end)
        case 240:
            operação_HLT()
        case _:
            operação_NOP()
            PC += 1
            logthis = False
    if logthis:
        last_line_length = len(LOG.rsplit("\t", 1)[-1])
        LOG += f"{' ' * (60 - last_line_length)}{' ' * (3 - len(str(AC)))}{AC}\n"
        # LOG += f"\n{' '*76}AC: {AC}\n"


def main():
    global MEM, EXEC, LOG, AC, PC
    MEM = read_file(sys.argv[1])
    MEM += [0] * (255 - len(MEM))

    MEM = translate_list(MEM)
    memory_copy = MEM.copy()

    while EXEC and PC < 256:
        interpretador()
    # print("\n", LOG, sep="", end="\n")
    print(log_color(LOG))
    print(check_diff(memory_copy, MEM))


if __name__ == "__main__":
    main()
