# Copyright (c) 2010, Tomohiro Kusumi
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from __future__ import division
import string
import sys

from . import console
from . import filebytes
from . import fileobj
from . import kbd
from . import literal
from . import methods
from . import panel
from . import screen
from . import setting
from . import terminal
from . import util

EDIT   = "EDIT"
DELETE = "DELETE"
MOTION = "MOTION"
ESCAPE = "ESCAPE"

class WriteBinaryCanvas (panel.BinaryCanvas):
    def update_highlight(self, low, range_update):
        pos = self.fileops.get_pos()
        ppos = self.fileops.get_prev_pos()
        # update previous position first
        self.chgat_posstr(ppos, screen.A_NONE)
        if self.in_same_page(pos, ppos):
            if ppos <= self.fileops.get_max_pos(): # may be false on exit edit
                b = self.fileops.read(ppos, 1)
                attr = screen.buf_attr[filebytes.ord(b)] if b else screen.A_NONE
                self.chgat_cursor(ppos, attr, attr, low)
            else:
                self.chgat_cursor(ppos, screen.A_NONE, screen.A_NONE, low)
        # update search strings before update current position
        if not self.in_same_page(pos, ppos):
            ppos = self.get_page_offset()
        if range_update:
            d = self.range_update_search(pos, ppos, pos)
        else:
            d = self.page_update_search(self.fileops.get_pos())
        # update current position
        attr1 = screen.A_COLOR_CURRENT if self.current else screen.A_STANDOUT
        b = self.fileops.read(pos, 1)
        attr2 = screen.buf_attr[filebytes.ord(b)] if b else screen.A_NONE
        if d != -1 and pos in d:
            l = d[pos] # synthesize attrs from search strings
        else:
            l = screen.A_NONE, screen.A_NONE
        self.chgat_posstr(pos, self.attr_posstr)
        self.chgat_cursor(pos, attr1 | l[0], attr2 | l[1], low)

    def update_search(self, pos, attr_bytes, here):
        if here and self.current:
            attr1 = self.attr_search | screen.A_COLOR_CURRENT
        else:
            attr1 = self.attr_search
        attr2 = self.attr_search | attr_bytes
        self.chgat_search(pos, attr1, attr2, here)
        return attr1, attr2

class Console (console.Console):
    def handle_signal(self):
        self.co.flash("Interrupted")
        return kbd.INTERRUPT

    def dispatch(self, arg):
        try:
            self.init_cursor()
            self.test()
            self.co.lrepaintf()
            self.__listen(arg)
            assert not self.co.is_barrier_active()
        except fileobj.Error as e:
            self.co.flash(e)
        finally:
            self.co.cleanup_region()
            self.cleanup_cursor() # must have called init_cursor()
            self.co.lrepaintf()
            self.set_console(None)

    def __listen(self, arg):
        if arg.start != -1:
            methods.go_to(self, arg.start)
        self.init_listen(arg)
        assert self.co.get_barrier(setting.barrier_size) != -1
        l = []
        while True:
            if arg.limit == 0:
                x = kbd.ESCAPE
                console.seqno += 1
            else:
                x = self.read_incoming()
            cmd = self.process_incoming(arg, x)
            if self.process_command(arg, x, cmd, l) == -1:
                break
            if cmd is not None:
                self.log(cmd, x)
            if setting.use_debug:
                console.set_banner(self.co.get_barrier_range())

    def init_cursor(self):
        return

    def cleanup_cursor(self):
        return

    def init_listen(self, arg):
        return

    def process_incoming(self, arg, x):
        util.raise_no_impl("process_incoming")

    def process_command(self, arg, x, cmd, l):
        util.raise_no_impl("process_command")

