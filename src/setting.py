# Copyright (c) 2010-2014, TOMOHIRO KUSUMI
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

import os
import sys

from . import env

def iter_setting_name():
    for s in env.iter_env_name():
        yield env.env_to_setting_name(s)

def get_trace_path():
    return __get_path("trace")

def get_stream_path():
    return __get_path("stream")

def get_log_path():
    return __get_path("log")

def get_history_path():
    return __get_path("history")

def get_ext_cstruct_path():
    return __get_path("ext_cstruct")

def __get_path(s):
    f = getattr(this, s + "_path")
    b = getattr(this, s + "_base")
    d = getattr(this, s + "_dir")
    if f:
        return f
    if b and d:
        return os.path.join(d, b)
    elif not b:
        return ''
    else:
        d = get_userdir_path()
        if d:
            return os.path.join(d, b)
        else:
            return ''

def get_userdir_path():
    if this.userdir_path:
        return this.userdir_path
    elif this.userdir_base and this.userdir_dir:
        return os.path.join(this.userdir_dir, this.userdir_base)
    else:
        return ''

def init_user():
    f = get_userdir_path()
    if not f:
        return -1
    elif os.path.isdir(f):
        if os.access(f, os.R_OK | os.W_OK):
            this.userdir_path = f
            return 0 # already exists
        else:
            this.userdir_base = None
            return -1 # no permission
    else:
        try:
            os.makedirs(f)
            this.userdir_path = f
            return 1 # mkdir success
        except Exception:
            this.userdir_base = None
            return -1

def init():
    for s in env.iter_env_name():
        setattr(this, env.env_to_setting_name(s),
            env.get_setting(s))

this = sys.modules[__name__]
init()
