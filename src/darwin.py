# Copyright (c) 2016, Tomohiro Kusumi
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

from __future__ import with_statement

from . import libc
from . import log
from . import unix

PT_READ_I  = 1
PT_READ_D  = 2
PT_WRITE_I = 4
PT_WRITE_D = 5
PT_ATTACH  = 10
PT_DETACH  = 11

def get_blkdev_info(f):
    with fopen(f) as fd:
        return __get_blkdev_info(fd)

def __get_blkdev_info(fd):
    try:
        d = {   "DKIOCGETBLOCKCOUNT" : 0x40086419,
                "DKIOCGETBLOCKSIZE"  : 0x40046418, }
        s = "DKIOCGETBLOCKCOUNT"
        blkcount = unix.ioctl_get_int(fd, d[s], 8)
        s = "DKIOCGETBLOCKSIZE"
        sector_size = unix.ioctl_get_int(fd, d[s], 4)
        return blkcount * sector_size, sector_size, ''
    except Exception as e:
        log.error("ioctl({0}, {1}) failed, {2}".format(fd.name, s, e))
        raise

def read_reg_size(f):
    return unix.read_reg_size(f)

def seek_end(f):
    return unix.seek_end(f)

def get_inode(f):
    return unix.get_inode(f)

def fopen(f, mode='r'):
    return unix.fopen(f, mode)

def fopen_text(f, mode='r'):
    return unix.fopen_text(f, mode)

def fcreat(f):
    return unix.fcreat(f)

def fcreat_text(f):
    return unix.fcreat_text(f)

def symlink(source, link_name):
    return unix.symlink(source, link_name)

def fsync(fd):
    return unix.fsync(fd)

def truncate(f, offset):
    return unix.truncate(f, offset)

def utime(f, st):
    return unix.utime(f, st)

def touch(f):
    return unix.touch(f)

def stat_type(f):
    return unix.stat_type(f)

def get_page_size():
    return unix.get_page_size()

def get_buffer_size():
    return unix.get_buffer_size()

def get_total_ram():
    """
    [user@darwin ~]$ sysctl hw.physmem
    hw.physmem: 2147483648
    """
    try:
        s = execute("sysctl", "hw.physmem").stdout
        x = s.split()[-1]
        return int(x)
    except Exception as e:
        log.error(e)
        return -1

def get_free_ram():
    return unix.get_free_ram()

def has_blkdev():
    return True

def is_blkdev(f):
    """
    [user@darwin ~]$ file /dev/disk0
    /dev/disk0: block special
    """
    return unix.stat_is_blkdev(f)

def is_blkdev_supported():
    return True

def mmap_full(fileno, readonly=False):
    return unix.mmap_full(fileno, readonly)

def mmap_partial(fileno, offset, length, readonly=False):
    return unix.mmap_partial(fileno, offset, length, readonly)

def has_mmap():
    return True

def has_mremap():
    return False

def test_mmap_resize(osiz, nsiz):
    return unix.test_mmap_resize(osiz, nsiz)

def has_pid_access(pid):
    return unix.kill_sig_zero(pid)

def has_pid(pid):
    return unix.ps_has_pid(pid)

def get_pid_name(pid):
    return unix.get_pid_name_from_ps(pid)

def has_ptrace():
    return libc.has_ptrace()

def ptrace_peektext(pid, addr):
    return libc.ptrace(PT_READ_I, pid, addr, None)

def ptrace_peekdata(pid, addr):
    return libc.ptrace(PT_READ_D, pid, addr, None)

def ptrace_poketext(pid, addr, data):
    return libc.ptrace(PT_WRITE_I, pid, addr, data)

def ptrace_pokedata(pid, addr, data):
    return libc.ptrace(PT_WRITE_D, pid, addr, data)

def ptrace_attach(pid):
    return libc.ptrace(PT_ATTACH, pid, None, None)

def ptrace_detach(pid):
    return libc.ptrace(PT_DETACH, pid, 1, 0)

def get_ptrace_word_size():
    return libc.get_ptrace_data_size()

def waitpid(pid, opts):
    return unix.waitpid(pid, opts)

def parse_waitpid_result(status):
    return unix.parse_waitpid_result(status)

def execute(*l):
    return unix.execute(*l)

def execute_sh(cmd):
    return unix.execute_sh(cmd)

def init():
    unix.init_procfs()
    libc.init_ptrace("int")
