Envoy WASM debugging with BPFtrace
========================================================

:date: 2021-01-19 23:00
:language: en-GB
:author: eloycoto
:head: Envoy WASM debugging with BPFtrace
:index_title: Envoy WASM debugging with BPFtrace
:metatitle: Envoy bpftrace debug
:tags: bpf, envoy, wasm
:metatags: bpf, envoy, wasm
:description: How to debug how many proxy_wasm::export calls are made by wasm filters in envoy using BPFtrace
:keywords: bpf, envoy, wasm, bpftrace

A few days back, I was checking `Envoy <https://www.envoyproxy.io/>`_
performance when WASM is in use. `PPROF
<https://github.com/envoyproxy/envoy/blob/main/bazel/PPROF.md>`_ can be enabled
quite easily in Envoy, but I wanted to have less intrusive experience.

In the past, to debug things like this I always use `Systemtap
<https://www.sourceware.org/systemtap/>`_, (super intrusive) but `BPFtrace
<https://github.com/iovisor/bpftrace>`_ is straightforward and fast.

So I did this super simple `docker-compose project
<https://github.com/eloycoto/envoy_playground/tree/master/bpftrace>`_ where you
can run bpftrace meanwhile you run Envoy, and here is the bpftrace script that
you can see the list of WASM functions used by Envoy, and the time that was
used.

Over the next weeks, I'll keep adding bpftrace scripts `here
<https://github.com/eloycoto/envoy_playground/tree/master/bpftrace/traces>`_,
because they are quite useful on my day job.

.. code-block:: bpftrace

  #!/usr/bin/env bpftrace
  BEGIN
  {
    printf("Tracing proxy-wasm call in envoy...Hit Ctrl-C to end.\n");
  }

  uprobe:/usr/bin/envoy:proxy_wasm*exports* {
    @start[tid] = nsecs;
  }

  uretprobe:/usr/bin/envoy:proxy_wasm*exports*
  /@start[tid]/
  {
    @ns[func] = hist(nsecs - @start[tid]);
    delete(@start[tid]);
  }

And running it using the following command:

.. code-block:: none

  #-> bpftrace -p $(pgrep envoy) /traces/proxy_wasm_calls_time.bt
  Attaching 249 probes...
  Tracing proxy-wasm call in envoy...Hit Ctrl-C to end.
  ^C
  @ns[proxy_wasm::exports::get_current_time_nanoseconds(void*, proxy_wasm::Word)]:
  [2K, 4K)               2 |@@@@@@@@@@@@@@@@@@@@                                |
  [4K, 8K)               5 |@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@|
  [8K, 16K)              2 |@@@@@@@@@@@@@@@@@@@@                                |

  @ns[proxy_wasm::exports::send_local_response(void*, proxy_wasm::Word, proxy_wasm::Word, proxy_wasm::Word, proxy_wasm::Word, proxy_wasm::Word, proxy_wasm::Word, proxy_wasm::Word, proxy_wasm::Word)]:
  [1K, 2K)             544 |@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@|
  [2K, 4K)             419 |@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@            |
  [4K, 8K)              31 |@@                                                  |
  [8K, 16K)              3 |                                                    |
  [16K, 32K)             1 |                                                    |
  [32K, 64K)             1 |                                                    |
  [64K, 128K)            1 |                                                    |

  @ns[proxy_wasm::exports::send_local_response(void*, proxy_wasm::Word, proxy_wasm::Word, proxy_wasm::Word, proxy_wasm::Word, proxy_wasm::Word, proxy_wasm::Word, proxy_wasm::Word, proxy_wasm::Word)]:
  [2K, 4K)             653 |@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@|
  [4K, 8K)             295 |@@@@@@@@@@@@@@@@@@@@@@@                             |
  [8K, 16K)             47 |@@@                                                 |
  [16K, 32K)             5 |                                                    |

  @ns[proxy_wasm::exports::get_header_map_pairs(void*, proxy_wasm::Word, proxy_wasm::Word, proxy_wasm::Word)]:
  [1K, 2K)             295 |@@@@@@@@@@@@@@@@@@@@@@@                             |
  [2K, 4K)             653 |@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@|
  [4K, 8K)              47 |@@@                                                 |
  [8K, 16K)              3 |                                                    |
  [16K, 32K)             2 |                                                    |

  @ns[proxy_wasm::exports::log(void*, proxy_wasm::Word, proxy_wasm::Word, proxy_wasm::Word)]:
  [1K, 2K)            4036 |@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ |
  [2K, 4K)            4098 |@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@|
  [4K, 8K)             746 |@@@@@@@@@                                           |
  [8K, 16K)            106 |@                                                   |
  [16K, 32K)            14 |                                                    |
  [32K, 64K)             6 |                                                    |
  [64K, 128K)            1 |                                                    |
  [128K, 256K)           1 |                                                    |
  [256K, 512K)           0 |                                                    |
  [512K, 1M)             0 |                                                    |
  [1M, 2M)               1 |                                                    |

If you want to learn bpftrace, I highly recommend to have a look at `bpftrace
one-liners
<https://github.com/iovisor/bpftrace/blob/master/docs/tutorial_one_liners.md>`_
tutorial, is made for dummies like me.

Enjoy!
