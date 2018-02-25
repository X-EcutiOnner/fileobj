## v0.7.57
+ Minor fixes and improvement
+ Change CTRL-w,v and CTRL-w,CTRL-v to vertical split
+ Add :vsplit
+ Add :screen
+ Add :set bpl (alias for :set bytes_per_line)
+ Add :set bpw (alias for :set bytes_per_window)
+ Add --bpl (alias for --bytes_per_line)
+ Add --bpw (alias for --bytes_per_window)
+ Add --no-native option for setup.py
+ Change -O to do vertical split (align with -O in vim)
+ Change -o to do horizontal version of -O (align with -o in vim)
+ Rename script/profile to script/profile.py
+ Remove script/fedora.spec
+ Remove script/pyclean.sh (integrate into script/pybuild.sh)
+ Move script/cstruct.usb to script/cstruct/usb
+ Move script/cstruct.hammer to script/cstruct/hammer
+ Create empty file ~/.fileobj/cstruct if it does not exist

## v0.7.56
+ Minor fixes and improvement

## v0.7.55
+ Minor fixes and improvement
+ Fix a bug (be able to recover from a tmux specific screen issue with Ctrl-l)
+ Change default manpage directory from /usr/local/share/man/man1 to /usr/share/man/man1
+ Rename script/build.sh to script/pybuild.sh
+ Rename script/clean.sh to script/pyclean.sh

## v0.7.54
+ Minor fixes and improvement
+ Improve Solaris/illumos support

## v0.7.53
+ Minor fixes and improvement
+ Fix a bug (check errno for native ptrace(2) peek functions)
+ Fix a bug (search "a b c" ignores " b c" for the initial attempt)
+ Enable ptrace(2) support on FreeBSD/DragonFlyBSD/NetBSD/OpenBSD
+ Enable pid path support on FreeBSD/DragonFlyBSD/NetBSD/OpenBSD
+ Improve Solaris/illumos support
+ Add FILEOBJ_USE_ILLUMOS_CAVEAT

## v0.7.52
+ Minor fixes and improvement
+ Fix a bug (avoid >1 same fileobj being loaded via partial path)
+ Change default window mode to --simple
+ Remove --simple
+ Add --verbose_window
+ Add FILEOBJ_USE_CURSOR_FALL_THROUGH
+ Add FILEOBJ_USE_SHELL
+ Remove FILEOBJ_USE_MAGIC_SCAN
+ Remove FILEOBJ_NETBSD_SIZEOF_DISKLABEL
+ Remove FILEOBJ_DRAGONFLYBSD_SIZEOF_PARTINFO
+ Remove FILEOBJ_KEY_TAB
+ Remove FILEOBJ_KEY_ENTER
+ Remove FILEOBJ_KEY_ESCAPE
+ Remove FILEOBJ_KEY_SPACE
+ Enable fileobj._native ptrace(2) support on Linux
+ Support @objdump[section] syntax for pid path

## v0.7.51
+ Minor fixes and improvement
+ Add [count] support for searching
+ Add script/clean.sh
+ Add script/build.sh
+ Move script/README* to doc/
+ Move script/fileobj.1 to doc/

## v0.7.50
+ Minor fixes and improvement
+ Fix bugs
+ Add :cmpr
+ Add :cmpr!
+ Add :cmprnext
+ Add :cmprnext!
+ Add :fobj
+ Improve :hammervol

## v0.7.49
+ Minor fixes and improvement
+ Add :bind
+ Add @:
+ Add --force
+ Add FILEOBJ_USE_FORCE
+ Add FILEOBJ_REGFILE_SOFT_LIMIT
+ Use even-sized windows on :cmp variants

## v0.7.48
+ Minor fixes and improvement

## v0.7.47
+ Minor fixes and improvement

## v0.7.46
+ Minor fixes and improvement

## v0.7.45
+ Minor fixes and improvement
+ Add Python3.6 to supported Python versions

## v0.7.44
+ Minor fixes and improvement
+ Add C extension for Cygwin

## v0.7.43
+ Minor fixes and improvement
+ Add C extension fileobj._native to better support ioctls for Linux/NetBSD/OpenBSD/FreeBSD/DragonFlyBSD
+ Add fileobj.native as a wrapper over fileobj._native

## v0.7.42
+ Minor fixes and improvement

## v0.7.41
+ Fix/workaround OpenBSD specific bug
+ Minor fixes and improvement

## v0.7.40
+ Minor fixes and improvement
+ Add Python3.6b to supported Python versions at the moment

## v0.7.39
+ Minor fixes and improvement
+ Improve Cygwin support
+ Add FILEOBJ_USE_CYGWIN_CAVEAT
+ Add script/README.distributions.md

## v0.7.38
+ Minor fixes and improvement
+ Add :allocator
+ Add :osdep

## v0.7.37
+ Minor fixes and improvement
+ Add :meminfo
+ Add script/README.changes.md

## v0.7.36
+ Minor fixes and improvement
+ Improve Cygwin support
+ Separate lists/examples/notes section of README.md into different script/*.md files
+ Add script/autogen.py

## v0.7.35
+ Minor fixes and improvement
+ Add script/fedora.spec
+ Improve README.md

## v0.7.34
+ Minor fixes and improvement
+ Remove v prefix from version# in sdist archive to sync with Fedora's RPM versioning in general (Git branch and tag name still use v prefix)
+ Add version.RELEASE to sync with Fedora's RPM versioning in general (version.RELEASE may or may not be used)
+ Rename script/installman.sh to script/install.sh
+ Remove script/check.py
+ Improve README.md

## v0.7.33
+ Add script/fileobj.1
+ Add script/installman.sh
+ Add :cmpnext
+ Add :cmpnext!
+ Improve README.md

## v0.7.32
+ Fix :cstruct bug

## v0.7.31
+ Add :cmp
+ Add :cmp!

## v0.7.30
+ Minor fixes and improvement
+ Cleanups
+ Remove unused code

## v0.7.29
+ Minor fixes and improvement
+ Cleanups
+ Remove unused code
+ Remove symlink README -> ./README.md
+ Remove script/stream

## v0.7.28
+ Minor bug fixes
+ Cleanups
+ Support string type in :cstruct in addition to char[] (helps omit bunch of \0 shown when using char[] as C string)
+ Support x8,x16,x32,x64 types in :cstruct to indicate unsigned hexadecimal output
+ Add :hammervol extension
+ Add FILEOBJ_USE_TMUX_CAVEAT
+ Add FILEOBJ_USE_PUTTY_CAVEAT
+ Improve terminal multiplexer and PuTTY support
+ Improve README.md

## v0.7.27
+ Minor bug fix
+ Cleanups

## v0.7.26
+ Minor bug fixes
+ Cleanups
+ Add --simple
+ Add --terminal_height,--terminal_width
+ Add --bytes_per_window
+ Add :set bytes_per_window
+ Rename --width to --bytes_per_line
+ Rename :set width to :set bytes_per_line
+ Add basic registers {0-9a-zA-Z"} support (experimental)
+ Add :registers
+ Add :kmod
+ Add :fcls
+ Add :bufsiz
+ Add :argv
+ Add :md5
+ Add sb for bytes swap
+ Improve window height adjustment
+ Add Darwin support (experimental)
+ Add FILEOBJ_USE_XNIX
+ Add FILEOBJ_USE_BSD_CAVEAT
+ Improve *nix support in general