#
# Conditional build:
%bcond_without	tests	# unit tests

%define		module	aiohappyeyeballs
Summary:	Happy Eyeballs for asyncio
Summary(pl.UTF-8):	Algorytm Happy Eyeballs dla asyncio
Name:		python3-%{module}
Version:	2.6.1
Release:	1
License:	PSF
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/aiohappyeyeballs/
Source0:	https://files.pythonhosted.org/packages/source/a/aiohappyeyeballs/%{module}-%{version}.tar.gz
# Source0-md5:	2fa845a1ce2f7730045fa763aa9987f8
Patch0:		aiohappyeyeballs-pytest_asyncio.patch
URL:		https://pypi.org/project/aiohappyeyeballs/
BuildRequires:	python3-build
BuildRequires:	python3-installer
BuildRequires:	python3-modules >= 1:3.9
BuildRequires:	python3-poetry-core
%if %{with tests}
BuildRequires:	python3-pytest >= 7
BuildRequires:	python3-pytest-cov >= 3
BuildRequires:	python3-pytest-asyncio >= 0.23.2
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 2.044
Requires:	python3-modules >= 1:3.9
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This library exists to allow connecting with Happy Eyeballs (RFC 8305)
when you already have a list of addrinfo and not a DNS name.

%description -l pl.UTF-8
Ta biblioteka pozwala na łączenie z użyciem algorythmu Happy Eyeballs
(RFC 8305), kiedy mamy już listę addrinfo, a nie nazwę DNS.

%prep
%setup -q -n %{module}-%{version}
%patch -P0 -p1

%build
%py3_build_pyproject

%if %{with tests}
%{__python} -m zipfile -e build-3/*.whl build-3-test
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS=pytest_cov.plugin,pytest_asyncio.plugin \
%{__python3} -m pytest -o pythonpath="$PWD/build-3-test" tests
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install_pyproject

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.md
%{py3_sitescriptdir}/%{module}
%{py3_sitescriptdir}/%{module}-%{version}.dist-info
