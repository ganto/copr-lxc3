#!/usr/bin/env ruby

# Create the vagrant-lxc sudo-wrapper from the template.
# Roughly taken from lib/vagrant-lxc/command/sudoers.rb
#
# Michael Adam <obnox@samba.org>

require 'tempfile'

require "vagrant/util/template_renderer"


class CreateWrapper
  class << self
    def run!(argv)
      raise "Argument missing" unless(argv)

      template_root = argv.shift
      wrapper_dst = "./vagrant-lxc-wrapper"

      wrapper_tmp = create_wrapper!(template_root)

      system "cp #{wrapper_tmp} #{wrapper_dst}"
      puts "#{wrapper_dst} created"
    end

    private

    # This requires vagrant 1.5.2+
    # https://github.com/mitchellh/vagrant/commit/3371c3716278071680af9b526ba19235c79c64cb
    def create_wrapper!(template_root)
      wrapper = Tempfile.new('lxc-wrapper').tap do |file|
        template = Vagrant::Util::TemplateRenderer.new(
          'sudoers.rb',
          #:template_root  => Vagrant::LXC.source_root.join('templates').to_s,
          #:template_root  => "/usr/share/vagrant/gems/gems/vagrant-lxc-1.1.0/templates",
          :template_root  => template_root,
          :cmd_paths      => build_cmd_paths_hash,
          #:pipework_regex => "#{ENV['HOME']}/\.vagrant\.d/gems/gems/vagrant-lxc.+/scripts/pipework"
          :pipework_regex => "/usr/share/vagrant/gems/gems/vagrant-lxc.+/scripts/pipework"
        )
        file.puts template.render
      end
      wrapper.close
      wrapper.path
    end

    # for fedora, we know that all these commands
    # are found in /usr/bin ...
    def build_cmd_paths_hash
      {}.tap do |hash|
        %w( which cat mkdir cp chown chmod rm tar chown ip ifconfig brctl ).each do |cmd|
          #hash[cmd] = `which #{cmd}`.strip
          hash[cmd] = "/usr/bin/#{cmd}"
        end
        #hash['lxc_bin'] = Pathname(`which lxc-create`.strip).parent.to_s
        hash['lxc_bin'] = "/usr/bin"
      end
    end
  end
end

CreateWrapper.run!(ARGV)
