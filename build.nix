with import <nixpkgs> {};

let
in  
    let 
      dockerFilePath = builtins.toString ./.;
      outTag = "emotes:latest";
      buildTag = "emotes:latest";
    in runCommandLocal "emotes-docker.tar.gz"
    {
      name = "emotes-docker.tar.gz";
      src = ./.;
      nativeBuildInputs = [ skopeo docker curl ];
      m = fetchurl {
        url = "https://github.com/genuinetools/img/releases/download/v0.5.11/img-linux-amd64";
        sha256 = "1kqcyhcy73kfbzvkkwb7abqfjlw24hz1sjivfs31ix0znp4089lx";
        executable = true;
      };
    } ''
    $m build . -t emotes
        # skopeo --insecure-policy copy "$buildTag" "docker-archive://$out:$outTag"
    ''
