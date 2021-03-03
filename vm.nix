{ config, lib, pkgs, ... }:

{
  imports = [
    ./.
  ];

  services.emotes = {
    enable = true;
  };
}
