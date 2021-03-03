with import <nixpkgs> {};

let
in  
    let 
      dockerFilePath = builtins.toString ./.;
      outTag = "emotes:latest";
      buildTag = "emotes:latest";
    in stdenv.mkDerivation 
    {
      name = "emotes-docker.tar.gz";
      src = ./.;
      nativeBuildInputs = [ skopeo docker curl buildah ];
      shellHook = ''
      '';
    buildPhase = ''

  mkdir -p /etc/containers
  cat <<EOF | sudo tee /etc/containers/policy.json
  {
      "default": [
          {
              "type": "insecureAcceptAnything"
          }
      ]
  }
  cat <<EOF | sudo tee /etc/containers/registries.conf
  [registries.search]
  registries = [ 'docker.io' ]
  EOF
  # documentation for this is very disorganized at this point
  # see https://github.com/containers/libpod/blob/master/docs/libpod.conf.5.md
  cat <<EOF | tee $HOME/podman.conf
  conmon_path = [ "$(which conmon)" ]
  events_logger = "file"
  [runtimes]
  runc = [ "$(which runc)" ]
  EOF
  echo $(whoami):100000:65536 | sudo tee /etc/sub{u,g}id
  head /etc/subuid /etc/subgid
  chown root: $(which new{u,g}idmap)
  chmod 4555 $(which new{u,g}idmap)
  ls -l $(which new{u,g}idmap)
  ln -s ${tzdata}/share/zoneinfo/America/New_York /etc/zoneinfo
    echo ${tzdata}
    ls /etc/zoneinfo
    buildah build . -t emotes
        # skopeo --insecure-policy copy "$buildTag" "docker-archive://$out:$outTag"
    '';
    }
