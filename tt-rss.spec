%define name tt-rss
%define version 20190212
%define release 1
%define httpuser apache

Summary: A rpm for tt-rss
Name: %{name}
Version: %{version}
Release: %{release}%{?dist}
License: GPL
Source: %{name}-%{version}.tar.gz
Source1: httpd.conf
Source2: cron
Source3: logrotate.conf
BuildArch: noarch
URL: https://tt-rss.org/
BuildRequires: nethserver-devtools
Requires: php-gd httpd logrotate
#AutoReq: no

%description
NethServer configuration for fail2ban

%prep
%setup

%pre

%post
%preun

%build

%install
rm -rf $RPM_BUILD_ROOT
(cd root   ; find . -depth -print | cpio -dump $RPM_BUILD_ROOT)

%{genfilelist} %{buildroot} \
$RPM_BUILD_ROOT > e-smith-%{version}-filelist


# rename icons to rssicons so it won't clash with the global icons directory
#%{__mv} %{buildroot}/%{_datadir}/%{name}/feed-icons %{buildroot}/%{_datadir}/%{name}/rssicons

# remove cache and lock directories
%{__rm} -Rf %{buildroot}/%{_datadir}/%{name}/{cache,lock}

# And create them at the correct place
%{__mkdir} -p %{buildroot}/%{_localstatedir}/cache/%{name}/{simplepie,images,export,js,upload,starred-images}
%{__mkdir} -p %{buildroot}/%{_localstatedir}/lock/%{name}

#sed -e "s|\"pgsql\"|\"mysql\"|g" \
#    -e "s|cache|%{_localstatedir}/cache/%{name}/|g" \
#    -e "s|\"feed-icons\"|\"rssicons\"|g" \
#    -e "s|'lock'|'%{_localstatedir}/lock/%{name}'|g" \
#    config.php-dist \
#    > %{buildroot}/%{_datadir}/%{name}/config.php

%{__mkdir} -p %{buildroot}/%{_sysconfdir}/httpd/conf.d/
%{__install} -m 0644 %{SOURCE1} %{buildroot}/%{_sysconfdir}/httpd/conf.d/%{name}.conf
sed -i -e "s|__ROOT_DIR__|%{_datadir}/%{name}|g" \
       -e "s|__CACHE_DIR__|%{_localstatedir}/cache/%{name}|g" \
       -e "s|__LOCK_DIR__|%{_localstatedir}/lock/%{name}|g" \
       %{buildroot}/%{_sysconfdir}/httpd/conf.d/%{name}.conf

%{__mkdir} -p %{buildroot}/%{_localstatedir}/log/
touch %{buildroot}/%{_localstatedir}/log/%{name}.log

%{__mkdir} -p %{buildroot}/%{_sysconfdir}/cron.d
%{__install} -m 0644 %{SOURCE2} %{buildroot}/%{_sysconfdir}/cron.d/%{name}
sed -i -e "s|__APACHE__|%{httpuser}|g" \
       -e "s|__ROOT_DIR__|%{_datadir}/%{name}|g" \
       -e "s|__LOG_FILE__|%{_localstatedir}/log/%{name}.log|g" \
       %{buildroot}/%{_sysconfdir}/cron.d/%{name}

%{__mkdir} -p %{buildroot}/%{_sysconfdir}/logrotate.d/
%{__install} -m 644 %{SOURCE3} %{buildroot}/%{_sysconfdir}/logrotate.d/%{name}
sed -i -e "s|__LOG_DIR__|%{_localstatedir}/log/%{name}.log|g" \
       -e "s|__APACHE__|%{httpuser}|g" \
%{SOURCE3} %{buildroot}/%{_sysconfdir}/logrotate.d/%{name}





%clean
rm -rf $RPM_BUILD_ROOT

%files -f e-smith-%{version}-filelist
%defattr(-,root,root)
#%{_datadir}/%{name}

%dir %attr(770,root,%{httpuser}) %{_localstatedir}/cache/%{name}/simplepie
%dir %attr(770,root,%{httpuser}) %{_localstatedir}/cache/%{name}/images
%dir %attr(770,root,%{httpuser}) %{_localstatedir}/cache/%{name}/export
%dir %attr(770,root,%{httpuser}) %{_localstatedir}/cache/%{name}/js
%dir %attr(770,root,%{httpuser}) %{_localstatedir}/cache/%{name}/upload
%dir %attr(770,root,%{httpuser}) %{_localstatedir}/cache/%{name}/starred-images
%dir %attr(775,root,%{httpuser}) %{_localstatedir}/lock/%{name}
%dir %attr(775,root,%{httpuser}) %{_datadir}/%{name}/feed-icons
%attr(660,root,%{httpuser}) %{_localstatedir}/log/%{name}.log
#%config(noreplace) %attr(660,root,%{httpuser}) %{_datadir}/%{name}/config.php
%config(noreplace) %{_sysconfdir}/httpd/conf.d/%{name}.conf
%config(noreplace) %{_sysconfdir}/cron.d/%{name}
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}

