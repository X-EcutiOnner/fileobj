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