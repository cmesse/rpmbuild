Name:           scls-release
Version:        2024
Release:        1%{?dist}
Summary:        Repository configuration for Scientific Core Libraries (SCLS)
License:        GPLv2
URL:            https://belfem.lbl.gov/scls
Source0:        RPM-GPG-KEY-SCLS
BuildArch:      noarch

%description
This package provides the Scientific Core Libraries (SCLs) repository configuration
and GPG key for Enterprise Linux 9.

%prep

%build

%install
mkdir -p %{buildroot}%{_sysconfdir}/yum.repos.d
mkdir -p %{buildroot}%{_sysconfdir}/pki/rpm-gpg

# Remove the leading dot from %{?dist}
DIST_TAG=`echo "%{?dist}" | sed 's/^\.//'`

cat <<EOF > %{buildroot}%{_sysconfdir}/yum.repos.d/scls.repo
[scls]
name=Scientific Core Libraries for Enterprise Linux $DIST_TAG - \$basearch
baseurl=https://belfem.lbl.gov/scls/$DIST_TAG/\$basearch/
enabled=1
gpgcheck=1
countme=1
gpgkey=https://belfem.lbl.gov/scls/RPM-GPG-KEY-SCLS

[scls-source]
name=Scientific Core Libraries for Enterprise Linux $DIST_TAG - \$basearch - Source
baseurl=https://belfem.lbl.gov/scls/$DIST_TAG/source/
enabled=0
gpgcheck=1
countme=1
gpgkey=https://belfem.lbl.gov/scls/RPM-GPG-KEY-SCLS
EOF

install -m 644 %{SOURCE0} %{buildroot}%{_sysconfdir}/pki/rpm-gpg/

%files
%config(noreplace) %{_sysconfdir}/yum.repos.d/scls.repo
%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-SCLS

%changelog
* Wed Jan 24 2024 Christian Messe <cmesse@lbl.gov> - 2024-1
- Initial Package