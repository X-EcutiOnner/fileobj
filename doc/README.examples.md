## Examples

+ Note that some commands can take *[count]* prefix, see *[List of commands](README.list_of_commands.md)* for details.

+ Note that *offset 0* of buffer means first byte of the buffer. *offset 1* is second byte.

+ Note that *sector 0* of buffer means first sector of the buffer. *sector 1* is second sector.

+ Note that sector based commands use 512 bytes sector if the buffer is not block device.

### Command line options (also see *[List of options](README.list_of_options.md)*)

+ Print help message and exit.

        $ fileobj -h

+ Print the list of available editor commands and exit.

        $ fileobj --command

+ Use read-only mode.

        $ fileobj -R

+ Use verbose status window format instead of the default one.

        $ fileobj --verbose_window

+ Use green foreground and black background color.

        $ fileobj --fg=green --bg=black

+ Print fixed *bytes per line* within an editor window.

        $ fileobj --bytes_per_line=8

+ Print fixed *bytes per window* within an editor window.

        $ fileobj --bytes_per_window=512

+ Always keep the same window size after splitting a window.

        $ fileobj --bytes_per_window=even

### Basic commands

+ Run the program with an empty buffer.

        $ fileobj

+ Run the program and then quit.

        $ fileobj
          (command):q<ENTER>

+ Run the program and discard incomplete command which has been typed after the previous command.

        $ fileobj
          (command)ttttttttt<ESC>
          (command):elhwefsdhnkfjsd<ESC>
          (command)[123456789<ESC>

### Open a file

+ Open a file *./a.out*.

        $ fileobj ./a.out

+ Open a file *./a.out* and quit the program.

        $ fileobj ./a.out
          (command):q<ENTER>

+ Open a file *./a.out* and quit the program without saving.

        $ fileobj ./a.out
          (command):q!<ENTER>

+ Open a file *./a.out* and save the buffer.

        $ fileobj ./a.out
          (command):w<ENTER>

+ Open a file *./a.out* and quit the program after saving the buffer.

        $ fileobj ./a.out
          (command):wq<ENTER>

+ Open an empty buffer and save it as *./a.out*.

        $ fileobj
          (command):w ./a.out<ENTER>

### Move a cursor

+ Open a file *./a.out* and move the cursor.

        $ fileobj ./a.out
          (command)j
          or
          (command)k
          or
          (command)h
          or
          (command)l
          or
          (command)<DOWN>
          or
          (command)<UP>
          or
          (command)<LEFT>
          or
          (command)<RIGHT>

+ Open a file *./a.out* and move the cursor to offset 0 of the buffer.

        $ fileobj ./a.out
          (command)(move the cursor)
          (command)gg

+ Open a file *./a.out* and move the cursor to the last byte of the buffer.

        $ fileobj ./a.out
          (command)G

+ Open a file *./a.out* and move the cursor to offset 1024.

        $ fileobj ./a.out
          (command)1024go

+ Open a file *./a.out* and move the cursor to the next printable character.

        $ fileobj ./a.out
          (command)w

+ Open a file *./a.out* and move the cursor to the previous printable character.

        $ fileobj ./a.out
          (command)b

+ Open a file *./a.out* and move the cursor to the next zero (\x00).

        $ fileobj ./a.out
          (command))

+ Open a file *./a.out* and move the cursor to the previous zero (\x00).

        $ fileobj ./a.out
          (command)(

+ Open a file *./a.out* and move the cursor to the next non-zero (not \x00).

        $ fileobj ./a.out
          (command)}

