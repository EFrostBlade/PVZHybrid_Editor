# ruff: noqa: F401,F403,F405,E402,F541,E722
from keystone import *

CODE = [
    "fldz",
    "fstp dword ptr [edi+30]",
    "mov ecx,edi",
    "call 013C0032",
    "test al,al",
    "je 013C001E",
    "fld dword ptr [00679FE4]",
    "fadd dword ptr [00679498]",
    "jmp 013C0020",
    "fldz",
    "fstp dword ptr [edi+2C]",
    "fild dword ptr [edi+08]",
    "mov esi,[ebp+0C]",
    "mov edx,[ebx]",
    "push edx",
    "push 0041713F",
    "ret",
    "push 0052BEE0",
    "ret",
]

ks = Ks(KS_ARCH_X86, KS_MODE_64)

for i, line in enumerate(CODE, 1):
    try:
        encoding, count = ks.asm(line)
        print(f"Line {i}: {line}")
        print("Byte array: ", end="")
        for byte in encoding:
            print(f"{byte:02x} ", end="")
        print("\n")
    except KsError as e:
        print(f"Keystone error at line {i}: {e}")
        break
