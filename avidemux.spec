%define with_gtk 1
%define with_qt 1
#define svndate 20080521

Name:           avidemux
Version:        2.4.2
Release:        3%{?dist}
Summary:        Graphical video editing tool

Group:          Applications/Multimedia
License:        GPLv2+
URL:            http://www.avidemux.org/
Source0:        http://download.berlios.de/avidemux/avidemux_%{version}.tar.gz
Source1:        %{name}-gtk.desktop
Source2:        %{name}-qt.desktop
Patch0:         avidemux-2.4.2-pulseaudio-default.patch
#http://bugs.gentoo.org/attachment.cgi?id=160132&action=view
Patch1:         avidemux-2.4.2-x264-2pass.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# GTK interface is what people are used to, let's use that be default.
Requires:       %{name}-gtk

# Compiling
BuildRequires:  libtool >= 1.5.6
BuildRequires:  gettext-devel
BuildRequires:  autoconf

# Libraries
BuildRequires:  nasm >= 0.98.38
BuildRequires:  libxml2-devel >= 2.6.8
BuildRequires:  fontconfig-devel
BuildRequires:  freetype-devel
BuildRequires:  js-devel
BuildRequires:  libXv-devel
BuildRequires:  libXmu-devel
# Required by gtk: libXi-devel, libXext-devel, libX11-devel
# Required by qt: libXt-devel, libXext-devel, libX11-devel

# Sound out
BuildRequires:  alsa-lib-devel >= 1.0.3
BuildRequires:  esound-devel >= 0.2.0

# Video out 
BuildRequires:  SDL-devel >= 1.2.7

# Audio Codecs
BuildRequires:  a52dec-devel >= 0.7.4
BuildRequires:  faac-devel >= 1.24
BuildRequires:  faad2-devel >= 2.0
BuildRequires:  lame-devel >= 3.96.1
# BuildRequires:  libdca-devel
# needs libdts/dts_internal.h; but that's not shipped by  libdca-devel because
# it's an internal lib. Someone needs to report that upstream to get fixed
BuildRequires:  libmad-devel >= 0.15.1
BuildRequires:  libogg-devel >= 1.1
BuildRequires:  libvorbis-devel >= 1.0.1

# Video Codecs
BuildRequires:  xvidcore-devel >= 1.0.2
BuildRequires:  x264-devel
BuildRequires:  ffmpeg-devel

# Finally...
BuildRequires:  desktop-file-utils

%description
Avidemux is a free video editor designed for simple cutting, filtering and
encoding tasks. It supports many file types, including AVI, DVD compatible
MPEG files, MP4 and ASF, using a variety of codecs. Tasks can be automated
using projects, job queue and powerful scripting capabilities.

%if %{with_gtk}
%package gtk
Summary:        GTK GUI for %{name}
Group:          Applications/Multimedia
BuildRequires:  gtk2-devel >= 2.8.0
BuildRequires:  cairo-devel
Provides:       %{name}-gui = %{version}-%{release}.1

%description gtk
This package provides the GTK interface for %{name}
%endif

%if %{with_qt}
%package qt
Summary:        QT GUI for %{name}
Group:          Applications/Multimedia
BuildRequires:  qt4-devel
Provides:       %{name}-gui = %{version}-%{release}

%description qt
This package provides the QT interface for %{name}
%endif

%prep
%setup -q -n avidemux_%{version}
pushd avidemux
%patch0 -b .pulse
popd
%patch1 -p1 -b .x264_2pass

%build
make -f Makefile.dist
# doesn't seem to fix ppc :/
# edit: maybe it does? let's find out!
#--with-newfaad \
%configure \
  --with-jsapi-include=%{_includedir} \
  --with-qt-include=%{_includedir} \
  --with-qt-lib=%{_libdir}/qt4 \
  --with-qt-dir=%{_libdir}/qt4 \
%ifarch ppc ppc64
  --enable-altivec \
  --with-newfaad \
%endif

# Weird... %%{?_smp_mflags} works locally, but not on the buildsys?
make


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%if %{with_gtk}
desktop-file-install --vendor livna \
    --dir $RPM_BUILD_ROOT%{_datadir}/applications \
    %{SOURCE1}
%endif

%if %{with_qt}
desktop-file-install --vendor livna \
    --dir $RPM_BUILD_ROOT%{_datadir}/applications \
    %{SOURCE2}
%endif

find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS COPYING ChangeLog History README TODO
%{_bindir}/avidemux2_cli

