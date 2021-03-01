{ stdenv, bundlerEnv, ruby }:
let
  gems = bundlerEnv {
    name = "your-package";
    inherit ruby;
    gemdir  = ./.;
  };
in stdenv.mkDerivation {
  name = "your-package";
  src = ./.;
  buildInputs = [gems ruby];
  installPhase = ''
    mkdir -p $out
    cp -r $src $out
  '';
}