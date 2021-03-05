{ config, lib, pkgs, ... }:

{
  imports = [
    ./.
  ];

  environment.systemPackages = [ pkgs.wget pkgs.python3 pkgs.firefox ];

  services.mysql.enable = true;
  services.mysql.package = pkgs.mariadb;
  services.emotes = {
    enable = true;
    port = 3000;
  };
}
