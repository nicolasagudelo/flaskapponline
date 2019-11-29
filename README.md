# FlaskAppOnline

Deployment of a Flask application using Ansible playbooks with Ubuntu 18.04

## Table of Contents

- [FlaskAppOnline](#flaskapponline)
  * [Getting Started](#getting-started)
    + [Prerequisites](#prerequisites)
    + [Installing](#installing)
  * [Deploying the app](#deploying-the-app)
  * [Ansible directory](#ansible-directory)
  * [Built With](#built-with)
  * [Authors](#authors)
  * [References](#references)

## Getting Started

**Keep in mind the following instructions are for systems with Ubuntu 18.04 and may vary for different Linux distributions**

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

You can find a running version of this app [here](https://ormucotest.tk)

![Web app](https://i.imgur.com/9pWGYoR.png)

### Prerequisites

* One Ansible control host: this is the machine you will use to connect and control the workstation hosts.
    * A non-root user with sudo privileges
    * An SSH keypair associated with this user.
* One or more Ansible workstation hosts: this will be the machines that your control host will be controlling. For more information on how to do this, you can check [How to Install and Configure Ansible on Ubuntu 18.04](https://www.digitalocean.com/community/tutorials/how-to-install-and-configure-ansible-on-ubuntu-18-04)
    * Add the SSH keypair associated with your control host user to the __authorized keys__ directory of a system user on your workstation host. If you are not sure how to do this you can find a more detailed guide here: [How to set up SSH Keys on Ubuntu 18.04](https://www.digitalocean.com/community/tutorials/how-to-set-up-ssh-keys-on-ubuntu-1804)
    * If you are using platforms such as  AWS's EC2 or  Google Cloud Platform Compute Engine to create virtual machines for your workstation hosts you may be able to add your ssh using these platforms. A guide on how to do that for Google Cloud Platform can be found [here](https://cloud.google.com/compute/docs/instances/adding-removing-ssh-keys#project-wide) for all your instances or [here](https://cloud.google.com/compute/docs/instances/adding-removing-ssh-keys#instance-only) for specific instances.

### Installing

Once you've finished configuring ansible on your control host and can connect to your workstation host(s) using SSH you can proceed to deploy the application for this:

 1. Either clone or download the project files from this repository to your Ansible control host if you want you can take just the Ansible folder since it's the only one we are going to need to deploy the app.
 2. Take the public IP(s) of your workstation host(s) and add them to your Ansible inventory on your control host, the default location of your inventory is __/etc/ansible/hosts__ use nano or any text editor you like to do so. Your inventory will look something similar to this:

```
# Ex 1: Ungrouped hosts, specify before any group headers.

mail.example.com
your.host.ip.address

# Ex 2: A collection of hosts belonging to the 'webservers' group

[webservers]
your.host.ip.address
foo.example.com
bar.example.com

# Ex 3: A collection of database servers in the 'dbservers' group

[dbservers]
one.example.com
two.example.com
three.example.com
```

The heading in brackets are group names that you can use to classify your hosts and to control multiple hosts at the same time, it is not mandatory to use them but they are very useful.

You can also add aliases to your hosts to control them individually just write them before your host's domain or IP address and add the ansible_host attribute:

```
[webservers]
alias1 ansible_host=your.host.ip.address
host1 ansible_host=foo.example.com
host2 ansible_host=bar.example.com

```

For more information regarding Ansible inventory: [How to build your inventory](https://docs.ansible.com/ansible/latest/user_guide/intro_inventory.html#how-to-build-your-inventory)

3. __If__ you are going to add SSL to the web app you need to go into __ansible/certbot.yml__ and modify the last line adding your email after the --email flag, and the IP of your workstation host where you are going to deploy the application after the -d flag, you can add multiple -d flags if you have domain names associated to this IP and want to add the SSL certificate to them too.

    __If not__ then go into __ansible/main.yml__ and either delete or comment the line related to certbot configuration: ___- include: certbot.yml___

If you want a domain name you can get one for free [here](https://my.freenom.com)

4. Finally open __myflaskapp__ file in __/ansible__ directory and look for the ___server_name___ directive, after the directive,  write the domain name of your site. If you don't have one you can leave example.com
```
server {
    listen       80;
    server_name  example.org www.example.org  "";
    ...
}
```

## Deploying the app

Once you've finished with the configuration steps you are ready to deploy the app. Open your terminal on your control host machine and head into the folder where the ansible playbooks are ``.../ansible``

Test the connection with your workstation hosts with the following command:

``ansible all -m ping -u root``

With this, you'll check if your control host has access to your workstation hosts. You should get an output similar to this:

```
server1 | SUCCESS => {
    "changed": false, 
    "ping": "pong"
}
server2 | SUCCESS => {
    "changed": false, 
    "ping": "pong"
}
server3 | SUCCESS => {
    "changed": false, 
    "ping": "pong"
}
```

In case you are receiving a host unreachable error:
* Check your inventory and make sure everything is correct
* Check if you can connect to your workstation host using SSH

1. If everything is fine head to ___main.yml___ file and open it with your favorite text editor.
2. After the ___-hosts___ attribute, write either: 
    * The group name of the hosts you want to reach as it appears on your inventory
    * The aliases of the hosts you want to reach
    * The IPs of the hosts you want to reach
    * __all__ to reach all hosts in your inventory

Execute ___main.yml___ to do so you need to run the following command

```
`ansible-playbook -i /etc/ansible/hosts git-setup.yml`
```
_Note_: If your inventory is not in ___/etc/ansible/hosts___ change this path on the command with the path to your inventory

_Note_: if you are not in the directory where the playbooks are you'll need to specify the full path of the playbook to execute it.

The playbook will then start to execute you should start to see output similar to this:

```
PLAY [host1] *******************************************************************

TASK [Gathering Facts] *********************************************************
ok: [host1]

TASK [Update repositories cache] ***********************************************
changed: [host1]

TASK [install nginx] ***********************************************************
changed: [host1]
.
.
.
```

Once it finishes you should be able to connect to the web app using either the public Ip address of the workstation host or the domain name if you have one, in case you used the certbot.yml playbook your website should have SSL certificates.

The files related to the app will be installed in the following directory ___/var/www/html/mywebapp___

## Ansible directory

```
.
├── aptinstall.yml
├── certbot.yml
├── database.yml
├── flaskapp.sql
├── git.yml
├── gunicorn.service
├── install.yml
├── main.yml
├── myflaskapp
├── mysqlconf.yml
├── nginx.conf
├── nginx-gunicorn.yml
├── nginx.yml
├── pip.yml
└── ufw.yml
```

The Ansible directory contains all the playbooks used to deploy the application as well as the required configuration files to make sure everything works, keep in mind this files will work to deploy __this__ application, some of them can be used as a template for other projects. However, you may need to add or remove things if you are planning on deploying something else.

A brief explanation of the playbooks follows:

* main.yml: Is the main playbook here we specify the hosts and is responsible for orchestrating everything.
* nginx.yml: Installs and configures Nginx service.
* mysqlconf.yml: Sets the root password for the root user before installing MySQL
* apt-install.yml: Is responsible for installing the packages needed to build the application
* pip.yml: Is responsible for installing the python related packages to build the application.
* database.yml: Here the database for the application will be built 
The database will consist of only one table described as shown below:
```
+----------------+-------------+------+-----+---------+----------------+
| Field          | Type        | Null | Key | Default | Extra          |
+----------------+-------------+------+-----+---------+----------------+
| Id             | smallint(6) | NO   | PRI | NULL    | auto_increment |
| Name           | varchar(20) | NO   | UNI | NULL    |                |
| Favorite_Color | varchar(20) | NO   |     | NULL    |                |
| CatOrDog       | varchar(3)  | NO   |     | NULL    |                |
+----------------+-------------+------+-----+---------+----------------+
```
* git.yml: Get the files for the application from GitHub
* Nginx-gunicorn.yml: This playbook will configure both Nginx and Gunicorn for the application.
* ufw.yml: Configure the rules for the firewall of the application.
* certbot.yml: Get the SSL certificate for the website.
## Built With

* [Flask](https://palletsprojects.com/p/flask/)
* [Ansible](https://docs.ansible.com/)
* [Nginx](https://www.nginx.com/)
* [Gunicorn](https://gunicorn.org/)

## Authors

* **Nicolas Agudelo**

## References

Cool sites if you want more information:

* https://docs.ansible.com/ansible/latest/index.html
* https://www.e-tinkers.com/2018/08/how-to-properly-host-flask-application-with-nginx-and-guincorn/
* https://www.ssl.com/faqs/faq-what-is-ssl/
* https://letsencrypt.org/getting-started/
* https://www.w3schools.com/
* https://www.fullstackpython.com/flask.html
* https://www.digitalocean.com/community/tutorials/how-to-setup-a-firewall-with-ufw-on-an-ubuntu-and-debian-cloud-server
* https://www.digitalocean.com/community/tutorials/how-to-install-and-configure-ansible-on-ubuntu-18-04
* https://www.digitalocean.com/community/tutorials/how-to-set-up-ssh-keys-on-ubuntu-1804
* https://certbot.eff.org/docs/using.html
* http://nginx.org/en/docs/http/server_names.html

