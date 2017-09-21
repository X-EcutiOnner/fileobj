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

# This file must have no dependency on other files.

import os
import platform

if platform.system() in (
    "NetBSD",
    "OpenBSD",
    "FreeBSD",
    "DragonFly",
    "Darwin"):
    if "FILEOBJ_USE_BSD_CAVEAT" not in os.environ:
        os.environ["FILEOBJ_USE_BSD_CAVEAT"] = "forced_by_init"

# XXX copied from nodep.is_cygwin()
def __is_cygwin(name):
    if name.startswith("CYGWIN"):
        return True
    if not name.startswith("Windows"):
        return False
    try:
        import subprocess
        p = subprocess.Popen(["uname"], stdout=subprocess.PIPE)
        s = p.communicate()[0]
        return s.startswith("CYGWIN")
    except Exception:
        return False

if __is_cygwin(platform.system()):
    if "FILEOBJ_USE_CYGWIN_CAVEAT" not in os.environ:
        os.environ["FILEOBJ_USE_CYGWIN_CAVEAT"] = "forced_by_init"

    # procfs doesn't appear in mount command result
    if "FILEOBJ_PROCFS_MOUNT_POINT" not in os.environ:
        os.environ["FILEOBJ_PROCFS_MOUNT_POINT"] = "/proc"
