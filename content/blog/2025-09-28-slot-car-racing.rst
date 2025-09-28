Rust, PIO, and Racing: A Personal Project
==========================================
:date: 2025-09-28 16:30
:language: en-GB
:author: eloycoto
:tags: hardware, rust
:head: Real-Time Racing Data with Rust, RP2350, and a DIY Dashboard
:index_title: Rust, PIO, and Racing: A Personal Project
:metatitle: Creating a WRC-Style Dashboard for Slot Car Racing
:metatags: hobby electronics, race timing, datalogger, Rust Embassy, dashboard, embedded systems
:description: How I used Rust Embassy, RP2350 PIO, and Ratatui to transform basic slot car timing into a real-time racing experience.

A little while ago I finished up a personal project that made me genuinely happy. It brought together few things I enjoy: tinkering with hardware, Rust, and slot car racing.

I’ve been into slot cars for about 20 years now. In my village the scene is surprisingly big, and the competitions can get intense. Naturally, being a nerd, I couldn’t just race, I wanted to understand the details behind each different lap. That curiosity led me straight into another rabbit hole.

.. image:: /img/slot_first_dashboard_blog.jpg
   :alt: Slot First Dashboard
   :align: center

The standard setup we use relies on a `commercial timing tool <https://scaleauto-slot.com/ds-electronic/>`_ with a light sensor that triggers when a car crosses the line. It works fine, but the data is only available at the very end of the race. No useful lap-by-lap details, no real-time insight, nothing live for others. For someone like me, that was just begging to be improved.

The timing device had an RS232 interface, which I’d experimented with before for central counting. This time I decided to go further. With the help of some custom hardware and the RP2350’s PIO interfaces, I built a datalogger. To make the data accessible, I hooked up a budget-friendly OrangePI with HDMI output. On top of that, I wrote a `Ratatui <https://ratatui.rs>`_ application to create a live dashboard.

The result is something like a WRC-style dashboard: live, interactive, and fun for everyone participating in the race. Instead of waiting until the end, we now get a clear picture of what’s happening as it happens.

Here’s how the setup looks:

- RP2350 device as datalogger:
    - Rust Embassy as framework
    - PIO as datalogger
    - Custom board with RS232 interfaces

- OrangePI
    - Ratatui app for dashboard display
    - Armbian as distro in read-only mode

The first working prototype looked like this:

.. image:: /img/slot_first_proto_blog.jpg
   :alt: Slot First Prototype
   :align: center

One of the neatest parts is how the memory works. All data is kept in RAM just for the duration of the race. Exporting is optional, but nothing ever writes to the SD card. The moment the TV powers on, the whole system boots up ready to go.

Building this project was fun. I learned a ton about the RP2350’s PIO ports, got to stretch my Rust and PCB design skills, and in the end created something my friends and I can actually use. Honestly, that combination of learning and sharing the fun is what makes this project so fun!
