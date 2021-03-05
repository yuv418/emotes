{ config, lib, pkgs, ... }:

{
  imports = [
    ./.
  ];
#virtualisation.graphics = true;
    #services.xserver.enable = true;
    #services.xserver.desktopManager.lxqt.enable = true;

   environment.systemPackages = [ pkgs.wget pkgs.python3 pkgs.firefox ];

  services.emotes = {
    enable = true;
  };
}
