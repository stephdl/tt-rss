%define name tt-rss
%define version 20150711
%define release 1
%define httpuser apache

%if 0%{?fedora} >= 11 || 0%{?rhel} >= 5
%global useselinux 1
%else
%global useselinux 0
%endif

Summary: Web based RSS reader
Name: %{name}
Version: %{version}
Release: %{release}%{?dist}
License: GPLv3
URL: http://tt-rss.org/redmine/wiki/tt-rss/
Group: Applications/Internet
Source: %{name}-%{version}.tar.gz
Source1: httpd.conf
Source2: cron
Source3: logrotate.conf

Patch0: tt-rss-1.6.1-dont_check_conf_version.patch

BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-%{version}

Requires: php-gd
Requires: httpd
Requires: logrotate

%description
http://tt-rss.org/redmine/wiki/tt-rss/
Tiny Tiny RSS is an open source web-based news feed (RSS/Atom)
aggregator, designed to allow you to read news from any location,
while feeling as close to a real desktop application as possible.

%prep
%setup -q -n Tiny-Tiny-RSS-%{version}

%patch0 -p1

%build
# empty build

%install
%{__rm} -rf $RPM_BUILD_ROOT
%{__mkdir} -p %{buildroot}/%{_datadir}/%{name}
for a in $(find ./ -mindepth 1 -maxdepth 1 -type d -print); do
    cp -r $a %{buildroot}/%{_datadir}/%{name}/
done
cp {*.php,*.xsl} %{buildroot}/%{_datadir}/%{name}/
%{__rm} -rf .buildpath .gitignore .project

# rename icons to rssicons so it won't clash with the global icons directory
%{__mv} %{buildroot}/%{_datadir}/%{name}/feed-icons %{buildroot}/%{_datadir}/%{name}/rssicons

# remove cache and lock directories
%{__rm} -Rf %{buildroot}/%{_datadir}/%{name}/{cache,lock}

# And create them at the correct place
%{__mkdir} -p %{buildroot}/%{_localstatedir}/cache/%{name}/{simplepie,images,export,js,upload,starred-images}
%{__mkdir} -p %{buildroot}/%{_localstatedir}/lock/%{name}

sed -e "s|\"pgsql\"|\"mysql\"|g" \
    -e "s|cache|%{_localstatedir}/cache/%{name}/|g" \
    -e "s|\"feed-icons\"|\"rssicons\"|g" \
    -e "s|'lock'|'%{_localstatedir}/lock/%{name}'|g" \
    config.php-dist \
    > %{buildroot}/%{_datadir}/%{name}/config.php

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
rm -rf %{buildroot}

%post
%if %{useselinux}
(
# New File context
semanage fcontext -a -s system_u -t httpd_log_t -r s0 "%{_localstatedir}/log/%{name}.log"
semanage fcontext -a -s system_u -t httpd_var_lib_t -r s0 "%{_localstatedir}/lock/%{name}(/.*)?"
semanage fcontext -a -s system_u -t httpd_var_lib_t -r s0 "%{_datadir}/%{name}/rssicons(/.*)?"
semanage fcontext -a -s system_u -t httpd_var_lib_t -r s0 "%{_localstatedir}/cache/%{name}(/.*)?"
# files created by app
restorecon -R %{_datadir}/%{name}/
restorecon -R %{_localstatedir}/cache/%{name}
restorecon -R %{_localstatedir}/log/%{name}.log
restorecon -R %{_localstatedir}/lock/%{name}
) &>/dev/null || :
%endif

%postun
%if %{useselinux}
if [ "$1" -eq "0" ]; then
    # Remove the File Context
    (
    semanage fcontext -d "%{_localstatedir}/log/%{name}.log"
    semanage fcontext -d "%{_localstatedir}/cache/%{name}(/.*)?"
    semanage fcontext -d "%{_datadir}/%{name}/rssicons(/.*)?"
    semanage fcontext -d "%{_localstatedir}/lock/%{name}(/.*)?"
    ) &>/dev/null || :
fi
%endif

%files
%defattr(-,root,root)
%doc README.md
%{_datadir}/%{name}
%dir %attr(770,root,%{httpuser}) %{_localstatedir}/cache/%{name}/simplepie
%dir %attr(770,root,%{httpuser}) %{_localstatedir}/cache/%{name}/images
%dir %attr(770,root,%{httpuser}) %{_localstatedir}/cache/%{name}/export
%dir %attr(770,root,%{httpuser}) %{_localstatedir}/cache/%{name}/js
%dir %attr(770,root,%{httpuser}) %{_localstatedir}/cache/%{name}/upload
%dir %attr(770,root,%{httpuser}) %{_localstatedir}/cache/%{name}/starred-images
%dir %attr(775,root,%{httpuser}) %{_localstatedir}/lock/%{name}/
%dir %attr(775,root,%{httpuser}) %{_datadir}/%{name}/rssicons
%attr(660,root,%{httpuser}) %{_localstatedir}/log/%{name}.log
%config(noreplace) %attr(660,root,%{httpuser}) %{_datadir}/%{name}/config.php
%config(noreplace) %{_sysconfdir}/httpd/conf.d/%{name}.conf
%config(noreplace) %{_sysconfdir}/cron.d/%{name}
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}


%changelog
* Sat Jul 11 2015 stephane de Labrusse <stephdl@de-labrusse.fr> 20150711-1.sme
- new git version of the day 20150711

* Tue Jun 23 2015 stephane de Labrusse <stephdl@de-labrusse.fr> 20150623-1.sme
- new git version of the day 20150623

