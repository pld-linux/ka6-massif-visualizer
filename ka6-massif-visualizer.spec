#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeappsver	26.04.3
%define		kframever	6.13.0
%define		qtver		6.8
%define		kaname		massif-visualizer
Summary:	Visualizer for Valgrind Massif
Name:		ka6-%{kaname}
Version:	26.04.3
Release:	1
License:	GPL v2+/LGPL v2.1+
Group:		X11/Applications
Source0:	https://download.kde.org/stable/release-service/%{kdeappsver}/src/%{kaname}-%{version}.tar.xz
# Source0-md5:	587414f32ca82aa03e3550576a53bdc0
URL:		http://www.kde.org/
BuildRequires:	Qt6Core-devel >= %{qtver}
BuildRequires:	Qt6Gui-devel
BuildRequires:	Qt6Svg-devel
BuildRequires:	Qt6Widgets-devel
BuildRequires:	gettext-tools
BuildRequires:	kdiagram-devel >= 3.0.0
BuildRequires:	kf6-extra-cmake-modules >= %{kframever}
BuildRequires:	kf6-karchive-devel >= %{kframever}
BuildRequires:	kf6-kconfig-devel >= %{kframever}
BuildRequires:	kf6-kcoreaddons-devel >= %{kframever}
BuildRequires:	kf6-ki18n-devel >= %{kframever}
BuildRequires:	kf6-kio-devel >= %{kframever}
BuildRequires:	kf6-kparts-devel >= %{kframever}
BuildRequires:	ninja
BuildRequires:	qt6-build >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	shared-mime-info
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires(post,postun):	desktop-file-utils
%requires_eq_to Qt6Core Qt6Core-devel
Obsoletes:	ka5-%{kaname} < %{version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Massif Visualizer is a tool that - who'd guess that - visualizes
massif data. You run your application in Valgrind with --tool=massif
and then open the generated massif.out.%pid in the visualizer. Gzip or
Bzip2 compressed massif files can also be opened transparently.

Features:
- Interactive chart of memory consumption over time.
- Detailed snapshot analysis with callgraph visualization (requires
  KGraphViewer).
- Summary of peak memory consumption of all allocating functions.

%description -l pl.UTF-8
Program do wizualizacji Massif jest narzędziem, które wizualizuje dane
massif. Uruchamiasz swoją aplikację w Valgrind przy użyciu
--tool=massif a następnie otwierasz utworzony massif.out.%pid w
programie do wizualizacji. Można otwierać pliki massif skompresowane
przy użyciu Gzip lub Bzip2.

Możliwości:
- Interaktywny wykres wykorzystania pamięci w czasie.
- Szczegółowe analizy zrzutów z wizualizacją wykresu wywołań (wymaga
  KGraphViewer).
- Podsumowanie szczytowego wykorzystania pamięci wszystkich
  przydzielonych funkcji.

%prep
%setup -q -n %{kaname}-%{version}

%build
%cmake \
	-B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_DOCBUNDLEDIR=%{_kdedocdir} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON \
	-DQT_MAJOR_VERSION=6
%ninja_build -C build

%if %{with tests}
ctest --test-dir build
%endif


%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%find_lang %{kaname} --all-name --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_desktop_database_post

%postun
%update_desktop_database_postun

%files -f %{kaname}.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/massif-visualizer
%{_desktopdir}/org.kde.massif-visualizer.desktop
%{_datadir}/config.kcfg/massif-visualizer-settings.kcfg
%{_iconsdir}/hicolor/scalable/apps/massif-visualizer.svg
%{_datadir}/massif-visualizer
%{_datadir}/metainfo/org.kde.massif_visualizer.appdata.xml
%{_datadir}/mime/packages/massif.xml
