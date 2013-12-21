#
# Conditional build:
%bcond_without	prof	# profiling library
#
%define		pkgname	resourcet
Summary:	Deterministic allocation and freeing of scarce resources
Summary(pl.UTF-8):	Deterministyczne przydzielanie i zwalnianie brakujących zasobów
Name:		ghc-%{pkgname}
Version:	0.4.10
Release:	1
License:	BSD
Group:		Development/Languages
#Source0Download: http://hackage.haskell.org/package/resourcet
Source0:	http://hackage.haskell.org/package/%{pkgname}-%{version}/%{pkgname}-%{version}.tar.gz
# Source0-md5:	16f1f663be6bb1284177366ccc07a93b
URL:		http://hackage.haskell.org/package/resourcet
BuildRequires:	ghc >= 6.12.3
BuildRequires:	ghc-base >= 4.3
BuildRequires:	ghc-base < 5
BuildRequires:	ghc-containers
BuildRequires:	ghc-lifted-base >= 0.1
BuildRequires:	ghc-mmorph
BuildRequires:	ghc-monad-control >= 0.3.1
BuildRequires:	ghc-monad-control < 0.4
BuildRequires:	ghc-mtl >= 2.0
BuildRequires:	ghc-mtl < 2.2
BuildRequires:	ghc-transformers >= 0.2.2
BuildRequires:	ghc-transformers < 0.4
BuildRequires:	ghc-transformers-base >= 0.4.1
BuildRequires:	ghc-transformers-base < 0.5
%if %{with prof}
BuildRequires:	ghc-prof >= 6.12.3
BuildRequires:	ghc-base-prof >= 4.3
BuildRequires:	ghc-base-prof < 5
BuildRequires:	ghc-containers-prof
BuildRequires:	ghc-lifted-base-prof >= 0.1
BuildRequires:	ghc-mmorph-prof
BuildRequires:	ghc-monad-control-prof >= 0.3.1
BuildRequires:	ghc-monad-control-prof < 0.4
BuildRequires:	ghc-mtl-prof >= 2.0
BuildRequires:	ghc-mtl-prof < 2.2
BuildRequires:	ghc-transformers-prof >= 0.2.2
BuildRequires:	ghc-transformers-prof < 0.4
BuildRequires:	ghc-transformers-base-prof >= 0.4.1
BuildRequires:	ghc-transformers-base-prof < 0.5
%endif
BuildRequires:	rpmbuild(macros) >= 1.608
Requires(post,postun):	/usr/bin/ghc-pkg
%requires_eq	ghc
Requires:	ghc-base >= 4.3
Requires:	ghc-base < 5
Requires:	ghc-containers
Requires:	ghc-lifted-base >= 0.1
Requires:	ghc-mmorph
Requires:	ghc-monad-control >= 0.3.1
Requires:	ghc-monad-control < 0.4
Requires:	ghc-mtl >= 2.0
Requires:	ghc-mtl < 2.2
Requires:	ghc-transformers >= 0.2.2
Requires:	ghc-transformers < 0.4
Requires:	ghc-transformers-base >= 0.4.1
Requires:	ghc-transformers-base < 0.5
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
Requires:	ghc-base-prof < 5
Requires:	ghc-containers-prof
Requires:	ghc-lifted-base-prof >= 0.1
Requires:	ghc-mmorph-prof
Requires:	ghc-monad-control-prof >= 0.3.1
Requires:	ghc-monad-control-prof < 0.4
Requires:	ghc-mtl-prof >= 2.0
Requires:	ghc-mtl-prof < 2.2
Requires:	ghc-transformers-prof >= 0.2.2
Requires:	ghc-transformers-prof < 0.4
Requires:	ghc-transformers-base-prof >= 0.4.1
Requires:	ghc-transformers-base-prof < 0.5

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
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/HSresourcet-%{version}.o
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSresourcet-%{version}.a
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Control
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Control/Monad
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Control/Monad/Trans
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Control/Monad/Trans/Resource.hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Control/Monad/Trans/Resource
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Control/Monad/Trans/Resource/*.hi

%if %{with prof}
%files prof
%defattr(644,root,root,755)
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSresourcet-%{version}_p.a
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Control/Monad/Trans/Resource.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Control/Monad/Trans/Resource/*.p_hi
%endif

%files doc
%defattr(644,root,root,755)
%doc %{name}-%{version}-doc/*
