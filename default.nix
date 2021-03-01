with import <nixpkgs> {};

let
  gems = bundlerEnv {
    name = "emotes";
    inherit ruby;
    gemdir  = ./.;

    # Stolen from https://github.com/emptyflask/rails-nix/blob/master/nix/rubyenv.nix
    gemConfig.pg = attrs: {
      buildInputs = [ postgresql ];
    };

    gemConfig.sqlite3 = attrs: {
      buildInputs = [ sqlite ];
    };

    gemConfig.nokogiri = attrs: {
      buildInputs = [ libiconv zlib ];
    };

    gemConfig.sassc = attrs: {
      buildInputs = [ libsass ];
      shellHook = ''
        export SASS_LIBSASS_PATH=${libsass}
      '';
    };
  };
in stdenv.mkDerivation {
  name = "emotes";
  src = ./.;
  buildInputs = [gems ruby];
  installPhase = ''
    mkdir -p $out
    cp -r $src $out
  '';
}