class WriteConsole (Console):
    def init_cursor(self):
        setting.discard_unit_based()
        self.co.open_eof_insert()

    def cleanup_cursor(self):
        self.co.close_eof_insert()
        setting.restore_unit_based()

    def init_listen(self, arg):
        self.go_right(arg.delta)

    def repaint(self, arg):
        util.raise_no_impl("repaint")

    def process_incoming(self, arg, x):
        if self.test_write(x):
            return self.handle_write(x)
        elif x in (kbd.ESCAPE, kbd.INTERRUPT):
            return self.handle_escape()
        elif x == kbd.RESIZE:
            return self.handle_resize()
        elif x == kbd.UP:
            return self.go_up()
        elif x == kbd.DOWN:
            return self.go_down()
        elif x == kbd.LEFT:
            return self.go_left()
        elif x == kbd.RIGHT:
            return self.go_right()
        elif x != kbd.ERROR:
            if not terminal.is_vtxxx(): # XXX avoid flash on vtxxx
                self.co.flash()
            return None
        else:
            return None

    def process_command(self, arg, x, cmd, l):
        if cmd == EDIT:
            if arg.limit != -1:
                arg.limit -= 1
            self.__enqueue(x, cmd, l)
        elif cmd == MOTION:
            if arg.limit > 0:
                self.co.put_barrier()
                return -1
            self.__enqueue(x, cmd, l)
        elif cmd == ESCAPE:
            if arg.limit > 0 or not l:
                self.co.put_barrier()
                return -1
            k, v = zip(*l)
            if (MOTION in k) or x == kbd.INTERRUPT:
                arg.amp = 1
            self.co.set_pos(self.co.put_barrier())
            self.co.test_access()
            if len(l) == 1:
                self.__sync(arg, arg.amp, k[0], v[0])
            else:
                self.co.disconnect_workspace()
                for x in util.get_xrange(arg.amp):
                    for i in util.get_xrange(len(l)):
                        self.__sync(arg, 1, k[i], v[i])
                self.co.reconnect_workspace()
            self.go_left()
            return -1

    def __enqueue(self, x, cmd, l):
        if cmd == EDIT:
            v = x
        elif cmd == MOTION:
            v = self.co.get_pos()
        if l and l[-1][0] == cmd:
            l[-1][1].append(v)
        else:
            l.append((cmd, [v]))

    def __sync(self, arg, n, cmd, seq):
        if cmd == EDIT:
            if self.write_buffer(n, seq) == -1:
                pfn = self.co.get_prev_context()
            else:
                pfn = None
            def fn(i):
                try:
                    self.init_cursor()
                    self.co.add_pos(arg.delta)
                    if pfn:
                        pfn(i)
                    else:
                        self.write_buffer(n, seq)
                    self.co.add_pos(-1)
                finally:
                    self.cleanup_cursor()
            self.co.set_prev_context(fn)
            if arg.merge_undo != -1:
                self.co.merge_undo_until(arg.merge_undo)
                arg.merge_undo = -1 # only first one applies
        elif cmd == MOTION:
            self.co.set_pos(seq[-1])

class DeleteConsole (Console):
    def test(self):
        try:
            methods.test_delete_raise(self)
        except fileobj.Error:
            self.co.pop_input(len(literal.delete.seq))
            raise

    def process_incoming(self, arg, x):
        for _ in literal.delete_cmds:
            if x == _:
                self.raw_delete(arg.amp)
                return DELETE
        else:
            self.co.push_input((x,))
            return ESCAPE

    def process_command(self, arg, x, cmd, l):
        if cmd == DELETE:
            l.append(arg.amp)
            arg.amp = 1 # only first delete gets amp
        elif cmd == ESCAPE:
            assert l, l # there must be at least 1 delete
            self.co.set_pos(self.co.put_barrier())
            self.co.test_access()
            self.co.disconnect_workspace()
            for x in l:
                self.delete(x)
            self.co.reconnect_workspace()
            return -1

    def delete(self, x):
        methods.delete(self, x, None, None, None)

    def raw_delete(self, x):
        methods.raw_delete(self, x, None, None, None)

class _insert (object):
    def test(self):
        methods.test_insert_raise(self)
        console.set_banner("insert")

class _replace (object):
    def test(self):
        methods.test_replace_raise(self)
        console.set_banner("replace")

_hexdigits = tuple(ord(x) for x in string.hexdigits)

class WriteBinaryConsole (WriteConsole):
    def dispatch(self, arg):
        self.low = False
        return super(WriteBinaryConsole, self).dispatch(arg)

    def test_write(self, x):
        return x in _hexdigits

    def handle_write(self, x):
        self.write(int(chr(x), 16)) # e.g. pass 10 if x is 0x41
        self.repaint(self.low)
        return EDIT

    def handle_escape(self):
        if not self.low:
            self.go_left()
        else:
            self.repaint(False)
            self.low = False
        return ESCAPE

    def handle_resize(self):
        self.co.resize()
        self.co.repaint(self.low)

    def go_up(self):
        methods.go_up(self)
        self.low = False
        return MOTION

    def go_down(self):
        methods.go_down(self)
        self.low = False
        return MOTION

    def go_right(self, n=1):
        methods.go_right(self, n)
        self.low = False
        return MOTION

    def go_left(self):
        methods.go_left(self)
        self.low = False
        return MOTION

    def write(self, x):
        self._do_write(x)
        if self.low:
            methods.go_right(self, 1)
        self.low = not self.low

    def write_buffer(self, n, seq):
        seq = seq[:]
        pad = len(seq) % 2
        if pad:
            seq.append(0x30) # '0'
        self.low = False
        ret = self._do_write_buffer(n, seq, pad)
        methods.go_right(self, ret)

