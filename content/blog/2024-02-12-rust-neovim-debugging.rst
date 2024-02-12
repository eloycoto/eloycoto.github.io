Tips for Rust debugging in Neovim
==================================

:date: 2024-02-12 17:00
:language: en-GB
:author: eloycoto
:head: Tips for Rust Debugging in Neovim
:index_title: Rust Debugging Tips for Neovim
:metatitle: Essential Rust Debugging Tips for Neovim Developers
:tags: Rust, embedded, neovim
:metatags: Rust debugging, Neovim, embedded development
:description: Explore essential Rust debugging tips for Neovim developers. Learn how to efficiently debug Rust code using Termdebug and GDB, with special insights for embedded development with OpenOCD integration.
:keywords: Rust debugging tips, Neovim development, Termdebug, GDB, embedded Rust, OpenOCD integration

One of the most important aspects of programming in Rust is efficient
debugging. There are various tools available for this purpose; some developers
prefer the `Debug Adapter Protocol (DAP)
<https://microsoft.github.io/debug-adapter-protocol//>`_, which is utilized by
default in VSCode. However, for those using Neovim, the trendy direction is
`nvim-dap <https://github.com/mfussenegger/nvim-dap>`_.

Since GDB version 1.14, it `has been possible
<https://www.phoronix.com/news/GNU-Debugger-GDB-14.1>`_ to utilize the DAP
protocol directly with GDB (using `gdb –interpreter dap`), allowing clients to
consume debugging information. I tried some opt for plugins like dap-ui and the
nvim-dap, but I cannot find confort without the GDB REPL, something that I miss
in this utilities.

With that said, Vim 8 introduced a powerful tool called **Termdebug**, which
can be configured to emulate the GDB workflow effectively.

In my setup, I have specific constraints:

-  The configuration should support using GDB with either the binary or
   with OpenOCD.
-  I prefer utilizing the GDB REPL but want to manage breakpoints from
   the code editor.

The first step is to enable Termdebug:

.. code-block:: bash

   :packadd termdebug

From there, Termdebug can be invoked directly:

.. code-block:: bash

   :Termdebug binary

Typing the binary path for each interaction can be tedious, so let’s
automate it. When running cargo build, there’s an option for JSON
output, allowing us to list the created executables:

.. code-block:: bash

   $ --> cargo build --message-format=json 2> /dev/null | jq -r 'select(.executable !=null) | [.executable]'
   [
     "/home/eloy/dev/upstream/eloycoto/playground/target/debug/playground"
   ]
   $ -->

With this information, we can launch Termdebug directly using a Neovim
Lua API:

.. code-block:: lua

   -- cargo_build_debug Build the cargo crate, and return the executables path
   function cargo_build_debug()
       vim.cmd("!cargo build")
       local cargo_output = vim.fn.system("cargo build --message-format=json 2> /dev/null | jq -r 'select(.executable !=null) | [.executable]'")
       return vim.fn.json_decode(cargo_output)
   end

   function Debugger()
       vim.cmd('packadd termdebug')
       local filepaths = cargo_build_debug()
       local paths_len = #filepaths
       local path = ""
       if paths_len == 0 then
           error("executable cannot be found")
       elseif paths_len == 1 then
           path = filepaths[1]
       else
           local choice = vim.fn.inputlist(filepaths)
           path = filepaths[choice+1]
       end
       vim.cmd('Termdebug '..path)
   end

   vim.api.nvim_create_user_command('DDebug', Debugger, {})

Calling the **DDebug** function launches a GDB command within Neovim,
utilizing the Job Async API, in a separate split where interaction with
the GDB REPL is possible. Now, within the code, interactions can be made
directly using commands like `:Break` or `:Step`.

The commands available in normal mode are:

::

    `:Run` [args]      run the program with [args] or the previous arguments
    `:Arguments` {args}  set arguments for the next `:Run`

    *:Break*   set a breakpoint at the current line; a sign will be displayed
    *:Clear*   delete the breakpoint at the current line

    *:Step*    execute the gdb "step" command
    *:Over*    execute the gdb "next" command (`:Next` is a Vim command)
    *:Until*   execute the gdb "until" command
    *:Finish*  execute the gdb "finish" command
    *:Continue*    execute the gdb "continue" command
    *:Stop*    interrupt the program

Additionally, variables can be inspected:

::

   `:Evaluate`     evaluate the expression under the cursor
   `K`         same (see |termdebug_map_K| to disable)
   `:Evaluate` {expr}   evaluate {expr}
   `:'<,'>Evaluate`     evaluate the Visually selected text

Bonus Point - OpenOCD Debugging
-------------------------------

In Rust embedded development, GDB connects to OpenOCD to reach the
target server. Typically, a GDB configuration file is created to
establish this connection.

In Neovim, we can check if the file exists and, if so, append the
configuration and debug directly on the target board:

::

   local stat = vim.loop.fs_stat("openocd.gdb")
   if stat then
       path = "-x openocd.gdb " .. path
   end
   vim.cmd('Termdebug '..path)

Using this approach enables seamless debugging of your Rust program.

Happy coding!
