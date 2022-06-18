{
  description = "Factorio-bot";

  inputs = {
    nix2container.url = "github:nlewo/nix2container";
    nixpkgs     = { url = "github:nixos/nixpkgs/nixpkgs-unstable"; };
    flake-utils = { url = "github:numtide/flake-utils"; };
    flake-compat = {
      url = "github:edolstra/flake-compat";
      flake = false;
    };
  };

  outputs = { self, nixpkgs, flake-utils, nix2container, ... }:
    flake-utils.lib.eachDefaultSystem (system: let
      pkgs = import nixpkgs { inherit system; };

      python = pkgs.python310;
      projectDir = ./.;
      overrides = pkgs.poetry2nix.overrides.withDefaults (final: prev: {
        # Python dependency overrides go here
      });

      packageName = "factorio-bot";
      nix2containerPkgs = nix2container.packages.${system};
      in rec {

        packages.${packageName} = pkgs.poetry2nix.mkPoetryApplication {
          inherit python projectDir overrides;
          # Other dependencies here
          propogatedBuildInputs = [];
        };

        # Build container using `nix run .#factorio-bot-container.copyToDockerDaemon`
        packages.factorio-bot-container = nix2containerPkgs.nix2container.buildImage {
          name = "factorio-bot";
          contents = [
            (pkgs.symlinkJoin { name = "root"; paths = [
              packages.${packageName}
              ]; })
          ];
          config = {
            entrypoint = ["factoriobot"];
          };
        };

        defaultPackage = self.packages.${system}.${packageName};
        apps.${system}.${packageName} = packages.${packageName};
        defaultApp = apps.${system}.${packageName};
        devShell = pkgs.mkShell {
          buildInputs = [
            (pkgs.poetry2nix.mkPoetryEnv {
              inherit python projectDir overrides;
            })
            pkgs.python310Packages.poetry
          ];
        };

    });
}