class BI (WriteBinaryConsole, _insert):
    def repaint(self, arg):
        self.co.lrepaintf(arg)

    def _do_write(self, x):
        if not self.low:
            self.co.insert_current((x << 4,))
        else:
            c = self.co.read_current(1)
            self.co.replace_current((filebytes.ord(c) | x,))

    def _do_write_buffer(self, n, seq, pad):
        l = get_ascii_seq(seq) * n
        self.co.insert_current(l)
        return len(l)

class BR (WriteBinaryConsole, _replace):
    def repaint(self, arg):
        self.co.prepaintf(-1, arg)

    def _do_write(self, x):
        c = self.co.read_current(1)
        xx = filebytes.ord(c) if c else 0
        if not self.low:
            xx &= 0x0F
            self.co.replace_current(((x << 4) | xx,))
        else:
            xx &= 0xF0
            self.co.replace_current((x | xx,))

    def _do_write_buffer(self, n, seq, pad):
        seq *= n
        if pad:
            siz = len(seq) // n
            for i in util.get_xrange(siz, siz * (n + 1), siz):
                x = self.co.get_pos() + i // 2 - 1
                if x < self.co.get_size():
                    b = self.co.read(x, 1)
                else:
                    b = filebytes.ZERO
                seq[i - 1] = ord(hex(filebytes.ord(b) & 0x0F)[2:])
        l = get_ascii_seq(seq)
        self.co.replace_current(l)
        return len(l)

class RangeBR (BR):
    def write_buffer(self, n, seq):
        methods.range_replace(self, None, None, get_ascii(*seq[:2]), None)
        return -1

class BlockBR (BR):
    def write_buffer(self, n, seq):
        methods.block_replace(self, None, None, get_ascii(*seq[:2]), None)
        return -1

class WriteAsciiConsole (WriteConsole):
    def test_write(self, x):
        # include 9 to 13 -> \t\n\v\f\r
        return util.isgraph(x) or util.isspace(x)

    def handle_write(self, x):
        self.write(x)
        self.repaint(False)
        return EDIT

    def handle_escape(self):
        self.go_left()
        return ESCAPE

    def handle_resize(self):
        self.co.resize()
        self.co.repaint()

    def go_up(self):
        methods.go_up(self)
        return MOTION

    def go_down(self):
        methods.go_down(self)
        return MOTION

    def go_right(self, n=1):
        methods.go_right(self, n)
        return MOTION

    def go_left(self):
        methods.go_left(self)
        return MOTION

    def write(self, x):
        self._do_write(x)
        methods.go_right(self, 1)

    def write_buffer(self, n, seq):
        ret = self._do_write_buffer(n, seq)
        methods.go_right(self, ret)

class AI (WriteAsciiConsole, _insert):
    def repaint(self, arg):
        self.co.lrepaintf(arg)

    def _do_write(self, x):
        self.co.insert_current((x,))

    def _do_write_buffer(self, n, seq):
        l = seq * n
        self.co.insert_current(l)
        return len(l)

class AR (WriteAsciiConsole, _replace):
    def repaint(self, arg):
        self.co.prepaintf(-1, arg)

    def _do_write(self, x):
        self.co.replace_current((x,))

    def _do_write_buffer(self, n, seq):
        l = seq * n
        self.co.replace_current(l)
        return len(l)

class RangeAR (AR):
    def write_buffer(self, n, seq):
        methods.range_replace(self, None, None, seq[0], None)
        return -1

class BlockAR (AR):
    def write_buffer(self, n, seq):
        methods.block_replace(self, None, None, seq[0], None)
        return -1

def get_ascii(upper, lower):
    # e.g. 52,49 ('4','1') -> 0x41
    hex_string = chr(upper) + chr(lower)
    return int(hex_string, 16)

def get_ascii_seq(seq):
    assert len(seq) % 2 == 0
    r = util.get_xrange(0, len(seq), 2)
    return [get_ascii(*seq[i : i + 2]) for i in r]

def get_insert_class():
    return __get_class("{0}I")

def get_replace_class():
    return __get_class("{0}R")

def get_range_replace_class():
    return __get_class("Range{0}R")

def get_block_replace_class():
    return __get_class("Block{0}R")

def get_delete_class():
    return DeleteConsole

def __get_class(s):
    this = sys.modules[__name__]
    _ = 'A' if setting.use_ascii_edit else 'B'
    return getattr(this, s.format(_))

def get_input_limit():
    if not setting.use_ascii_edit: # binary
        return 2
    else:
        return 1

class Arg (util.Namespace):
    def __init__(self, **d):
        d.setdefault("amp", 1)
        d.setdefault("start", -1)
        d.setdefault("delta", 0)
        d.setdefault("limit", -1)
        d.setdefault("merge_undo", -1) # used by cw
        super(Arg, self).__init__(**d)
