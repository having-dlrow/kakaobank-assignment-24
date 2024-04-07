{ pkgs }: {
    deps = [
        pkgs.unzip
        pkgs.python310Packages.setuptools
        pkgs.python310Packages.pip
        pkgs.python310Packages.virtualenv
        pkgs.python310
    ];
    env = {
    LD_LIBRARY_PATH = pkgs.lib.makeLibraryPath [
      pkgs.stdenv.cc.cc.lib
    ];
    PYTHONBIN = "${pkgs.python310}/bin/python3.10";
    LANG = "en_US.UTF-8";
  };
}