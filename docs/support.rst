==================
 Terminal Support
==================

Supported Terminals
===================

===============  =======  =======  ===  =========  =======  =======  ======
Terminal         default  bright   dim  underline  blink    reverse  hidden
===============  =======  =======  ===  =========  =======  =======  ======
xterm            yes      yes      yes  yes        yes      yes      yes
linux            yes      yes      yes  bright     yes      yes      no
rxvt             yes      yes      no   yes        bright   yes      no
Windows [0]_     yes      yes      yes  no         no       yes      yes
PuTTY [1]_       yes      yes      no   yes        [2]_     yes      no
Cygwin SSH [3]_  yes      yes      no   [4]_       [4]_     [2]_     yes
===============  =======  =======  ===  =========  =======  =======  ======

Currently unsupported, but should support
=========================================

===============  =======  =======  ===  =========  =======  =======  ======
Terminal         default  bright   dim  underline  blink    reverse  hidden
===============  =======  =======  ===  =========  =======  =======  ======
dtterm           yes      yes      yes  yes        reverse  yes      yes
teraterm         yes      reverse  no   yes        rev/red  yes      no
aixterm          kinda    normal   no   yes        no       yes      yes
Mac Terminal     yes      yes      no   yes        yes      yes      yes
===============  =======  =======  ===  =========  =======  =======  ======

Unsupported and will not support
================================

Windows Telnet
	It thinks it supports ANSI control, but it's so horribly 
	buggy its best to ignore it all together. (``TERM = ansi``)


.. [0] The default windows terminal, ``cmd.exe`` does not set the ``TERM`` variable, so
	detection is done by checking if the string ``'win32'`` is in ``sys.platform``. This
	This method has some limitations, particularly with remote terminal. But if you're
	allowing remote access to a Windows computer you probably have bigger problems.
	
.. [1] Putty has the ``TERM`` variable set to ``xterm`` by default

.. [2] Makes background bright

.. [3] Cygwin's SSH support's ANSI, but the regular terminal does not, check for
	win32 first, then check for cygwin. That should give us the cases when
	cygwin is used through SSH or telnet or something. (``TERM = cygwin``)

.. [4] Sets foreground color to cyan
