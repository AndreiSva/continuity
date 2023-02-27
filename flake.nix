# this took me way too long to write

{
  description = "A flake for building the continuity simulation";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixpkgs-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        prog_name = "continuity";
        pkgs = nixpkgs.legacyPackages.${system}; in
      {
        packages = rec {
          continuity = pkgs.python3Packages.buildPythonPackage rec {
            name = "continuity";
            src = ./.;
            propagatedBuildInputs = with pkgs.python3Packages; [
              numpy
              pygame
            ];
          };
          default = continuity;
        };

        apps = rec {
          hello = flake-utils.lib.mkApp {
            drv = self.packages.${system}.continuity;
            name = prog_name;
          };
          default = hello;
        };
        
      }
    );
}
