%define name tt-rss
%define version 20180905.git62d0060a
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
%setup

%pre

%post
%preun

%build

%install
rm -rf $RPM_BUILD_ROOT
(cd root   ; find . -depth -print | cpio -dump $RPM_BUILD_ROOT)
%{genfilelist} %{buildroot} $RPM_BUILD_ROOT > e-smith-%{version}-filelist

%clean
rm -rf $RPM_BUILD_ROOT

%files -f e-smith-%{version}-filelist
%defattr(-,root,root)
