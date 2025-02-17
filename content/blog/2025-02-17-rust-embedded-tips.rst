Embedded Rust Development Tips with Embassy
==============================================
:date: 2025-02-17 13:00
:language: en-GB
:author: eloycoto
:tags: rust
:head: Embedded Rust Development Tips with Embassy
:index_title: Embassy Rust Tips: I2C, Channels, and Hardware Selection
:metatitle: Practical Embedded Rust Development Guide with Embassy
:metatags: embedded rust, embassy framework, i2c, async programming, microcontroller
:description: Learn practical tips for embedded Rust development using Embassy, including I2C device management, async patterns, and microcontroller selection.
:keywords: embedded-rust, embassy, i2c-scanning, async-select, channels, esp32-c6, nrf52840, embedded-hal

I've been working with embedded Rust for a while now, and there's one thing
that keeps coming back to bite me - debug visibility. You know that feeling
when your device works perfectly on your desk but starts acting weird once
you've deployed? Yeah, I've been there a few times.

So I started collecting notes about the patterns and tools that helped me the
most when building embedded applications. Nothing groundbreaking here - just
practical stuff that made my life easier and might help you too:

Sanity Check: Finding Your I2C Devices
---------------------------------------

When starting up, checking all addresses to see if the expected devices are
connected helps validate that there are no mechanical problems or connection
issues with the I2C devices:

.. code-block:: rust

  for addr in 0..=127 {
      if let Ok(_) = debug_i2c.write(addr, &[0]).await {
          info!("Found device at address: 0x{:02x}", addr);
      }
  }


Playing Nice: Sharing I2C Between Tasks
------------------------------------------

Sharing I2C can be problematic in embedded Rust. For that, I normally suggest
using the embedded-hal shared_bus traits and sharing using the Embassy Mutex,
like this:

.. code-block:: rust

  use embassy_embedded_hal::shared_bus::asynch::i2c::I2cDevice;
  use embassy_sync::blocking_mutex::raw::NoopRawMutex;
  use embassy_sync::mutex::Mutex;

  let i2c_bus = Mutex::<NoopRawMutex, _>::new(i2c);
  let device_1_i2c = I2cDevice::new(&i2c_bus);
  let device_2_i2c = I2cDevice::new(&i2c_bus);

TIP: I use NoopRawMutex for reading because it has zero overhead when there are no
writes. For writing, I normally use ThreadModeMutex or CriticalSectionMutex
to prevent data races.

Juggling Events: Async Select to the Rescue
-------------------------------------------

When using Embassy, the async phase is more important than anything. When
reading multiple UARTs or waiting for multiple events, waiting for futures can
be problematic. Embassy's `select` allows the code to wait for any kind of event:

.. code-block:: rust

  use embassy_futures::select::{select, Either};
  ...

  match select(connection.next(), receiver.receive()).await {
      Either::First(event) => info!("Got connection event"),
      Either::Second(msg) => info!("Got new message"),
  }

Simple Task Communication with Channels
----------------------------------------

When two or more main tasks are part of the microcontroller and there is no
need for DMA, I recommend using Embassy channels. They provide a nice
abstraction that enables sharing information across tasks without problems and
race conditions. The computational overhead isn't that high.

.. code-block:: rust

    static CHANNEL: Channel<CriticalSectionRawMutex, Messages, 32> = Channel::new();

    let sender = CHANNEL.sender();
    let receiver = CHANNEL.receiver();

    let sender_future = async {
        let mut counter = 0;
        loop {
            info!("Sender: sending {}", counter);
            sender.send(Messages::Internal(counter)).await;
            Timer::after(Duration::from_secs(1)).await;
        }
    };

    let receiver_future = async {
        loop {
            let value = receiver.receive().await;
            match value {
                Messages::Internal(x) => info!("Receiver: got Internal {:?}", x),
                Messages::LOG(x) => info!("Receiver: got LOG {:?}", x),
            }
        }
    };

Picking the Right Chip
-----------------------

When designing a new device, selecting the right board is important. For
example:

**ESP32-C6**: This RISC-V microcontroller supports the IMAC instruction set, where:
    - I: Base integers
    - M: Integer multiplication
    - A: Atomic operations
    - C: Compressed instructions

If your app uses relies heavily on f32 operations, you might want to consider a chip with
floating-point support like the RP3050.

**nRF52840** has floating-point operations available but only 256KB of RAM
compared to the ESP32-C6's 512KB. What matters more for your application -
computation speed or memory usage? For battery-powered devices, fewer CPU
cycles often means better battery life.

These are a few of my go-to tips when I build something new in an embedded
application. Hope this helps you get started!
