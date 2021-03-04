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
      group = mkOption {
	type = types.str;
	default = "emotes";
	description = "Emotes group";
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

    users.users = optionalAttrs (cfg.user == "emotes") {
      emotes = {
        group = cfg.group;
        home = cfg.dir;
      };
    };
    users.groups = optionalAttrs (cfg.group == "emotes") {
      emotes = {};
    };

      services.mysql = {
        enable = true;
        package = pkgs.mariadb;
        ensureDatabases = [ cfg.db.name ];
        ensureUsers = [
          {
            name = cfg.db.user;
            ensurePermissions = {
              "${cfg.db.name}.*" = "select, lock tables";
            };
          }
        ];
      };

      systemd.tmpfiles.rules = [
        "d '${cfg.dir}' 0750 ${cfg.user} ${cfg.group} - -"
        "d '${cfg.dir}/cache' 0750 ${cfg.user} ${cfg.group} - -"
        "d '${cfg.dir}/log' 0750 ${cfg.user} ${cfg.group} - -"
        "d '${cfg.dir}/data' 0750 ${cfg.user} ${cfg.group} - -"
      ];

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
            EMOTES_DBSTRING = "mysql2://${auth}${cfg.db.host}/${cfg.db.name}";
            EMOTES_DATA = "${cfg.dir}/data";
            RAILS_CACHE = "${cfg.dir}/cache";
            RAILS_ENV = "production";
	    PIDFILE = "${cfg.dir}/emotes.pid";
            NIXOS="1";
            RAILS_PROD_LOGFILE = "${cfg.dir}/log/production.log";
          };
          serviceConfig.WorkingDirectory = emotes;
        };
      in {
        emotes-setup = {
          before = [ "emotes" ];
          script = "${bundle} exec rails db:migrate";
        } // sharedCfg;

        emotes = {
          script = "${bundle} exec rails server";
        } // sharedCfg;
      };
  };
}
