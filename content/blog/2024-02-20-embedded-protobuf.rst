Dynamic Serialization with Protobuf on Embedded Rust
=====================================================

:date: 2024-02-20 18:00
:language: en-GB
:author: eloycoto
:head: Dynamic Serialization with Protobuf on Embedded Rust
:index_title: Dynamic Serialization with Protobuf and Embedded Rust
:metatitle: Dynamic Serialization with Protobuf and Embedded Rust: A Comprehensive Guide
:tags: Rust, Embedded
:metatags: Rust, Protobuf, Embedded Systems, Serialization
:description: Exploring dynamic serialization options in Rust for embedded systems using Protocol Buffers (Protobuf).
:keywords: Rust, Protobuf, Embedded Systems, Serialization, Dynamic Serialization, Rust-embedded, Protobuf Serialization, Embedded Rust, Prost Library

The other day, I found myself in a situation where I needed to transmit data
via `LORA <https://es.wikipedia.org/wiki/LoRa>`_, and then, I realized I needed
dynamic serialization for my data structures. Fortunately, there are several
serialization engines available that I could leverage.

Typically, I'd opt for JSON due to its simplicity and widespread support.
However, `Protocol Buffers (ProtoBuf) <https://protobuf.dev/>`_, which has been
around for some years, usually has faster encoding and decoding. While ProtoBuf
may seem a bit more complex initially, I found it to be quite manageable,
especially when working with proto files. Another option, `Avro
<https://avro.apache.org/>`_, exists, but I lack sufficient experience with it.

When it comes to ProtoBuf in Rust, the go-to library is `tokio-rs/prost
<https://github.com/tokio-rs/prost>`_. It offers an excellent API and
non-standard support, although it does require heap allocation (`alloc
<https://doc.rust-lang.org/alloc/>`_).

Heap allocation on embedded devices
***************************************

Heap allocation isn't typically present in embedded environments, but thanks to
the Rust-embedded team's efforts, there is a `heap allocator library
<https://github.com/rust-embedded/embedded-alloc/tree/master>`_ available.
However, allocating memory on embedded devices requires careful consideration
due to its implications.

To enable allocation on a device, follow these steps:

First, we need to incorporate the alloc crate:

.. code-block:: rust

    use embedded_alloc::Heap;
    extern crate alloc;

The `Global Allocator <https://doc.rust-lang.org/std/alloc/#the-global_allocator-attribute>`_  is the
way to define the Rust allocator for your program. The `GlobalAlloc trait
<https://doc.rust-lang.org/alloc/alloc/trait.GlobalAlloc.html>`_ outlines
what's necessary to use it. You can find a straightforward example in the
documentation `here <https://doc.rust-lang.org/alloc/alloc/trait.GlobalAlloc.html#example>`_.

Our application should define a new global allocator using the
`embedded_alloc::Heap` type:

.. code-block:: rust

    #[global_allocator]
    static HEAP: Heap = Heap::empty();

I highly recommend exploring the Heap alloc implementation , as it's relatively
straightforward and provides insights into the internals, which can be helpful.
You can find `it here <https://github.com/rust-embedded/embedded-alloc/blob/5ff132a2c1c504e3a5827bca828d4eaf2682a77d/src/lib.rs#L75-L90>`_.

One of the prerequisites is to initialize the heap. It's crucial to understand
the constraints of your board to avoid filling up memory unnecessarily. Here's
an example:

.. code-block:: rust

    #[entry]
    fn main() -> ! {
        {
            use core::mem::MaybeUninit;
            const HEAP_SIZE: usize = 1024;
            static mut HEAP_MEM: [MaybeUninit<u8>; HEAP_SIZE] = [MaybeUninit::uninit(); HEAP_SIZE];
            unsafe { HEAP.init(HEAP_MEM.as_ptr() as usize, HEAP_SIZE) }
        }


With this setup, all the `alloc <https://doc.rust-lang.org/alloc/>`_ libraries
are now available, like `alloc::Vec` for use with growable arrays.


Encoding to protobuf
***********************

Let's delve into why `prost` needs the alloc library. When parsing protobuf
data, the list of items can be undetermined, making it challenging to work with
fixed arrays. Prost leverages alloc::Vec, enabling arrays to grow dynamically
if it's needed.

There's a `helpful guide
<https://github.com/tokio-rs/prost?tab=readme-ov-file#using-prost-in-a-cargo-project>`_
on using prost, which you can follow. For our purposes, we'll focus on
serializing an internal struct. In this case, it's crucial to annotate the
struct with attributes like `Message` and `prost`:

.. code-block:: rust

    #[derive(Clone, PartialEq, ::prost::Message)]
    pub struct Chrono {
        #[prost(uint32, tag = "1")]
        pub id: u32,
        #[prost(uint32, tag = "2")]
        pub time: u32,
    }

Once the struct is initialized, the encode method is available, which return
the buffer with the data in hexadecimal:


.. code-block:: rust

    let mut dst = Vec::with_capacity(chrono.encoded_len());

    chrono.encode(&mut dst).unwrap();
    writeln!(hstdout, "DST: {:?}", dst).unwrap();
    drop(chrono);

To wrap up, I've opted for Prost despite its slight complexity because I
require a dynamic array with an unpredictable length, and I'd rather avoid
implementing chunked reading or custom serialization. This approach aligns
perfectly with my use case, although I'll proceed with caution in another
scenarios.
