#pragma once

#include "gen/image.data"

#pragma inline_recursion(on)
#pragma inline_depth(255)

template <size_t N> __forceinline void
nops()
{
    if constexpr (N != 0) {
        __asm  __emit 0x90;
        nops<N - 1>();
    }
}

static char _pixel_dummy_mem[0x64];
template <size_t N, bool wide = true> __forceinline void
pixel()
{
    if constexpr (wide) {
        __asm vfmaddsub132ps xmm0, xmm1, xmmword ptr cs : [edi + esi * 4 + _pixel_dummy_mem] ;
    }
    nops<N>();
}

template <class T, size_t N>
using Arr_t = const T[N];

template <size_t H, Arr_t<size_t, H>& PVALS, bool wide = true, size_t _PTR = 0> __forceinline void
pixel_column()
{
#define JMP_0 __asm __emit 0xe9 __asm __emit 0x00 __asm __emit 0x00  __asm __emit 0x00 __asm __emit 0x00
    if constexpr (_PTR < H) {
        pixel<PVALS[_PTR], wide>();
        JMP_0;
        pixel_column<H, PVALS, wide, _PTR + 1>();
    }
#undef JMP_0
}

template<int N>
struct _pixel_padding_arr {
    constexpr _pixel_padding_arr() : arr() {
        for (auto i = 0; i != N; ++i)
            const_cast<size_t*>(arr)[i] = 25;
    }
    Arr_t<size_t, N> arr;
};

template <size_t W, size_t H, Arr_t<Arr_t<size_t, H>, W>& PVALS> void
pixel_image()
{
    unsigned int select = 0;
    __asm xor edi, edi
    __asm xor esi, esi
    __asm int 3

    static constexpr size_t padding[H] = _pixel_padding_arr<H>().arr;

    switch (select) {
#define ITER_GADGET(N) case N: pixel_column<H, PVALS[N]>(); __asm jmp end;
#define ITER_END (IMAGE_WIDTH-1)
#include "iter.x"
    case W: pixel_column<H, padding, false>(); __asm jmp end; // TODO: Make padding not so wide
    default: __asm jmp end;
    }

end:
    return;
}

template <size_t NFRAMES, size_t W, size_t H, Arr_t<Arr_t<Arr_t<size_t, H>, W>, NFRAMES>& PVALS, size_t _PTR=0> void
movie()
{
    if constexpr (_PTR < NFRAMES) {
        pixel_image<W, H, PVALS[_PTR]>();
        movie<NFRAMES, W, H, PVALS, _PTR + 1>();
    }
}
