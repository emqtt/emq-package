%define __debug_install_post %{_rpmconfigdir}/find-debuginfo.sh %{?_find_debuginfo_opts} "%{_builddir}/%{?buildsubdir}" %{nil}
Name:    emqx	
Version: 2.4
Release: 1%{?dist}
Summary: emqx
Group:	 System Environment/Daemons
License: Apache License Version 2.0
URL:	 http://www.emqtt.io
Source0:	%{name}-%{version}.tar.gz
BuildRoot:  %_topdir/BUILDROOT
#BuildRequires: gcc,make	
#Requires:	pcre,pcre-devel,openssl,chkconfig

%description
(Erlang MQTT Broker) is a distributed, massively scalable, highly extensible MQTT message broker written in Erlang/OTP.

%prep
%setup -q

%build
make %{?_smp_mflags}

%install
#make install DESTDIR=%{buildroot}
%define relpath       %{_builddir}/%{buildsubdir}/_rel/emqx
%define buildroot_lib %{buildroot}%{_libdir}/emqx
%define buildroot_etc %{buildroot}%{_sysconfdir}/emqx
%define buildroot_bin %{buildroot_lib}/bin

mkdir -p %{buildroot_etc}
mkdir -p %{buildroot_lib}
mkdir -p %{buildroot}%{_localstatedir}/lib/emqx
mkdir -p %{buildroot}%{_localstatedir}/log/emqx
mkdir -p %{buildroot}%{_localstatedir}/run/emqx
mkdir %{buildroot_bin}
mkdir -p %{buildroot}/usr/sbin/

install -p -D -m 0755 %{relpath}/bin/emqx %{buildroot}/usr/sbin
install -p -D -m 0755 %{relpath}/bin/emqx_ctl %{buildroot}/usr/sbin

cp -R %{relpath}/lib           %{buildroot_lib}
cp -R %{relpath}/erts-*        %{buildroot_lib}
cp -R %{relpath}/releases      %{buildroot_lib}

cp %{relpath}/bin/cuttlefish               %{buildroot_bin}
cp %{relpath}/bin/install_upgrade_escript  %{buildroot_bin}
cp %{relpath}/bin/nodetool                 %{buildroot_bin}
cp %{relpath}/bin/start_clean.boot         %{buildroot_bin}

cp -R %{relpath}/etc/* %{buildroot_etc}

mkdir -p %{buildroot}%{_localstatedir}/lib/emqx

cp -R %{relpath}/data/* %{buildroot}%{_localstatedir}/lib/emqx

command -v service >/dev/null 2>&1 || { mkdir -p %{buildroot}%{_unitdir}/; install -m755  %{_topdir}/emqx.service %{buildroot}%{_unitdir}/; }
command -v systemctl >/dev/null 2>&1 || { mkdir -p %{buildroot}%{_sysconfdir}/init.d; install -m755 %{_topdir}/init.script  %{buildroot}%{_sysconfdir}/init.d/emqx; }

%pre
# Pre-install script
if ! getent group emqtt >/dev/null 2>&1; then
	groupadd -r emqtt
fi

if getent passwd emqtt >/dev/null 2>&1; then
	usermod -d %{_localstatedir}/lib/emqx emqtt || true
else
    useradd -r -g emqtt \
           --home %{_localstatedir}/lib/emqtt \
           --comment "emqtt user" \
           --shell /bin/bash \
           emqtt
fi

%post
if [ $1 == 1 ];then
    if [ -e /etc/init.d/emqx ] ; then
        sbin/chkconfig --add emqx
    else
        systemctl enable emqx.service
    fi
fi

%preun
# Pre-uninstall script

# Only on uninstall, not upgrades
if [ "$1" = 0 ] ; then
    if [ -e /etc/init.d/emqx ] ; then
        /sbin/service emqx stop > /dev/null 2>&1
        /sbin/chkconfig --del emqx
    else
        systemctl disable emqx.service
    fi
fi
exit 0

%files
%defattr(-,emqtt,emqtt)
/etc/ 
/usr/ 
/var/ 
%doc

%clean
rm -rf %{buildroot}

%changelog

