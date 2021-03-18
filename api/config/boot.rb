ENV['BUNDLE_GEMFILE'] ||= File.expand_path('../Gemfile', __dir__)

require "bundler/setup" # Set up gems listed in the Gemfile.
if ENV["NIXOS"] == "1" && ENV["RAILS_TMPDIR"] # Only load if NIXOS is not set or if RAILS_TMPDIR is set and NIXOS is set
  require 'bootsnap'
  Bootsnap.setup(
    cache_dir: ENV["RAILS_TMPDIR"]
  )
else
  require "bootsnap/setup" # Speed up boot time by caching expensive operations.
end
