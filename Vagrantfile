# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  # Every Vagrant virtual environment requires a box to build off of.
  config.vm.box = "ubuntu/trusty32"

  # Create a private network, which allows host-only access to the machine
  # using a specific IP.
  config.vm.network "private_network", ip: "192.168.33.10"

  # Provider-specific configuration so you can fine-tune various
  # backing providers for Vagrant. These expose provider-specific options.
  # Example for VirtualBox:
  #
  # config.vm.provider "virtualbox" do |vb|
  #   # Don't boot with headless mode
  #   vb.gui = true
  #
  #   # Use VBoxManage to customize the VM. For example to change memory:
  #   vb.customize ["modifyvm", :id, "--memory", "1024"]
  # end
  config.vm.provision "shell" do |s|
    s.inline = <<SCRIPT
apt-get update
apt-get install -y python-pip python3-pip python-dev python3-dev build-essential libssl-dev
pip2 install static werkzeug gunicorn gevent-websocket
pip2 install  --install-option="--install-scripts=/home/vagrant/bin2/" uwsgi
pip2 install -e /vagrant/
pip3 install static werkzeug
pip3 install  --install-option="--install-scripts=/home/vagrant/bin3/" uwsgi
pip3 install -e /vagrant/
SCRIPT
  end
end
