# Running with ansible

This app can be managed across several machines using ansible.

To follow these instructions, you will need to have ansible and a suitable version of python installed on the controller machine, see instructions [here](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html?extIdCarryOver=true&sc_cid=701f2000001OH7YAAW). Since ansible does not run on linux machines, you may need to use a virtual machine for this. You will also need this ansible folder copied over to the controller, or a copy of the codebase downloaded on to the controller using git.

From your controller machine, check you can SSH into your host machines and copy your SSH key across to the hosts.

Before you can run with ansible, you'll need to make some changes to files in this folder:
 - Change the IP addresses in the `inventory.ini` file to match the host IP addresses you are using
 - If the user you are logging in as on the host machines is not called ec2-user, you will need to change this in `playbook.yml` and `todoapp.service`
 - If you want to run the code on another branch (not main), change this under version under the task "Check out latest version of todoapp" in `playbook.yml`

You are now ready to run the playbook
```
ansible-playbook playbook.yml -i inventory.ini
```

The playbook will prompt you for your mongo connection string and database name. You can obtain these as described in the README. It should then run through the setup stages and the todoapp should be accessible on the host IP addresses.
