# SPDX-License-Identifier: MIT
{ sources ? import ./nix/sources.nix }:
let
  inherit (sources) nixpkgs gitignore;
  pkgs = import nixpkgs { };
  gitignoreSource = (import gitignore { }).gitignoreSource;
  inherit (pkgs) python3 python3Packages nodePackages yarn;
in
python3Packages.buildPythonPackage {
  name = "comicindex";

  src = gitignoreSource ./.;

  propagatedBuildInputs = with python3Packages; [
    (callPackage ./overpy.nix { })
    requests
    brotli
    zopfli
    jinja2
  ];

  nativeBuildInputs = (with python3Packages; [ pylint autopep8 ])
    ++ [
    yarn
    nodePackages."@vue/cli"
  ];

  doCheck = false;
}
