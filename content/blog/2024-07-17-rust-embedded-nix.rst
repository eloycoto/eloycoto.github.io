Nix flake for embedded programming
==================================

:date: 2024-07-17 12:00
:language: en-GB
:author: eloycoto
:head: Nix flake for embedded programming
:index_title: Nix flake for embedded programming
:metatitle: Using Nix for Rust Embedded Development
:tags: Rust, embedded, nix
:metatags: Rust, embedded programming, Nix flake, development platform, Rust development, Nix integration, GitHub Actions
:description: Discover the advantages of using Nix as a development platform for Rust embedded applications, including better integration with editors and simplified workflows.
:keywords: Rust, embedded development, nix

Lately, I've been using Nix more and more as a development platform. Docker has
been great, but Nix allows better integration with editors. When I revisit
older projects, Nix is a reliable way to ensure they work.

Embedded programming is not part of my day-to-day work, so having a Nix flake
is a real advantage, especially when I share setups in our local Hackspace. The
main thing about embedded programming is that you need a few programs to help
develop and debug applications.

For Rust embedded applications, I find the following base Flake useful, which I
extend based on my project's needs:

.. code-block:: nix

    {
      inputs = {
        nixpkgs.url = "github:NixOS/nixpkgs/nixos-24.05";
        flake-utils.url = "github:numtide/flake-utils";
        rust-overlay.url = "github:oxalica/rust-overlay";
      };
      outputs = { self, nixpkgs, flake-utils, rust-overlay }:
        flake-utils.lib.eachDefaultSystem
          (system:
            let
              overlays = [ (import rust-overlay) ];
              pkgs = import nixpkgs {
                inherit system overlays;
              };
            in
            with pkgs;
            {
              devShells.default = mkShell {
                buildInputs = with pkgs; [
                  (rust-bin.stable.latest.default.override {
                    extensions = [ "rust-src" ];
                    targets = [ "thumbv6m-none-eabi" ];
                  })
                ] ++  [
                  openocd
                  rust-analyzer
                  rustfmt
                  probe-run
                  flip-link
                  probe-rs
                  kicad
                ];
              };
            }
          );
    }

To get the environment, simply run:

.. code-block:: nix

    nix develop .

From there, you can run all your commands as usual:

.. code-block:: nix

    cargo run
    openocd -f openocd.cfg

This simplifies my workflow and helps run things on other computers or in
GitHub Actions.

Hope this helps.
