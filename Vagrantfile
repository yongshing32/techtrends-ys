Vagrant.configure("2") do |config|
  config.vm.provision "shell",
    inline: <<-SHELL
      # set up the default terminal
      ENV["TERM"]="linux"

      # set minimum version for Vagrant
      Vagrant.require_version ">= 2.2.10"
      
      # Copy Kubernetes manifests
      mkdir /vagrant/kubernetes
      cp /vagrant/namespace.yaml /vagrant/kubernetes/
      cp /vagrant/deploy.yaml /vagrant/kubernetes/
      cp /vagrant/service.yaml /vagrant/kubernetes/

      # Install packages
      zypper update -y
      zypper install -y apparmor-parser
    SHELL

  # Set the image for the Vagrant box
  config.vm.box = "opensuse/Leap-15.2.x86_64"
  # Set the image version
  config.vm.box_version = "15.2.31.632"

  # Forward the ports from the guest VM to the local host machine
  # Forward more ports, as needed
  config.vm.network "forwarded_port", guest: 8080, host: 8080
  config.vm.network "forwarded_port", guest: 6111, host: 6111
  config.vm.network "forwarded_port", guest: 6112, host: 6112

  # Set the static IP for the Vagrant box
  config.vm.network "private_network", ip: "192.168.50.4"
  
  # Configure the parameters for VirtualBox provider
  config.vm.provider "virtualbox" do |vb|
    vb.memory = "4096"
    vb.cpus = 4
    vb.customize ["modifyvm", :id, "--ioapic", "on"]
  end
end
