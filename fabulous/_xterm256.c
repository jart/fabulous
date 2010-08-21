/**
 * Optimized Code For Quantizing Colors to xterm256
 *
 * These functions are equivalent to the ones found in xterm256.py but
 * orders of a magnitude faster and should compile quickly (fractions
 * of a second) on most systems with very little risk of
 * complications.
 *
 * Color quantization is very complex.  This works by treating RGB
 * values as 3D euclidean space and brute-force searching for the
 * nearest neighbor.
 */

typedef struct {
        int r;
        int g;
        int b;
} rgb_t;

int CUBE_STEPS[] = { 0x00, 0x5F, 0x87, 0xAF, 0xD7, 0xFF };
rgb_t BASIC16[] = { {   0,   0,   0 }, { 205,   0,   0}, {   0, 205,   0 },
		    { 205, 205,   0 }, {   0,   0, 238}, { 205,   0, 205 },
		    {   0, 205, 205 }, { 229, 229, 229}, { 127, 127, 127 },
		    { 255,   0,   0 }, {   0, 255,   0}, { 255, 255,   0 },
		    {  92,  92, 255 }, { 255,   0, 255}, {   0, 255, 255 },
		    { 255, 255, 255 } };
rgb_t COLOR_TABLE[256];


rgb_t xterm_to_rgb(int xcolor)
{
        rgb_t res;
        if (xcolor < 16) {
                res = BASIC16[xcolor];
        } else if (16 <= xcolor && xcolor <= 231) {
                xcolor -= 16;
                res.r = CUBE_STEPS[(xcolor / 36) % 6];
                res.g = CUBE_STEPS[(xcolor / 6) % 6];
                res.b = CUBE_STEPS[xcolor % 6];
        } else if (232 <= xcolor && xcolor <= 255) {
                res.r = res.g = res.b = 8 + (xcolor - 232) * 0x0A;
        }
        return res;
}

/**
 * This function provides a quick and dirty way to serialize an rgb_t
 * struct to an int which can be decoded by our Python code using
 * ctypes.
 */
int xterm_to_rgb_i(int xcolor)
{
        rgb_t res = xterm_to_rgb(xcolor);
        return (res.r << 16) | (res.g << 8) | (res.b << 0);
}

#define sqr(x) ((x) * (x))

/**
 * Quantize RGB values to an xterm 256-color ID
 */
int rgb_to_xterm(int r, int g, int b)
{
        int best_match = 0;
        int smallest_distance = 1000000000;
        int c, d;
        for (c = 16; c < 256; c++) {
                d = sqr(COLOR_TABLE[c].r - r) +
                    sqr(COLOR_TABLE[c].g - g) +
                    sqr(COLOR_TABLE[c].b - b);
                if (d < smallest_distance) {
                        smallest_distance = d;
                        best_match = c;
                }
        }
        return best_match;
}

/* int rgb_to_xterm(int r, int g, int b) */
/* { */
/*         int best_match = 0; */
/*         int smallest_distance = 1000000000; */
/*         int c, d; */
/*         for (c = 0; c < 16; c++) { */
/*                 d = sqr(BASIC16[c].r - r) + */
/* 			sqr(BASIC16[c].g - g) + */
/* 			sqr(BASIC16[c].b - b); */
/*                 if (d < smallest_distance) { */
/*                         smallest_distance = d; */
/*                         best_match = c; */
/*                 } */
/*         } */
/*         return best_match; */
/* } */

int init()
{
        int c;
        for (c = 0; c < 256; c++) {
		COLOR_TABLE[c] = xterm_to_rgb(c);
	}
        return 0;
}
