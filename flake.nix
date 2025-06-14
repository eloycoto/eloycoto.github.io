 { 
  description = "blog";
  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };
  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem
      (system:
        let
          pkgs = import nixpkgs {
            inherit system;
          };

          python-packages = ps: with ps; [
            pelican
          ];

        in
        with pkgs;
        {
          devShells.default = mkShell {
            buildInputs = [
              (pkgs.python3.withPackages python-packages)
              pkgs.gnumake
              pkgs.harper
            ];
          };
        }
      );
}
