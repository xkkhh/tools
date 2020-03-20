#!/usr/bin/env python
#coding:utf-8
#make in china by xkkhh 2017.11.11 23点23分


import os
import sys

cmd = os.system


def setup_1():
	'''
	cloudstack_setup.py manager
	管理节点设置需要和以下8个文件在同一目录下
	列如:/opt/cloudstack
	然后通过U盘等上传到CentOS6.5里面就行
	cloudstack-agent-4.5.1-shapeblue0.el6.x86_64.rpm
	cloudstack-awsapi-4.5.1-shapeblue0.el6.x86_64.rpm
	cloudstack-baremetal-agent-4.5.1-shapeblue0.el6.x86_64.rpm
	cloudstack-cli-4.5.1-shapeblue0.el6.x86_64.rpm
	cloudstack-common-4.5.1-shapeblue0.el6.x86_64.rpm
	cloudstack-management-4.5.1-shapeblue0.el6.x86_64.rpm
	cloudstack-mysql-ha-4.5.1-shapeblue0.el6.x86_64.rpm
	cloudstack-usage-4.5.1-shapeblue0.el6.x86_64.rpm
	'''
	#hostname
	hostname = 'B-MS.cs'
	cloudstackdir = raw_input('Please input your\'s cloudstackdir:\n') 
	f2 = open('/etc/hosts','a+')
	f2.write('192.168.0.1 '+hostname+'\n192.168.0.2 B-NFS.cs\n192.168.0.3 B-XS1.cs\n192.168.0.4 B-XS2.cs\n')
	f2.close()
	f3 = open('/etc/sysconfig/network','w')
	f3.write('NETWORKING=yes\nHOSTNAME='+hostname)
	f3.close()
	#selinux
	cmd('hostname '+hostname + ' && setenforce 0')
	f4 = open('/etc/selinux/config','w')
	f4.write('SELINUX=permissive\nSELINUXTYPE=targeted')
	f4.close()
	#yum
	cmd('mkdir /opt/CentOS && mount /dev/sr0 /opt/CentOS')
	os.chdir('/etc/yum.repos.d/')
	cmd('rename .repo .bck *')
	f5 = open('cloudstack.repo','w')
	f5.write('[base]\nname=CentOS-dvd-base\nbaseurl=file:///opt/CentOS\nenable=1\ngpgcheck=0\n')
	f5.close()
	cmd('yum clean all && yum repolist all')
	#mysql
	cmd('yum -y install mysql-server')
	f6 = open('/etc/my.cnf','w')
	f6.write("[mysqld]\ndatadir=/var/lib/mysql\nsocket=/var/lib/mysql/mysql.sock\nuser=mysql\nsymbolic-links=0\ninnodb_rollback_on_timeout=1\ninnodb_lock_wait_timeout=600\nmax_connections=350\nlog-bin=mysql-bin\nbinlog-format='ROW'\n[mysqld_safe]\nlog-error=/var/log/mysqld.log\npid-file=/var/run/mysqld/mysqld.pid\n")
	f6.close()
	cmd("service mysqld start && mysqladmin -u root password 'cspassword'")
	#ntp
	f7 = open('/etc/ntp.conf','w')
	f7.write('driftfile /var/lib/ntp/drift\nrestrict default kod nomodify notrap nopeer noquery\nrestrict -6 default kod nomodify notrap nopeer noquery\nrestrict 127.0.0.1\nrestrict -6 ::1\nrestrict 192.168.0.0 mask 255.255.255.0 nomodify notrap\nserver 127.127.1.0\nfudge 127.127.1.0 stratum 10\nincludefile /etc/ntp/crypto/pw\nkeys /etc/ntp/keys\n')
	f7.close()
	#cloudstack-management
	cmd('service ntpd start && yum -y install createrepo && createrepo ' + cloudstackdir)
	f8 = open('/etc/yum.repos.d/cloudstack.repo','a+')
	f8.write('[cloudstack]\nname=cloudstack\nbaseurl=file://' + cloudstackdir + '\nenable=1\ngpgcheck=0')
	f8.close()
	cmd('yum clean all && yum repolist all && yum -y install cloudstack-management')
	#cloudstack-database
	cmd('cloudstack-setup-databases cloud:cspassword@localhost --deploy-as=root:cspassword && cloudstack-setup-management && service iptables stop')
	#start for the system
	cmd('chkconfig mysqld on && chkconfig ntpd on')
	raw_input('######setup ok, please wait for 3 min... \n Please input any key to exit!######')

