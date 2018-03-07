# Copyright (c) 2010-2016, Tomohiro Kusumi
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

from . import console
from . import edit
from . import extension
from . import panel
from . import screen
from . import util
from . import virtual
from . import visual
from . import void
from . import window

BUILD_FAILED = -1
BUILD_RETRY  = -2

class Workspace (object):
    def __init__(self, bpl):
        self.__bpl = 1
        self.set_bytes_per_line(bpl)
        assert self.__bpl >= 1, self.__bpl
        self.__windows = ()
        self.__fileopss = []
        self.__consoles = []
        self.__vwindows = {}
        self.__bwindows = {}
        self.__twindows = {}
        self.__swindows = {}
        self.__cur_fileops = None
        self.__cur_console = None
        self.__set_window(None)
        self.__def_vwindow, \
        self.__def_bwindow, \
        self.__def_twindow, \
        self.__def_swindow \
        = self.__windows

    def __getattr__(self, name):
        if name == "_Workspace__cur_fileops":
            raise AttributeError(name)
        return getattr(self.__cur_fileops, name)

    def __len__(self):
        return len(self.__windows)

    def dispatch(self):
        return -1

    def __set_buffer(self, o):
        self.__cur_fileops = o
        self.set_console(None, None)

    def set_console(self, con, arg):
        if isinstance(con, console.Console):
            self.__cur_console = con
        else:
            i = self.__fileopss.index(self.__cur_fileops)
            self.__cur_console = self.__consoles[i]
        self.__set_window(self.__cur_console)
        for o in self.__windows:
            o.set_buffer(self.__cur_fileops)
        def dispatch():
            return self.__cur_console.dispatch(arg)
        self.dispatch = dispatch

    def __set_window(self, con):
        # virtual window comes first
        if isinstance(con, console.Console):
            cls = util.get_class(con)
        else:
            cls = console.get_default_class()
        self.__windows = \
            self.__get_virtual_window(cls), \
            self.__get_binary_window(cls), \
            self.__get_text_window(cls), \
            self.__get_status_window(cls)

    def disconnect_window(self):
        # only leave virtual window to disable repaint
        self.__windows = self.__windows[0],

    def reconnect_window(self):
        # bring back windows of current console
        self.__set_window(self.__cur_console)

    def clone(self):
        ret = Workspace(self.__bpl)
        for i, o in enumerate(self.__fileopss):
            # do shallow copy, but don't use copy.copy()
            ret.add_buffer(i, o.clone(), self.__consoles[i])
        return ret

    def add_buffer(self, i, fop, con):
        self.__fileopss.insert(i, fop)
        self.__consoles.insert(i, con)
        if len(self.__fileopss) == 1:
            self.__set_buffer(fop)

    def remove_buffer(self, i):
        o = self.__fileopss[i]
        i = self.__fileopss.index(o)
        if self.__cur_fileops == o:
            if i == len(self.__fileopss) - 1:
                self.switch_to_prev_buffer()
            else:
                self.switch_to_next_buffer()
        self.__fileopss.remove(self.__fileopss[i])
        self.__consoles.remove(self.__consoles[i])

    def switch_to_buffer(self, i):
        self.__set_buffer(self.__fileopss[i])

    def switch_to_first_buffer(self):
        self.__set_buffer(self.__fileopss[0])

    def switch_to_last_buffer(self):
        self.__set_buffer(self.__fileopss[-1])

    def switch_to_next_buffer(self):
        if len(self.__fileopss) > 1:
            i = self.__fileopss.index(self.__cur_fileops)
            if i >= len(self.__fileopss) - 1:
                o = self.__fileopss[0]
            else:
                o = self.__fileopss[i + 1]
            self.__set_buffer(o)

    def switch_to_prev_buffer(self):
        if len(self.__fileopss) > 1:
            i = self.__fileopss.index(self.__cur_fileops)
            if i <= 0:
                o = self.__fileopss[len(self.__fileopss) - 1]
            else:
                o = self.__fileopss[i - 1]
            self.__set_buffer(o)

    def iter_buffer(self):
        for o in self.__fileopss:
            yield o

    def get_build_size(self):
        return self.get_height(), self.get_width()

    def get_height(self):
        bin_hei = self.__def_bwindow.get_size_y()
        tex_hei = self.__def_twindow.get_size_y()
        sta_hei = self.__def_swindow.get_size_y()
        sta_hei_ = self.__get_status_window_height()
        # screen size may change before build() while resizing
        if not screen.test_soft_resize():
            assert bin_hei == tex_hei, (bin_hei, tex_hei)
            assert sta_hei == sta_hei_, (sta_hei, sta_hei_)
        return bin_hei + sta_hei

    def get_width(self):
        bin_wid = self.__def_bwindow.get_size_x()
        tex_wid = self.__def_twindow.get_size_x()
        sta_wid = self.__def_swindow.get_size_x()
        ret = bin_wid + tex_wid
        # screen size may change before build() while resizing
        if not screen.test_soft_resize():
            assert ret == sta_wid, (bin_wid, tex_wid, sta_wid)
        return ret

    def __get_status_window_class(self):
        return panel.get_status_canvas_class(), panel.get_status_frame_class()

    def __get_status_window_height(self):
        return window.get_status_window_height(
            *self.__get_status_window_class())

    # horizontal split (default)
    def build_dryrun_delta(self, hei_delta, beg_delta):
        hei = self.__def_twindow.get_size_y() + self.__def_swindow.get_size_y()
        beg = self.__def_bwindow.get_position_y()
        return self.build_dryrun(hei + hei_delta, beg + beg_delta)

    def build_dryrun(self, hei, beg):
        sta_hei = self.__get_status_window_height()
        min_hei = window.get_min_binary_window_height() + sta_hei
        return self.__test_build(hei, beg, min_hei)

    def build(self, hei, beg):
        sta_hei = self.__get_status_window_height()
        self.__build(hei, beg, sta_hei)
        return hei

    def build_fixed_size_dryrun(self, lpw, beg):
        sta_hei = self.__get_status_window_height()
        hei = window.get_min_binary_window_height(lpw) + sta_hei
        min_hei = window.get_min_binary_window_height() + sta_hei
        return self.__test_build(hei, beg, min_hei)

    def build_fixed_size(self, lpw, beg):
        sta_hei = self.__get_status_window_height()
        hei = window.get_min_binary_window_height(lpw) + sta_hei
        self.__build(hei, beg, sta_hei)
        return hei

    def __test_build(self, hei, beg, min_hei):
        scr_hei = screen.get_size_y()
        scr_wid = screen.get_size_x()
        if hei <= 0:
            return BUILD_FAILED
        if beg < 0:
            return BUILD_FAILED
        if scr_hei < min_hei: # screen height < minimum workspace height
            return BUILD_FAILED
        if hei < min_hei: # height < minimum workspace height
            return BUILD_FAILED
        if hei > scr_hei: # height > screen height
            return BUILD_FAILED
        if beg + hei >= scr_hei: # this workspace exceeds screen size
            return BUILD_FAILED
        if self.guess_width() > scr_wid: # test width
            return BUILD_FAILED
        return hei

    def __build(self, hei, beg, sta_hei):
        def vfn(o):
            siz = hei - sta_hei, self.__guess_virtual_window_width()
            pos = beg, 0
            self.__build_window(o, siz, pos)
        def bfn(o):
            siz = hei - sta_hei, self.__guess_binary_window_width()
            pos = beg, 0
            self.__build_window(o, siz, pos)
        def tfn(o):
            siz = hei - sta_hei, self.__guess_text_window_width()
            pos = beg, self.__def_bwindow.get_size_x()
            self.__build_window(o, siz, pos)
        def sfn(o):
            siz = sta_hei, self.guess_width()
            pos = beg + self.__def_bwindow.get_size_y(), 0
            self.__build_window(o, siz, pos)
        self.__do_build(vfn, bfn, tfn, sfn)

    # vertical split
    def vbuild_dryrun(self, beg):
        sta_hei = self.__get_status_window_height()
        hei = console.get_position_y()
        min_hei = window.get_min_binary_window_height() + sta_hei
        return self.__test_vbuild(hei, beg, min_hei)

    def vbuild(self, beg):
        sta_hei = self.__get_status_window_height()
        hei = console.get_position_y()
        self.__vbuild(hei, beg, sta_hei)
        return beg

    def vbuild_fixed_size_dryrun(self, lpw, beg):
        sta_hei = self.__get_status_window_height()
        hei = window.get_min_binary_window_height(lpw) + sta_hei
        min_hei = window.get_min_binary_window_height() + sta_hei
        return self.__test_vbuild(hei, beg, min_hei)

    def vbuild_fixed_size(self, lpw, beg):
        sta_hei = self.__get_status_window_height()
        hei = window.get_min_binary_window_height(lpw) + sta_hei
        self.__vbuild(hei, beg, sta_hei)
        return beg

    def __test_vbuild(self, hei, beg, min_hei):
        scr_hei = screen.get_size_y()
        scr_wid = screen.get_size_x()
        if hei <= 0:
            return BUILD_FAILED
        if beg < 0:
            return BUILD_FAILED
        if scr_hei < min_hei: # screen height < minimum workspace height
            return BUILD_FAILED
        if hei < min_hei: # height < minimum workspace height
            return BUILD_FAILED
        if hei > scr_hei: # height > screen height (redundant)
            return BUILD_FAILED
        if hei >= scr_hei: # this workspace exceeds screen size
            return BUILD_FAILED
        if beg + self.guess_width() > scr_wid: # test width
            return BUILD_FAILED
        return hei

    def __vbuild(self, hei, beg, sta_hei):
        def vfn(o):
            siz = hei - sta_hei, self.__guess_virtual_window_width()
            pos = 0, beg
            self.__build_window(o, siz, pos)
        def bfn(o):
            siz = hei - sta_hei, self.__guess_binary_window_width()
            pos = 0, beg
            self.__build_window(o, siz, pos)
        def tfn(o):
            siz = hei - sta_hei, self.__guess_text_window_width()
            pos = 0, beg + self.__def_bwindow.get_size_x()
            self.__build_window(o, siz, pos)
        def sfn(o):
            siz = sta_hei, self.guess_width()
            pos = self.__def_bwindow.get_size_y(), beg
            self.__build_window(o, siz, pos)
        self.__do_build(vfn, bfn, tfn, sfn)

    def __do_build(self, vfn, bfn, tfn, sfn):
        self.__build_virtual_window = vfn
        self.__build_binary_window = bfn
        self.__build_text_window = tfn
        self.__build_status_window = sfn

        for o in self.__vwindows.values():
            self.__build_virtual_window(o)
        for o in self.__bwindows.values():
            self.__build_binary_window(o)
        for o in self.__twindows.values():
            self.__build_text_window(o)
        for o in self.__swindows.values():
            self.__build_status_window(o)

        bin_hei = self.__def_bwindow.get_size_y()
        tex_hei = self.__def_twindow.get_size_y()
        assert bin_hei == tex_hei, (bin_hei, tex_hei)

        bin_wid = self.__def_bwindow.get_size_x()
        tex_wid = self.__def_twindow.get_size_x()
        sta_wid = self.__def_swindow.get_size_x()
        assert bin_wid + tex_wid == sta_wid, (bin_wid, tex_wid, sta_wid)

    def __build_virtual_window(self, o):
        self.__build_window(o, None, None)
    def __build_binary_window(self, o):
        self.__build_window(o, None, None)
    def __build_text_window(self, o):
        self.__build_window(o, None, None)
    def __build_status_window(self, o):
        self.__build_window(o, None, None)

    def __build_window(self, o, siz, pos):
        o.resize(siz, pos)
        o.update_capacity(self.__bpl)

    def __guess_virtual_window_width(self):
        return window.get_width(virtual.BinaryCanvas, self.__bpl)
    def __guess_binary_window_width(self):
        return window.get_width(panel.BinaryCanvas, self.__bpl)
    def __guess_text_window_width(self):
        return window.get_width(panel.TextCanvas, self.__bpl)

    def guess_width(self):
        return self.__guess_binary_window_width() + \
            self.__guess_text_window_width()

    def __get_virtual_window(self, cls):
        if cls not in self.__vwindows:
            if cls is console.get_default_class():
                o = window.Window(virtual.BinaryCanvas, virtual.NullFrame)
            elif cls is void.ExtConsole:
                o = window.Window(virtual.ExtCanvas, virtual.NullFrame)
            elif cls is visual.Console:
                o = self.__def_vwindow
            elif cls is visual.ExtConsole:
                o = self.__get_virtual_window(void.ExtConsole)
            elif util.is_subclass(cls, edit.Console):
                o = self.__def_vwindow
            self.__build_virtual_window(o)
            self.__vwindows[cls] = o
        return self.__vwindows[cls]

    def __get_binary_window(self, cls):
        if cls not in self.__bwindows:
            if cls is console.get_default_class():
                o = window.Window(panel.BinaryCanvas, panel.FocusableFrame)
            elif cls is void.ExtConsole:
                o = window.Window(extension.ExtBinaryCanvas,
                    panel.FocusableFrame)
            elif cls is visual.Console:
                o = window.Window(visual.BinaryCanvas, panel.FocusableFrame)
            elif cls is visual.ExtConsole:
                o = window.Window(visual.ExtBinaryCanvas, panel.FocusableFrame)
            elif util.is_subclass(cls, edit.Console):
                o = self.__def_bwindow
            self.__build_binary_window(o)
            self.__bwindows[cls] = o
        return self.__bwindows[cls]

    def __get_text_window(self, cls):
        if cls not in self.__twindows:
            if cls is console.get_default_class():
                o = window.Window(panel.TextCanvas, panel.Frame)
            elif cls is void.ExtConsole:
                o = window.Window(extension.ExtTextCanvas, panel.Frame)
            elif cls is visual.Console:
                o = window.Window(visual.TextCanvas, panel.Frame)
            elif cls is visual.ExtConsole:
                o = self.__get_text_window(void.ExtConsole)
            elif util.is_subclass(cls, edit.Console):
                o = self.__def_twindow
            self.__build_text_window(o)
            self.__twindows[cls] = o
        return self.__twindows[cls]

    def __get_status_window(self, cls):
        if cls not in self.__swindows:
            if cls is console.get_default_class():
                o = window.Window(*self.__get_status_window_class())
            elif cls is void.ExtConsole:
                o = self.__def_swindow
            elif cls is visual.Console:
                o = self.__def_swindow
            elif cls is visual.ExtConsole:
                o = self.__def_swindow
            elif util.is_subclass(cls, edit.Console):
                o = self.__def_swindow
            self.__build_status_window(o)
            self.__swindows[cls] = o
        return self.__swindows[cls]

    def read(self, x, n):
        return self.__cur_fileops.read(x, n)
    def read_current(self, n):
        return self.__cur_fileops.read(self.get_pos(), n)

    def insert(self, x, l, rec=True):
        self.__cur_fileops.insert(x, l, rec)
    def insert_current(self, l, rec=True):
        self.__cur_fileops.insert(self.get_pos(), l, rec)

    def replace(self, x, l, rec=True):
        self.__cur_fileops.replace(x, l, rec)
    def replace_current(self, l, rec=True):
        self.__cur_fileops.replace(self.get_pos(), l, rec)

    def delete(self, x, n, rec=True):
        self.__cur_fileops.delete(x, n, rec)
    def delete_current(self, n, rec=True):
        self.__cur_fileops.delete(self.get_pos(), n, rec)

    def brepaint(self, focus):
        for o in self.__windows:
            if o in self.__bwindows.values():
                o.repaint(focus)

    def repaint(self, focus):
        for o in self.__windows:
            o.repaint(focus)

    def lrepaint(self, low=False):
        for o in self.__windows:
            o.lrepaint(low)

    def go_up(self, n=1):
        for o in self.__windows:
            if o.go_up(n) == -1:
                return -1

    def go_down(self, n=1):
        for o in self.__windows:
            if o.go_down(n) == -1:
                return -1

    def go_left(self, n=1):
        for o in self.__windows:
            if o.go_left(n) == -1:
                return -1

    def go_right(self, n=1):
        for o in self.__windows:
            if o.go_right(n) == -1:
                return -1

    def go_pprev(self, n):
        for o in self.__windows:
            if o.go_pprev(n) == -1:
                return -1

    def go_hpprev(self, n):
        for o in self.__windows:
            if o.go_hpprev(n) == -1:
                return -1

    def go_pnext(self, n):
        for o in self.__windows:
            if o.go_pnext(n) == -1:
                return -1

    def go_hpnext(self, n):
        for o in self.__windows:
            if o.go_hpnext(n) == -1:
                return -1

    def go_head(self, n):
        for o in self.__windows:
            if o.go_head(n) == -1:
                return -1

    def go_tail(self, n):
        for o in self.__windows:
            if o.go_tail(n) == -1:
                return -1

    def go_lhead(self):
        for o in self.__windows:
            if o.go_lhead() == -1:
                return -1

    def go_ltail(self, n):
        for o in self.__windows:
            if o.go_ltail(n) == -1:
                return -1

    def go_phead(self, n):
        for o in self.__windows:
            if o.go_phead(n) == -1:
                return -1

    def go_pcenter(self):
        for o in self.__windows:
            if o.go_pcenter() == -1:
                return -1

    def go_ptail(self, n):
        for o in self.__windows:
            if o.go_ptail(n) == -1:
                return -1

    def go_to(self, n):
        for o in self.__windows:
            if o.go_to(n) == -1:
                return -1

    def get_bytes_per_line(self):
        return self.__bpl

    def set_bytes_per_line(self, bpl):
        assert isinstance(bpl, int)
        assert self.__bpl > 0
        if bpl == -1: # possible on container init
            return -1
        self.__bpl = bpl

    def get_capacity(self):
        return self.__def_bwindow.get_capacity()
