Summary:        Wrapper library for GNOME VTE
Name:           libvte-java 
Version:        0.12.3
Release:        %mkrel 3
Epoch:          0
URL:            http://java-gnome.sourceforge.net/
Source0:        http://fr2.rpmfind.net/linux/gnome.org/sources/libvte-java/0.12/libvte-java-%{version}.tar.bz2
Source1:        http://fr2.rpmfind.net/linux/gnome.org/sources/libvte-java/0.12/libvte-java-0.12.3.changes
Source2:        http://fr2.rpmfind.net/linux/gnome.org/sources/libvte-java/0.12/libvte-java-0.12.3.md5sum
Source3:        http://fr2.rpmfind.net/linux/gnome.org/sources/libvte-java/0.12/libvte-java-0.12.3.news
Source4:        java-gnome-macros.tar.bz2
License:        LGPL
Group:          System/Libraries
BuildRequires:  docbook-utils
BuildRequires:  java-gcj-compat-devel
BuildRequires:  glib-java-devel >= 0:0.4.2
BuildRequires:  java-devel >= 0:1.4.2
BuildRequires:  java-rpmbuild
BuildRequires:  libgtk-java-devel >= 0:2.10.2
BuildRequires:  libgnomeui2-devel
BuildRequires:  libgnomecanvas2-devel
BuildRequires:  pkgconfig
BuildRequires:  vte-devel
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

%description 
libvte-java is a Java wrapper library for the GNOME VTE library
which allows access to the terminal widget from Java.

%package        devel
Summary:        Development files for %{name}
Group:          Development/Java
Requires:       %{name} = %{epoch}:%{version}
Conflicts:      libvte-java < 0.12.3-2

%description    devel
Development files for %{name}.

%prep
%setup -q
%setup -q -T -D -a 4
%{__aclocal} -I macros --force
%{__autoconf} --force
%{__automake} --copy --force-missing
%{__libtoolize} --copy --force

%build
export CLASSPATH=
export JAVA=%{java}
export JAVAC=%{javac}
export JAR=%{jar}
export JAVADOC=%{javadoc}
export GCJ=%{gcj}
export CPPFLAGS="-I%{java_home}/include -I%{java_home}/include/linux"
%{configure2_5x} --with-jardir=%{_javadir}
%{make}

# pack up the java source
jarversion=$(echo -n %{version} | cut -d . -f -2)
jarname=$(echo -n %{name} | cut -d - -f 1 | sed "s/^lib//")
zipfile=$PWD/$jarname$jarversion-src-%{version}.zip
pushd src/java
%{_bindir}/zip -9 -r $zipfile $(find -name \*.java)
popd

%install
%{__rm} -rf %{buildroot}
%{makeinstall_std}
%{__rm} -rf %{buildroot}/%{name}-%{version}

# install the src zip and make a sym link
jarversion=$(echo -n %{version} | cut -d . -f -2)
jarname=$(echo -n %{name} | cut -d - -f 1 | sed "s/^lib//")
%{__install} -m 644 $jarname$jarversion-src-%{version}.zip $RPM_BUILD_ROOT%{_datadir}/java/
pushd %{buildroot}%{_datadir}/java
%{__ln_s} $jarname$jarversion-src-%{version}.zip $jarname$jarversion-src.zip
popd

%clean
%{__rm} -rf %{buildroot}

%post -p /sbin/ldconfig
 
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING INSTALL NEWS README 
%{_libdir}/libvtejava-*.so
%{_libdir}/libvtejni-*.so
%{_datadir}/java/*.jar

%files devel
%defattr(-,root,root)
%doc doc/api
%{_datadir}/java/*.zip
%{_libdir}/pkgconfig/*
%{_libdir}/libvtejava.so
%{_libdir}/libvtejni.so
%{_libdir}/*la