* Sat Mar 7 2015 Stephane de Labrusse <stephdl@de-labrusse.fr> 1.15.3-2
- First release by stephdl

* Sat Dec 13 2014 Daniel Berteaud <daniel@đirewall-services.com> 1.15.3-1
- Update to 1.15.3

* Mon Dec 8 2014 Daniel Berteaud <daniel@đirewall-services.com> 1.15-1
- Update to 1.15

* Tue Oct 21 2014 Daniel Berteaud <daniel@đirewall-services.com> 1.14-1
- update to 1.14

* Mon Jul 21 2014 Daniel Berteaud <daniel@đirewall-services.com> 1.13-1
- update to 1.13

* Fri Mar 21 2014 Daniel Berteaud <daniel@đirewall-services.com> 1.12-1
- update to 1.12

* Wed Dec 18 2013 Daniel Berteaud <daniel@đirewall-services.com> 1.11-1
- Update to 1.11

* Fri Nov 15 2013 Daniel Berteaud <daniel@đirewall-services.com> 1.10-3
- Spec file cleanup

* Tue Sep 24 2013 Daniel Berteaud <daniel@đirewall-services.com> 1.10-2
- Create missing starred-images cache dir

* Mon Sep 23 2013 Daniel Berteaud <daniel@đirewall-services.com> 1.10-1
- udpate to 1.10

* Sun Jul 21 2013 Daniel Berteaud <daniel@đirewall-services.com> 1.9-1
- update to 1.9

* Wed Jun 12 2013 Daniel Berteaud <daniel@đirewall-services.com> 1.8-1
- update to 1.8

* Tue May 14 2013 Daniel Berteaud <daniel@đirewall-services.com> 1.7.9-2
- Add upload subdir in cache

* Tue May 14 2013 Daniel Berteaud <daniel@đirewall-services.com> 1.7.9-1
- upstream upgrade to 1.7.9

* Thu Apr 4 2013 Daniel Berteaud <daniel@đirewall-services.com> 1.7.8-1
- upstream upgrade to 1.7.8

* Thu Apr 4 2013 Daniel Berteaud <daniel@đirewall-services.com> 1.7.7-1
- upstream upgrade to 1.7.7

* Wed Apr 3 2013 Daniel Berteaud <daniel@đirewall-services.com> 1.7.6-2
- upstream upgrade to 1.7.6

* Sat Mar 23 2013 Daniel Berteaud <daniel@đirewall-services.com> 1.7.5-2
- Add missing js directory in /var/cache/tt-rss

* Sat Mar 23 2013 Daniel Berteaud <daniel@đirewall-services.com> 1.7.5-1
- upstream upgrade to 1.7.5

* Sun Mar 17 2013 Daniel Berteaud <daniel@đirewall-services.com> 1.7.4-1
- upstream upgrade to 1.7.4

* Tue Mar 5 2013 Daniel Berteaud <daniel@đirewall-services.com> 1.7.1-1
- upstream upgrade to 1.7.1

* Thu Dec 20 2012 Daniel B. <daniel@firewall-services.com> 1.6.2-1
- upstream upgrade to 1.6.2

* Wed Nov 14 2012 Daniel B. <daniel@firewall-services.com> 1.6.1-1
- upstream upgrade to 1.6.1

* Mon May 21 2012 Daniel B. <daniel@firewall-services.com> 1.5.11-12
- upstream upgrade to 1.5.11

* Fri Mar 02 2012 Daniel B. <daniel@firewall-services.com> 1.5.10-11
- upstream upgrade to 1.5.10

* Thu Feb 02 2012 Daniel B. <daniel@firewall-services.com> 1.5.9-11
- upstream upgrade to 1.5.9

* Fri Jan 06 2012 Daniel B. <daniel@firewall-services.com> 1.5.8.1-11
- upstream upgrade to 1.5.8.1

* Fri Nov 25 2011 Daniel B. <daniel@firewall-services.com> 1.5.7-10
- upstream upgrade to 1.5.7

* Wed Sep 28 2011 Daniel B. <daniel@firewall-services.com> 1.5.5-8
- Don't exit with error if SELinux is disabled

* Fri Jul 22 2011 Daniel B. <daniel@firewall-services.com> 1.5.5-7
- Upstream upgrade to 1.5.5

* Mon Jul 04 2011 Daniel B. <daniel@firewall-services.com> 1.5.3-6
- Don't restart apache on install/remove/upgrade

* Sat Jul 2 2011 Daniel B. <daniel@firewall-services.com> 1.5.3-5
- create htmlpurifier cache directory

* Tue May 17 2011 Daniel B. <daniel@firewall-services.com> 1.5.3-4
- Upstream upgrade to 1.5.3

* Mon Mar 21 2011 Daniel B. <daniel@firewall-services.com> 1.5.2-4
- upstream upgrade to 1.5.2
- Read HTTP_TTRSS_LEVEL from LemonLDAP

* Wed Jan 26 2011 Daniel B. <daniel@firewall-services.com> 1.5.1-3
- Completly disable sanity checks (which are far too strict)

* Wed Jan 26 2011 Daniel B. <daniel@firewall-services.com> 1.5.1-2
- Allow open_basedir restriction

* Wed Jan 26 2011 Daniel B. <daniel@firewall-services.com> 1.5.1-1
- upstream upgrade to 1.5.1

* Mon Jan 03 2011 Daniel B. <daniel@firewall-services.com> 1.5.0-0
- initial release
- include patches for a better integration with LemonLDP::NG

