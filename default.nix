{ config, lib, pkgs, ... }:

let
  cfg = config.services.emotes;
in with lib; {
  options = {
    services.emotes = {
      enable = mkEnableOption "Emotes on Rails";

      user = mkOption {
        type = types.str;
        default = "emotes";
        description = "User to run service as";
      };
      dir = mkOption {
        type = types.str;
        default = "/var/emotes";
        description = "Data directory";
      };

      db = {
        user = mkOption {
          type = types.str;
          default = "emotes";
          description = "DB user";
        };
        password = mkOption {
          type = types.str;
          default = "";
          description = "DB password";
        };
        name = mkOption {
          type = types.str;
          default = "emotes";
          description = "Name of DB";
        };
        host = mkOption {
          type = types.str;
          default = "localhost";
          description = "Emotes DB location";
        };
      };
    };
  };

  config = mkIf (cfg.enable) {

      services.mysql = {
        enable = true;
        package = pkgs.mariadb;
        ensureUsers = [
          {
            name = cfg.db.user;
            ensurePermissions = {
              "${cfg.db.name}.*" = "select, lock tables";
            };
          }
        ];
      };

      systemd.services = with pkgs; let
        emotes = import ./build.nix;
        bundle = "${emotes}/bin/bundle";

        sharedCfg = {
          enable = true;
          wantedBy = [ "multi-user.target" ];
          after = [ "networking.service" "mysql.service" ];
          environment = let
            auth = if cfg.db.password != "" then "${cfg.db.username}:${cfg.db.password}@" else "";
          in {
            EMOTES_DBSTRING = "mysql://${auth}${cfg.db.host}/${cfg.db.name}";
            EMOTES_DATA = cfg.dir;
            RAILS_ENV = "production";
          };
          serviceConfig.WorkingDirectory = emotes;
        };
      in {
        emotes-setup = {
          before = [ "emotes" ];

          script = "${bundle} exec db:migrate";
        } // sharedCfg;

        emotes = {
          script = "${bundle} exec rails server";
        } // sharedCfg;
      };
  };
}
