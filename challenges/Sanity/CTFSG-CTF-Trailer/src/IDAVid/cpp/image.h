#pragma once

#include "rep.h"

#pragma inline_recursion(on)
#pragma inline_depth(255)

#define _NOP(N) __asm nop
#define NOPS(N) REPEAT(N, _NOP)

static char _pixel_dummy_mem[0x64];
#define JMP_0 __asm __emit 0xe9 __asm __emit 0x00 __asm __emit 0x00  __asm __emit 0x00 __asm __emit 0x00
#define P(N)  __asm vfmaddsub132ps xmm0, xmm1, xmmword ptr cs : [edi + esi * 4 + _pixel_dummy_mem] NOPS(N) JMP_0

#define PAD NOPS(26) JMP_0
