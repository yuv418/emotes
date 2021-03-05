{ config, lib, pkgs, ... }:

{
  imports = [
    ./.
  ];

  environment.systemPackages = [ pkgs.wget pkgs.python3 pkgs.firefox ];

  services.emotes = {
    enable = true;
    port = 3000;
  };
}
