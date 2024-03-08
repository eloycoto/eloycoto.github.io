Org-Mode Workflow with Neovim: VISIBILITY directive
==============================================================

:date: 2024-03-08 12:00
:language: en-GB
:author: eloycoto
:head: Org-Mode Workflow with Neovim: VISIBILITY directive
:index_title: Org-Mode Workflow with Neovim: VISIBILITY directive
:metatitle: Org-Mode Workflow with Neovim: VISIBILITY directive
:tags: neovim
:metatags: neovim, org-mode, productivity, workflow
:description: Discover how integrating Neovim with Org-Mode transformed the way I manage tasks and organize notes.
:keywords: Neovim, Org-Mode, productivity, workflow, task management, note organization

I have been using `org-mode <https://orgmode.org/>`_ for a few years now. The
`Neovim support <https://github.com/nvim-orgmode/>`_ is good, and I love the
way it handles tagging sections, links, formatting, and structure. I am also
happy with the agenda support it provides.

However, one of the issues I've encountered is the inability to unfold specific
sections. For instance, in my "work" note, where I track tasks ranging from
emails sent to pending matters, I typically organize it by weeks. I always want
the current week to be unfolded by default.

Recently, I experimented with `Treesitter query
<https://github.com/neovim/neovim/blob/master/runtime/doc/treesitter.txt>`_ in
Neovim. It was an exciting experiment because I could filter all the sections
with the directive `VISIBILITY
<https://orgmode.org/manual/Global-and-local-cycling.html>`_ and unfold them on
demand.

The query language is well described here, and with Neovim version 0.10, you
can test it using the `:EditQuery
<https://github.com/neovim/neovim/pull/25161>`_ command.

The final code looks something like this:

.. code-block:: lua

    function M:VISIBILITY()
        local query_string = [[
            ((directive name: (expr) @name value: (value) @value)
            ((#match? @name "VISIBILITY")))
        ]]

        local parser = require('nvim-treesitter.parsers').get_parser()
        local query = vim.treesitter.query.parse(parser:lang(), query_string)
        local tree = parser:parse()[1]
        local result = query:iter_captures(tree:root(), 0)
        for _, n in result do
            if n:type() == "value" then
                local value = get_value_for_directive(n)
                if value == "children" then
                    -- Get the parent section, and unfold all the children
                    parent = get_parent_subsection(n)
                    for child in parent:iter_children() do
                        pcall(unfold_node, child);
                    end
                elseif value == "all" then
                    unfold_node(n)
                elseif value == "folded" then
                    -- Do nothing for now
                    -- unfold_node(n)
                end
            end
        end
        vim.api.nvim_win_set_cursor(0, {1, 0})
    end


Full code can be found `here
<https://github.com/eloycoto/dotfiles/commit/24b93718e69d76bb4e8ed192ce50d837c85b3eac>`_

Now, my life is much, much easier.
