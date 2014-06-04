# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"
APP_HOST = "33.33.33.2"
APP_HOSTNAME = "caniusepython3.local"
ANSIBLE_ROOT = "deploy"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
    config.vm.box = "ubuntu/trusty64"
    config.vm.hostname = APP_HOSTNAME
    config.hostsupdater.aliases = ["flower." + APP_HOSTNAME]
    config.vm.network "private_network", ip: APP_HOST
    config.ssh.forward_agent = true

    # Configure provider
    config.vm.provider :virtualbox do |vb|
      vb.gui = false
      vb.customize ["modifyvm", :id, "--memory", "2048"]
      vb.customize ["modifyvm", :id, "--name", APP_HOSTNAME]
      vb.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
      vb.customize ["modifyvm", :id, "--natdnsproxy1", "on"]
    end

    config.vm.provision "ansible" do |ansible|
        ansible.playbook = ANSIBLE_ROOT + "/caniusepython3.yml"
        ansible.inventory_path = ANSIBLE_ROOT + "/inventory/dev.ini"
        # ansible.ask_vault_pass = true
        ansible.limit = 'all'
        ansible.sudo = true
        ansible.sudo_user = "root"
    end
end