def setup_2():
	'''
	存储节点直接cloudstack_setup.py uploadvm
	'''
	#set_hostname
	hostname='B-NFS.cs'
	cmd('mkdir -p /export/B_xs /export/B_sec')
	f2 = open('/etc/hosts','a+')
	f2.write('192.168.0.2 '+hostname+'\n192.168.0.1 B-MS.cs\n192.168.0.3 B-XS1.cs\n192.168.0.4 B-XS2.cs\n')  #ะด
	f2.close()
	f3 = open('/etc/sysconfig/network','w')
	f3.write('NETWORKING=yes\nHOSTNAME='+hostname)
	f3.close()
	cmd('hostname '+hostname + ' && setenforce 0')
	#set_selinux
	f4 = open('/etc/selinux/config','w')
	f4.write('SELINUX=permissive\nSELINUXTYPE=targeted')
	f4.close()
	#set_yum
	cmd('mkdir /opt/CentOS && mount /dev/sr0 /opt/CentOS')
	os.chdir('/etc/yum.repos.d/')
	cmd('rename .repo .bck *')
	f5 = open('NSF.repo','w')
	f5.write('[base]\nname=nfs-dvd-base\nbaseurl=file:///opt/CentOS\nenable=1\ngpgcheck=0\n')
	f5.close()
	cmd('/etc/init.d/iptables stop && yum clean all && yum repolist all && chkconfig ntpd on')
	#set_ntp
	f6 = open('/etc/ntp.conf','w')
	f6.write('driftfile /var/lib/ntp/drift\nrestrict default kod nomodify notrap nopeer noquery\nrestrict -6 default kod nomodify notrap nopeer noquery\nrestrict 127.0.0.1\nrestrict -6 ::1\nserver 192.168.0.1\nincludefile /etc/ntp/crypto/pw\nkeys /etc/ntp/keys\n')
	f6.close()
	cmd('chkconfig nfs on && chkconfig rpcbind on')
	f7 = open('/etc/idmapd.conf','w')
	f7.write('[General]\nDomain = .cs\n\n[Mapping]\nNobody-User = nobody\nNobody-Group = nobody\n\n[Translation]\nMethod = nsswitch\n')
	f7.close()
	f8 = open('/etc/exports','w')
	f8.write('/export *(rw,async,no_root_squash,no_subtree_check)')
	f8.close()
	#nfs
	f9 = open('/etc/sysconfig/nfs','w')
	f9.write('RQUOTAD_PORT=875\nLOCKD_TCPPORT=32803\nLOCKD_UDPPORT=32769\nMOUNTD_PORT=892\nSTATD_PORT=662\nSTATD_OUTGOING_PORT=2020\n')
	f9.close()
	cmd('service rpcbind start && service nfs start && /etc/init.d/iptables stop')
	raw_input('######setup ok!\nPlease input any key to exit!######')


def setup_3():
	'''
	cloudstack.py uploadvm
	上传虚拟机模板，要先搭建好存储节点
	目录下有：
	systemvm64template-4.5-xen.vhd.bz2
	'''
	cloudstackdir = raw_input('Please input your\'s cloudstackdir:\n') 
	cmd('mount -t nfs 192.168.0.2:/export/B_sec /mnt && /usr/share/cloudstack-common/scripts/storage/secondary/cloud-install-sys-tmplt -m /mnt -f' + cloudstackdir + 'systemvm64template-4.5-xen.vhd.bz2 -h xenserver -F && umount /mnt')
	raw_input('######setup ok!\nPlease input any key to exit!######')

if __name__ == '__main__':
	s = len(sys.argv)
	if s == 1:
		print 'use:\n1.cloudstack_setup.py manager\n2.cloudstack_setup.py storage\n3.cloudstack_setup.py uploadvm'
	elif s > 1:
		if sys.argv[1] == 'manager':
			setup_1()
		elif sys.argv[1] == 'storage':
			setup_2()
		elif sys.argv[1] == 'uploadvm':
			setup_3()			
		else:
			print 'Error!'
	else:
		print 'Error!'
