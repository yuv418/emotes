{ config, lib, pkgs, ... }:

{
  imports = [
    ./.
  ];

  virtualisation.docker.enable = true;
  services.emotes = {
    enable = true;
  };
}
