# How to Set Up with Nginx

```
USER1=user1
UNIX_SOCKET_PATH=/home/${USER1}/data/var/${USER1}.sock

sudo python -c "import socket as s; sock = s.socket(s.AF_UNIX); sock.bind('${UNIX_SOCKET_PATH}')"

sudo setfacl -m u:www-data:rw ${UNIX_SOCKET_PATH}

sudo setfacl -m u:${USER1}:rw ${UNIX_SOCKET_PATH}
```

Use HTTPS for git clone instead of SSH. SSH clone will require credentials, while HTTPS will not.

Set up firewall and allow only Telegram:

```
sudo ufw status

sudo ufw allow proto tcp from 149.154.167.0/24 to any port 443
```

```
virtualenv -p python3 venv
```

* http://www.blog.trackets.com/2014/05/17/ssh-tunnel-local-and-remote-port-forwarding-explained-with-examples.html
* https://unix.stackexchange.com/questions/34004/how-does-tcp-keepalive-work-in-ssh
* https://github.com/SECTHEMALL/log2iptables
* https://help.ubuntu.com/lts/serverguide/firewall.html
* https://db-ip.com/all/149.154.167