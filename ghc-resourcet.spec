#
# Conditional build:
%bcond_without	prof	# profiling library
#
%define		pkgname	resourcet
Summary:	Deterministic allocation and freeing of scarce resources
Summary(pl.UTF-8):	Deterministyczne przydzielanie i zwalnianie brakujących zasobów
Name:		ghc-%{pkgname}
Version:	1.2.4
Release:	2
License:	BSD
Group:		Development/Languages
#Source0Download: http://hackage.haskell.org/package/resourcet
Source0:	http://hackage.haskell.org/package/%{pkgname}-%{version}/%{pkgname}-%{version}.tar.gz
# Source0-md5:	ea8f630f0630639eef7546e7315eda5f
URL:		http://hackage.haskell.org/package/resourcet
BuildRequires:	ghc >= 6.12.3
BuildRequires:	ghc-base >= 4.3
BuildRequires:	ghc-containers
BuildRequires:	ghc-exceptions
BuildRequires:	ghc-mtl >= 2.0
BuildRequires:	ghc-primitive
BuildRequires:	ghc-transformers >= 0.2.2
BuildRequires:	ghc-unliftio-core
%if %{with prof}
BuildRequires:	ghc-prof >= 6.12.3
BuildRequires:	ghc-base-prof >= 4.3
BuildRequires:	ghc-containers-prof
BuildRequires:	ghc-exceptions-prof
BuildRequires:	ghc-mtl-prof >= 2.0
BuildRequires:	ghc-primitive-prof
BuildRequires:	ghc-transformers-prof >= 0.2.2
BuildRequires:	ghc-unliftio-core-prof
%endif
BuildRequires:	rpmbuild(macros) >= 1.608
Requires(post,postun):	/usr/bin/ghc-pkg
%requires_eq	ghc
Requires:	ghc-base >= 4.3
Requires:	ghc-containers
Requires:	ghc-exceptions
Requires:	ghc-mtl >= 2.0
Requires:	ghc-primitive
Requires:	ghc-transformers >= 0.2.2
Requires:	ghc-unliftio-core
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# debuginfo is not useful for ghc
%define		_enable_debug_packages	0

# don't compress haddock files
%define		_noautocompressdoc	*.haddock

%description
Deterministic allocation and freeing of scarce resources. This package
was originally included with the conduit package, and has since been
split off. For more information, please see
<http://www.yesodweb.com/book/conduits>.

%description -l pl.UTF-8
Deterministyczne przydzielanie i zwalnianie brakujących zasobów. Ten
pakiet był pierwotnie częścią pakietu conduit, ale później został
wydzielony. Więcej informacji można znaleźć pod adresem
<http://www.yesodweb.com/book/conduits>.

%package prof
Summary:	Profiling %{pkgname} library for GHC
Summary(pl.UTF-8):	Biblioteka profilująca %{pkgname} dla GHC
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	ghc-base-prof >= 4.3
Requires:	ghc-containers-prof
Requires:	ghc-exceptions-prof
Requires:	ghc-mtl-prof >= 2.0
Requires:	ghc-primitive-prof
Requires:	ghc-transformers-prof >= 0.2.2
Requires:	ghc-unliftio-core-prof

%description prof
Profiling %{pkgname} library for GHC. Should be installed when
GHC's profiling subsystem is needed.

%description prof -l pl.UTF-8
Biblioteka profilująca %{pkgname} dla GHC. Powinna być zainstalowana
kiedy potrzebujemy systemu profilującego z GHC.

%package doc
Summary:	HTML documentation for ghc %{pkgname} package
Summary(pl.UTF-8):	Dokumentacja w formacie HTML dla pakietu ghc %{pkgname}
Group:		Documentation

%description doc
HTML documentation for ghc %{pkgname} package.

%description doc -l pl.UTF-8
Dokumentacja w formacie HTML dla pakietu ghc %{pkgname}.

%prep
%setup -q -n %{pkgname}-%{version}

%build
runhaskell Setup.lhs configure -v2 \
	%{?with_prof:--enable-library-profiling} \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--libexecdir=%{_libexecdir} \
	--docdir=%{_docdir}/%{name}-%{version}

runhaskell Setup.lhs build
runhaskell Setup.lhs haddock --executables

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d

runhaskell Setup.lhs copy --destdir=$RPM_BUILD_ROOT

# work around automatic haddock docs installation
%{__rm} -rf %{name}-%{version}-doc
cp -a $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version} %{name}-%{version}-doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

runhaskell Setup.lhs register \
	--gen-pkg-config=$RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%ghc_pkg_recache

%postun
%ghc_pkg_recache

%files
%defattr(644,root,root,755)
%doc LICENSE
%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSresourcet-%{version}-*.so
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSresourcet-%{version}-*.a
%exclude %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSresourcet-%{version}-*_p.a
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Control
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Control/Monad
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Control/Monad/Trans
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Control/Monad/Trans/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Control/Monad/Trans/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Control/Monad/Trans/Resource
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Control/Monad/Trans/Resource/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Control/Monad/Trans/Resource/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Acquire
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Acquire/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Acquire/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/UnliftIO
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/UnliftIO/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/UnliftIO/*.dyn_hi

%if %{with prof}
%files prof
%defattr(644,root,root,755)
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSresourcet-%{version}-*_p.a
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Control/Monad/Trans/Resource.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Control/Monad/Trans/Resource/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Acquire/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/UnliftIO/*.p_hi
%endif

%files doc
%defattr(644,root,root,755)
%doc %{name}-%{version}-doc/*
