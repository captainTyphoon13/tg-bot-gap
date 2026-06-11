{ pkgs }:
{
  deps = [
    pkgs.python312
    pkgs.python312Packages.pip
    pkgs.libpq
    pkgs.gcc
  ];
}