+ Open a file *./a.out* and move the cursor to the previous non-zero (not \x00).

        $ fileobj ./a.out
          (command){

+ Open a file *./a.out* and move the cursor to the first byte of the current line.

        $ fileobj ./a.out
          (command)(move the cursor)
          (command)0

+ Open a file *./a.out* and move the cursor to the last byte of the current line.

        $ fileobj ./a.out
          (command)$

+ Open a file *./a.out* and move the cursor forward to the next page.

        $ fileobj ./a.out
          (command)CTRL-f

+ Open a file *./a.out* and move the cursor forward for 1/2 page.

        $ fileobj ./a.out
          (command)CTRL-d

+ Open a file *./a.out* and move the cursor backward to the previous page.

        $ fileobj ./a.out
          (command)CTRL-b

+ Open a file *./a.out* and move the cursor backward for 1/2 page.

        $ fileobj ./a.out
          (command)CTRL-u

+ Open a file *./a.out* and move the cursor to offset 0x10000. The [...] syntax gets evaluated by eval(...) function in Python. If Python3 runs fileobj, [...] syntax requires 0o prefix for an octal value.

        $ fileobj ./a.out
          (command)[0x10000]go
          or
          (command)[64KiB]go
          or
          (command)65536go

+ Open a file *./a.out* and print the current buffer size and position.

        $ fileobj ./a.out
          (command)(move the cursor)
          (command)CTRL-g

### Edit a buffer

+ Open a file *./a.out* and delete a character.

        $ fileobj ./a.out
          (command)x

+ Open a file *./a.out* and delete 256 bytes.

        $ fileobj ./a.out
          (command)256x
          or
          (command)x
          (command)256.

+ Open a file *./a.out* and delete 256 bytes at offset 1024.

        $ fileobj ./a.out
          (command)1024go
          or
          (command)1024l
          then
          (command)256x

+ Open a file *./a.out* and delete 256 bytes before offset 1024.

        $ fileobj ./a.out
          (command)1024go
          or
          (command)1024l
          then
          (command)256X

+ Open a file *./a.out*, delete 256 bytes, and insert it 4 times at offset 1024 (before delete).

        $ fileobj ./a.out
          (command)256x
          (command)768go
          (command)4P

+ Open a file *./a.out*, delete 256 bytes, and replace with it 4 times at offset 1024 (before delete).

        $ fileobj ./a.out
          (command)256x
          (command)768go
          (command)4O

+ Open a file *./a.out* and yank a character.

        $ fileobj ./a.out
          (command)y

+ Open a file *./a.out* and yank 256 bytes.

        $ fileobj ./a.out
          (command)256y

+ Open a file *./a.out* and yank 256 bytes at offset 1024.

        $ fileobj ./a.out
          (command)1024go
          or
          (command)1024l
          then
          (command)256y

+ Open a file *./a.out*, yank 256 bytes, and insert it 4 times at offset 1024.

        $ fileobj ./a.out
          (command)256y
          (command)1024go
          (command)4P

+ Open a file *./a.out*, yank 256 bytes, and replace with it 4 times at offset 1024.

        $ fileobj ./a.out
          (command)256y
          (command)1024go
          (command)4O

+ Open a file *./a.out* and toggle 256 bytes (switch upper <-> lower case for alphabets).

        $ fileobj ./a.out
          (command)256~

+ Open a file *./a.out* and apply &0xAA (bitwise and 0xAA) for 256 bytes.

        $ fileobj ./a.out
          (command)256&aa

+ Open a file *./a.out* and apply |0xAA (bitwise or 0xAA) for 256 bytes.

        $ fileobj ./a.out
          (command)256|aa

+ Open a file *./a.out* and apply ^0xAA (bitwise xor 0xAA) for 256 bytes.

        $ fileobj ./a.out
          (command)256^aa

+ Open a file *./a.out* and swap byte order of 4 bytes from the current cursor.

        $ fileobj ./a.out
          (command)4sb

+ Open a file *./a.out* and enter insert edit mode to insert "\x41\x42\x43".

        $ fileobj ./a.out
          (command)i414243<ESC>
          or
          (command):set ascii<ENTER>
          (command)iABC<ESC>

+ Open a file *./a.out* and enter insert edit mode to insert "\x41\x42\x43" for 4 times.

        $ fileobj ./a.out
          (command)4i414243<ESC>
          or
          (command):set ascii<ENTER>
          (command)4iABC<ESC>

+ Open a file *./a.out* and enter append edit mode to insert "\x41\x42\x43".

        $ fileobj ./a.out
          (command)a414243<ESC>
          or
          (command):set ascii<ENTER>
          (command)aABC<ESC>

+ Open a file *./a.out* and enter append edit mode to insert "\x41\x42\x43" for 4 times.

        $ fileobj ./a.out
          (command)4a414243<ESC>
          or
          (command):set ascii<ENTER>
          (command)4aABC<ESC>

+ Open a file *./a.out* and enter replace edit mode to replace with "\x41\x42\x43".

        $ fileobj ./a.out
          (command)R414243<ESC>
          or
          (command):set ascii<ENTER>
          (command)RABC<ESC>

+ Open a file *./a.out* and enter replace edit mode to replace with "\x41\x42\x43" for 4 times.

        $ fileobj ./a.out
          (command)4R414243<ESC>
          or
          (command):set ascii<ENTER>
          (command)4RABC<ESC>

### Rotate a buffer contents

+ Open an empty buffer and fill in the first 512 bytes with a pattern of "\x55\xaa" and save it as *./a.img*.

        $ fileobj
          (command)256i55aa<ESC>
          (command):wq ./a.img<ENTER>

+ Open above *./a.img* and overwrite the first 4 bytes with "\x7fELF".

        $ fileobj ./a.img
          (command)R7f454c46<ESC>
          or
          (command)R7f<ESC>
          (command):set ascii<ENTER>
          (command)l
          (command)RELF<ESC>

+ Open above *./a.img* and rotate the whole buffer 1 bit to right and then restore.

        $ fileobj ./a.img
          (command)>>
          (command)G
          (command)<<

+ Open above *./a.img* and rotate the whole buffer 8 bits (1 byte) to right.

        $ fileobj ./a.img
          (command)8>>

+ Open above *./a.img* and rotate the whole buffer 8 bits (1 byte) to left.

        $ fileobj ./a.img
          (command)G
          (command)8<<

### Undo a buffer

+ Open a file *./a.out* and undo.

        $ fileobj ./a.out
          (command)(do some edit)
          (command)u

+ Open a file *./a.out* and undo all.

        $ fileobj ./a.out
          (command)(do some edit)
          (command)U

+ Open a file *./a.out* and redo.

        $ fileobj ./a.out
          (command)(do some edit)
          (command)(do undo)
          (command)CTRL-r

### Search a buffer

+ Open a file *./a.out* and search forward for "GNU".

        $ fileobj ./a.out
          (command)/GNU<ENTER>

+ Open a file *./a.out* and search forward (backward if the previous search was backward) for the next.

        $ fileobj ./a.out
          (command)n

+ Open a file *./a.out* and search backward for "GNU".

        $ fileobj ./a.out
          (command)?GNU<ENTER>

+ Open a file *./a.out* and search backward (forward if the previous search was backward) for the next.

        $ fileobj ./a.out
          (command)N

+ Open a file *./a.out* and search for "\x7fELF" (can not search for ascii string in "\x??\x??.." or "\X??.." format).

        $ fileobj ./a.out
          (command)/\x7fELF<ENTER>
          or
          (command)/\x7f\x45\x4c\x46<ENTER>
          or
          (command)/\X7f454c46<ENTER>

+ Open a file *./a.out* and search for "\x41\x42\x43" (can not search for ascii string in "\x??\x??.." or "\X??.." format).

        $ fileobj ./a.out
          (command)/\x41\x42\x43<ENTER>
          or
          (command)/\X414243<ENTER>
          or
          (command)/ABC<ENTER>

### Mark a buffer

+ Open a file *./a.out*, move the cursor to offset 1024, and mark that offset as 'a'.

        $ fileobj ./a.out
          (command)1024go
          (command)ma

+ Open a file *./a.out* and jump to above mark 'a'.

        $ fileobj ./a.out
          (command)`a

### Partially open a file

+ Open a file *./a.out* from offset 1024.

        $ fileobj ./a.out@1024
        or
        $ fileobj ./a.out@0x400
        or
        $ fileobj ./a.out@02000

+ Open a file *./a.out* and read 512 bytes from offset 1024.

        $ fileobj ./a.out@1024:512
        or
        $ fileobj ./a.out@0x400:512
        or
        $ fileobj ./a.out@0x400-0x600

+ Open a file *./a.out* and read the first 1024 bytes.

        $ fileobj ./a.out@0:1024
        or
        $ fileobj ./a.out@0-1024
        or
        $ fileobj ./a.out@:1024
        or
        $ fileobj ./a.out@-1024
        or
        $ fileobj ./a.out@:0x400
        or
        $ fileobj ./a.out@-0x400

### Multiple files

+ Open a file *./a.out* and close the buffer.

        $ fileobj ./a.out
          (command):bdelete<ENTER>

+ Open an empty buffer and then open *./a.out*.

        $ fileobj
          (command):e ./a.out<ENTER>

+ Open a file *./a.out* and then open a file */path/to/b.out*.

        $ fileobj ./a.out
          (command):e /path/to/b.out<ENTER>

+ Open files *./a.out* and *./b.out*.

        $ fileobj ./a.out ./b.out

+ Open files *./a.out* and *./b.out*, and switch the buffer to *./b.out*.

        $ fileobj ./a.out ./b.out
          (command)<TAB>
          or
          (command):bnext<ENTER>

+ Open files *./a.out* and *./b.out* with different offset/length for each.

        $ fileobj ./a.out@0x400:0x200 ./b.out@:4096

### Multiple windows

+ Open files *./a.out* and *./b.out*, and start with horizontally splitted windows assigned for each buffer.

        $ fileobj ./a.out ./b.out -o

+ Open files *./a.out* and *./b.out*, and start with vertically splitted windows assigned for each buffer.

        $ fileobj ./a.out ./b.out -O

+ Open files *./a.out*, *./b.out*, *./c.out* with 3 windows, and move to the next window.

        $ fileobj ./a.out ./b.out ./c.out -o
          (command)CTRL-W w

+ Open files *./a.out*, *./b.out*, *./c.out* with 3 windows, and close all windows except for the current window.

        $ fileobj ./a.out ./b.out ./c.out -o
          (command)CTRL-W o
          or
          (command):only<ENTER>

+ Open files *./a.out*, *./b.out*, *./c.out* and print the list of buffers.

        $ fileobj ./a.out ./b.out ./c.out
          (command):args<ENTER>
          or
          (command):ls<ENTER>

+ Open a file *./a.out* and open (split) another window.

        $ fileobj ./a.out
          (command)CTRL-W s
          or
          (command):split<ENTER>

+ Open a file *./a.out* and open (split) another window and then close it.

        $ fileobj ./a.out
          (command)(split window)
          then
          (command)CTRL-W c
          or
          (command):close<ENTER>

### Visual mode

+ Open a file *./a.out* and enter visual mode.

        $ fileobj ./a.out
          (command)v
          and press escape or CTRL-c or v to exit
          (command)<ESC>

+ Open a file *./a.out* and enter line visual mode.

        $ fileobj ./a.out
          (command)V
          and press escape or CTRL-c or V to exit
          (command)<ESC>

+ Open a file *./a.out* and enter block visual mode (also see *[Notes](README.notes.md)*).

        $ fileobj ./a.out
          (command)CTRL-v
          and press escape or CTRL-c or CTRL-v to exit
          (command)<ESC>

+ Open a file *./a.out* and delete visually selected region.

        $ fileobj ./a.out
          (command)v
          or
          (command)V
          or
          (command)CTRL-v
          then
          (command)(move the cursor)
          then
          (command)x

+ Open a file *./a.out* and yank visually selected region.

        $ fileobj ./a.out
          (command)v
          or
          (command)V
          or
          (command)CTRL-v
          then
          (command)(move the cursor)
          then
          (command)y

+ Open a file *./a.out* and replace visually selected region with \xff.

        $ fileobj ./a.out
          (command)v
          or
          (command)V
          or
          (command)CTRL-v
          then
          (command)(move the cursor)
          then
          (command)rff

+ Open a file *./a.out* and rotate visually selected region.

        $ fileobj ./a.out
          (command)v
          or
          (command)V
          or
          (command)CTRL-v
          then
          (command)(move the cursor)
          then
          (command)>>

### Set editor options (also see *[List of commands](README.list_of_commands.md)*)

+ Set binary edit mode (unset ascii edit mode, default).

        $ fileobj ./a.out
          (command):set binary<ENTER>

+ Set ascii edit mode (unset binary edit mode).

        $ fileobj ./a.out
          (command):set ascii<ENTER>

+ Set *bytes per line* to the specified number, "max", "min" or "auto".

        $ fileobj ./a.out
          (command):set bytes_per_line 8<ENTER>
          or
          (command):set bpl 8<ENTER>

+ Set *bytes per window* to the specified number, "even" or "auto".

        $ fileobj ./a.out
          (command):set bytes_per_window 512<ENTER>
          or
          (command):set bpw 512<ENTER>

+ Ignore the case of alphabets on search.

        $ fileobj ./a.out
          (command):set ic<ENTER>

+ Unset above ic mode (default).

        $ fileobj ./a.out
          (command):set noic<ENTER>

+ Search wrap around the end of the buffer (default).

        $ fileobj ./a.out
          (command):set ws<ENTER>

+ Unset above ws mode.

        $ fileobj ./a.out
          (command):set nows<ENTER>

### Block device

+ Open a loop device */dev/loop0* on Linux.

        $ sudo fileobj /dev/loop0

+ Open the first 512 bytes of a block device */dev/sdb* on Linux.

        $ sudo fileobj /dev/sdb@:512
          or
        $ sudo fileobj /dev/sdb@:0x200

+ Open the first 512 bytes of a block device */dev/sdb* and zero clear that.

        $ sudo fileobj /dev/sdb@:512
          (command)v
          (command)G
          (command)r00

+ Open a block device */dev/sdb* and move the cursor to offset 320 MiB.

        $ sudo fileobj /dev/sdb
          (command)335544320go
          or
          (command)[320MiB]go
          or
          (command)[327680KiB]go

+ Open a block device */dev/sdb* and print sector size.

        $ sudo fileobj /dev/sdb
          (command):sector<ENTER>

+ Open a block device */dev/sdb* and print the current buffer size and position in sector.

        $ sudo fileobj /dev/sdb
          (command)(move the cursor)
          (command)gCTRL-g

+ Open a block device */dev/sdb* and move the cursor to the previous sector. If currently not at the beginning of the sector, move to the beginning of the current sector. This is sector based version of `h`.

        $ sudo fileobj /dev/sdb
          (command)sh

+ Open a block device */dev/sdb* and move the cursor to the next sector. This is sector based version of `l`.

        $ sudo fileobj /dev/sdb
          (command)sl

+ Open a block device */dev/sdb* and move the cursor to sector 128. This is sector based version of `go`.

        $ sudo fileobj /dev/sdb
          (command)128sgo

+ Open a block device */dev/sdb* and move the cursor to the first byte of the current sector. This is sector based version of `0`.

        $ sudo fileobj /dev/sdb
          (command)s0

+ Open a block device */dev/sdb* and move the cursor to the last byte of the current sector. This is sector based version of `$`.

        $ sudo fileobj /dev/sdb
          (command)s$

### Address space of a user process (experimental and platform specific feature)

+ Prepare a test program *test1* which continues to print "ABCDEFGHIJKLMNOPQRSTUVWXYZ".

        # uname
        Linux
        # cat > ./test1.c << EOF
        > #include <stdio.h>
        > #include <unistd.h>
        > const char *p = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
        > int main(void) {
        > while (1) {
        > printf("%s\n", p);
        > sleep(10);
        > }
        > return 0;
        > }
        > EOF
        # gcc -Wall -g ./test1.c -o test1
        # ./test1
        ABCDEFGHIJKLMNOPQRSTUVWXYZ
        ABCDEFGHIJKLMNOPQRSTUVWXYZ
        ABCDEFGHIJKLMNOPQRSTUVWXYZ
        ABCDEFGHIJKLMNOPQRSTUVWXYZ
        ABCDEFGHIJKLMNOPQRSTUVWXYZ
        ABCDEFGHIJKLMNOPQRSTUVWXYZ
        ABCDEFGHIJKLMNOPQRSTUVWXYZ
        ABCDEFGHIJKLMNOPQRSTUVWXYZ
        ...

+ Modify .rodata section while running *test1*.

        # objdump -s -j .rodata ./test1
        
        ./test1:     file format elf64-x86-64
        
        Contents of section .rodata:
         400618 01000200 00000000 00000000 00000000  ................
         400628 41424344 45464748 494a4b4c 4d4e4f50  ABCDEFGHIJKLMNOP
         400638 51525354 55565758 595a00             QRSTUVWXYZ.
        # pgrep -l test1
        8549 test1
        # fileobj pid8549@0x400628:26
          (command)26~
          (command):wq<ENTER>

+ *test1* starts to print "abcdefghijklmnopqrstuvwxyz".

        ...
        ABCDEFGHIJKLMNOPQRSTUVWXYZ
        ABCDEFGHIJKLMNOPQRSTUVWXYZ
        abcdefghijklmnopqrstuvwxyz <- .rodata section overwritten in lower case
        abcdefghijklmnopqrstuvwxyz
        abcdefghijklmnopqrstuvwxyz
        abcdefghijklmnopqrstuvwxyz
        abcdefghijklmnopqrstuvwxyz
        abcdefghijklmnopqrstuvwxyz
        ^C

+ If *test1* was executed via absolute path (i.e. */path/to/test1*), *@objdump[section]* syntax can be used to open the entire .rodata section.

        # fileobj pid8549@objdump.rodata
          (command)/A<ENTER>
          (command)26~
          (command):wq<ENTER>

### Extensions

+ Extensions open a new buffer in text only representation.

#### :extensions extension

+ Open a list of extensions buffer.

        $ fileobj
          (command):extensions<ENTER>

#### :help extension

+ Open a usage buffer.

        $ fileobj
          (command):help<ENTER>

#### :cstruct extension

+ Define a C struct *test1* in *${HOME}/.fileobj/cstruct*.

        $ cat > ~/.fileobj/cstruct << EOF
        > struct test1 {
        > char s[4];
        > u16 a;
        > s16 b;
        > u32 c;
        > s64 d;
        > string s[32];
        > };
        > EOF

+ Open a buffer */path/to/data* which contains the data in interest.

        $ fileobj /path/to/data

+ Open a :cstruct buffer which maps data to the C struct *test1*. The source data starts from current cursor position, which is 0 in this case. The C struct must be defined in *${HOME}/.fileobj/cstruct*, unless the file path is specified in the first argument before the C struct name.

        $ fileobj /path/to/data
          (command):cstruct test1<ENTER>

+ Save :cstruct buffer it as *./test1.out*.

        ...
          (command):wq ./test1.out<ENTER>
        $ cat ./test1.out
        struct test1 {
            char s[0]; 127 \x7F [.]
            char s[1]; 69 \x45 [E]
            char s[2]; 76 \x4C [L]
            char s[3]; 70 \x46 [F]
            u16 a; 258 \x02\x01 [..]
            s16 b; 1 \x01\x00 [..]
            u32 c; 0 \x00\x00\x00\x00 [....]
            s64 d; 17451457145995264 \x00\x00\x00\x00\x02\x00\x3E\x00 [......>.]
            string s[32]; "\x01"
        };

+ Another example using a predefined example in *fileobj/script/cstruct/usb*.

        $ cd /path/to/fileobj/source
        $ cp ./script/cstruct/usb ~/.fileobj/cstruct
        $ cd /path/to/somewhere
        $ od -tx1 -Ax ./usb_device_descriptor.bin
        000000 12 01 00 03 09 00 03 09 6b 1d 03 00 06 02 03 02
        000010 01 01
        000012
        $ fileobj ./usb_device_descriptor.bin
          (command):cstruct usb_device_descriptor<ENTER>
          (command):wq ./usb_device_descriptor.out<ENTER>
        $ cat ./usb_device_descriptor.out
        struct usb_device_descriptor {
            struct usb_descriptor_header {
                u8 bLength; 18 \x12 [.]
                u8 bDescriptorType; 1 \x01 [.]
            } hdr;
            x16le bcdUSB; 0x0300 \x00\x03 [..]
            u8 bDeviceClass; 9 \x09 [.]
            u8 bDeviceSubClass; 0 \x00 [.]
            u8 bDeviceProtocol; 3 \x03 [.]
            u8 bMaxPacketSize0; 9 \x09 [.]
            x16le idVendor; 0x1D6B \x6B\x1D [k.]
            x16le idProduct; 0x0003 \x03\x00 [..]
            x16le bcdDevice; 0x0206 \x06\x02 [..]
            u8 iManufacturer; 3 \x03 [.]
            u8 iProduct; 2 \x02 [.]
            u8 iSerialNumber; 1 \x01 [.]
            u8 bNumConfigurations; 1 \x01 [.]
        };