%if %{with_gtk}
%files gtk
%defattr(-,root,root,-)
%{_bindir}/avidemux2_gtk
%{_datadir}/applications/*gtk*.desktop
%endif

%if %{with_qt}
%files qt
%defattr(-,root,root,-)
%{_bindir}/avidemux2_qt4
%{_datadir}/applications/*qt*.desktop
%endif

%changelog
* Tue Aug 12 2008 Stewart Adam <s.adam at diffingo.com> - 2.4.2-3
- ppc64 uint_32 fun

* Sun Aug 03 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info - 2.4.2-2
- rebuild

* Sat Jul 19 2008 Thorsten Leemhuis <s.adam at diffingo.com> - 2.4.2-1
- Update to 2.4.2

* Wed May 21 2008 Stewart Adam <s.adam AT diffingo DOT com> - 2.4.1-3.20080521svn
- Disable --new-faad
- 20080521 subversion snapshot

* Sat Mar 15 2008 Stewart Adam <s.adam AT diffingo DOT com> - 2.4.1-2
- Disable %%{?_smp_mflags}

* Sat Mar 15 2008 Stewart Adam <s.adam AT diffingo DOT com> - 2.4.1-1
- Update to 2.4.1
- Don't list the bin files twice, revisited
- Default to GTK frontend

* Wed Feb 20 2008 Stewart Adam <s.adam AT diffingo DOT com> - 2.4-6.20080126svn
- Make pulseaudio default for sound out
- Don't list the bin files twice
- Don't build with arts support

* Fri Feb 15 2008 Stewart Adam <s.adam AT diffingo DOT com> - 2.4-5.20080126svn
- Don't list the .desktop files twice (bz#1870)
- Oops, we should have %%{svndate}svn in release tag!

* Sat Feb 2 2008 Stewart Adam <s.adam AT diffingo DOT com> - 2.4-4
- F-8/F-7 x86_64 does seem to need --with-newfaad

* Fri Feb 1 2008 Stewart Adam <s.adam AT diffingo DOT com> - 2.4-3
- Update to version 2.4 (20080126svn) and include fixes from devel branch

* Mon Jan 14 2008 Stewart Adam <s.adam AT diffingo DOT com> - 2.4-2
- Fix many copy/paste errors and desktop file's Exec field

* Sun Jan 13 2008 Stewart Adam <s.adam AT diffingo DOT com> - 2.4-1
- Update to 2.4 final
- Split up desktop files and make them pass desktop-file-validate
- Add structure to split into gtk and qt pacakges
- Disable qt4 for now, doesn't compile

* Sun Oct 7 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info>3- 2.3.0-4.3
- move js-include to a place where it is honored

* Sun Oct 7 2007 Stewart Adam <s.adam AT diffingo DOT com> - 2.3.0-4.2
- Fix macro problem
- Fix changelog date
- Rebuild with faad, but don't pass --newfaad

* Sun Oct 7 2007 Stewart Adam <s.adam AT diffingo DOT com> - 2.3.0-4.1
- Rebuild with no faad

* Sat Oct 6 2007 Stewart Adam <s.adam AT diffingo DOT com> - 2.3.0-4
- Rebuild for ffmpeg dependency problems
- Update License: tag per Fedora guidelines

* Sat Jan 13 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 2.3.0-3
- more features with new BR's: x264-devel libXv-devel
- make a note regarding the libdca-devel problem
- remove the "0:" from the versioned BR's

* Thu Jan 04 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 2.3.0-2
- don't use smp_mflags during make for now

* Sat Dec 23 2006 kwizart < kwizart at gmail.com > - 2.3.0-1
- Update to 2.3.0 Final
- Use find_lang

* Mon Apr 03 2006 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 2.1.2-1
- Update to 2.1.2

* Thu Mar 09 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- switch to new release field

* Tue Feb 28 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- add dist

* Wed Jan 04 2006 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 0:2.1.0-0.lvn.1
- Update to 2.1.0
- Drop epoch
- gtk 2.6 now, so drop FC3 support

* Sat Aug 27 2005 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 0:2.0.42-0.lvn.3
- Remove bogus BR ffmpeg-devel (#555)

* Thu Jul 09 2005 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 0:2.0.42-0.lvn.2
- Add missing BR desktop-file-utils (thanks to ixs)

* Thu Jul 07 2005 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 0:2.0.42-0.lvn.1
- Update to 2.0.42

* Sat Jan 22 2005 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 0:2.0.36-0.lvn.1
- Update to 2.0.34
- Rename package to avidemux -- no need for avidemux2 afaics

* Sun Nov 21 2004 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 0:2.0.34-0.lvn.1.test1
- Update to 2.0.34-test1
- BR gettext, libtool

* Tue Oct 18 2004 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 0:2.0.30-0.lvn.1
- Initial RPM release.
