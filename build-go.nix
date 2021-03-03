with import <nixpkgs> {};

buildGoModule rec {
        pname = "img";
        version = "0.5.11";
        vendorSha256 = null;
        buildInputs = [ libseccomp ];
        src = fetchFromGitHub {
          owner = "genuinetools";
          repo = "img";
          sha256 = "0r5hihzp2679ki9hr3p0f085rafy2hc8kpkdhnd4m5k4iibqib08";
          rev = "v${version}";
        };
	buildPhase = ''
	    patchShebangs .
	    make ${toString makeFlags} img 
	'';
	makeFlags = [ "BUILDTAGS+=seccomp" ];
        build-cache-failures = true;
      }
