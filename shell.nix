with import <nixpkgs> {};
stdenv.mkDerivation {
  name = "env";
  buildInputs = [
    ruby.devEnv
    git
    sqlite
    libpcap
    postgresql
    libxml2
    libxslt
    pkg-config
    bundix
    gnumake
    mariadb-client
    krb5Full.dev
  ];

  shellHook = ''
  alias rails='bundle exec rails'
  alias rake='bundle exec rake'
  '';
}

