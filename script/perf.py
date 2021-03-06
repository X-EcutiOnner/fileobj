# Copyright (c) 2014, Tomohiro Kusumi
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

if __name__ == '__main__':
    import cProfile
    import os
    import platform
    import pstats
    import re
    import sys

    try:
        if platform.system() == "Windows":
            import fileobj_.core as core
            import fileobj_.kernel as kernel
            import fileobj_.nodep as nodep
            import fileobj_.screen as screen
            import fileobj_.setting as setting
            import fileobj_.util as util
        else:
            import fileobj.core as core
            import fileobj.kernel as kernel
            import fileobj.nodep as nodep
            import fileobj.screen as screen
            import fileobj.setting as setting
            import fileobj.util as util
    except ImportError as e:
        sys.stderr.write("{0}\n".format(e))
        sys.exit(1)

    nodep.test()

    d = setting.get_user_dir()
    if not os.path.isdir(d):
        os.makedirs(d)
        if not os.path.isdir(d):
            sys.stderr.write("No {0}\n".format(d))
            sys.exit(1)

    s = util.get_stamp("perf")
    f = os.path.join(d, s) + ".txt"
    if os.path.isfile(f):
        sys.stderr.write("{0} exists\n".format(f))
        sys.exit(1)

    keys = "time",
    for i, s in enumerate(sys.argv):
        m = re.match(r"--sort=(\S+)", s)
        if m:
            l = m.group(1).split(",")
            keys = [x for x in l if x]
            del sys.argv[i]
            break

    profile = cProfile.Profile()
    profile.enable()
    assert util.is_running_script_perf()
    ret = core.dispatch()
    screen.cleanup()
    profile.disable()

    fd = open(f, "w")
    stats = pstats.Stats(profile, stream=fd)
    try:
        stats.sort_stats(*keys)
    except KeyError as e:
        print(repr(e))
        keys = (1,) # time
        stats.sort_stats(*keys)
    stats.print_stats()
    fd.close()

    l = os.path.join(os.path.dirname(f), "perf.txt")
    if os.path.islink(l):
        os.unlink(l)
    if kernel.symlink(os.path.basename(f), l) != -1:
        print("Create symlink {0} -> {1}".format(l, f))
    else: # likely "symbolic link privilege not held" on Windows
        print("Failed to create symlink {0} -> {1}".format(l, f))

    print("done...")
    print(keys)
    if ret:
        sys.exit(-ret)
