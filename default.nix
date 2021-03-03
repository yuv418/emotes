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

    virtualisation.oci-containers = { # Don't bother buliding it with Nix, haha.
      containers.emotes = {
        imageFile = pkgs.dockerTools.buildImage {
          fromImageName = "ruby";
          fromImageTag = "2.7.2-alpine3.12";

          name = "emotes";
          runAsRoot = ''
          apk add mysql-client
          '';
        };
        image = "emotes"
        autoStart = true;
        extraOptions = [ "--network=host" ];
        };
      };
    };
    /*

      systemd.services = with pkgs; let
        bundle = "${pkgs.bundler}/bin/";
        emotes = import ./build.nix;

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

          script = "bin/setup";
        } // sharedCfg;

        emotes = {
          script = "bin/start";
        } // sharedCfg;
      };*/
}
