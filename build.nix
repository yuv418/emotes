with import <nixpkgs> {};

let
  gems = bundlerEnv {
    name = "emotes";
    inherit ruby;
    gemdir  = ./api;

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

    gemConfig.mysql2 = attrs: {
      buildInputs = [ libmysqlclient.dev ];
    };
    groups = [ "default" "development" "test" ];
  };
in stdenv.mkDerivation {
  name = "emotes";
  src = ./.;
  buildInputs = [gems gems.bundler gems.wrappedRuby];
  installPhase = ''
    mkdir -p $out
    mkdir -p $out/tmp/{cache,pids,sockets}
    cp -r $src/* $out/
  '';
}
