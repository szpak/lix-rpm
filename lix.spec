%global forgeurl https://github.com/SimonN/LixD/

Name:           lix
Version:        0.10.36
Release:        2%{?dist}
Summary:        A single and multiplayer puzzle game inspired by Lemmings
Group:          Games and Entertainment
# CC0-1.0 for everything, expect "Bitstream Vera and Public Domain" for dejavu-sans fonts
License:        CC0-1.0 AND (Bitstream Vera and Public Domain)
URL:            https://www.lixgame.com/

# Add -i -v for detailed information
%forgemeta
Source:         %{forgesource}
Source1:        lix-dub-deps-local-%{version}.tar.xz
# TODO: In fact version 1.1 - add explicit versioning, if provided upstream - https://github.com/SimonN/LixD/issues/457
Source2:        https://www.lixgame.com/dow/lix-music.zip
Source3:        vendor.sh

BuildRequires:  ldc
BuildRequires:  dub
BuildRequires:  pkgconf-pkg-config
BuildRequires:  enet-devel
BuildRequires:  allegro5-devel
BuildRequires:  allegro5-addon-acodec-devel
BuildRequires:  allegro5-addon-audio-devel
BuildRequires:  allegro5-addon-image-devel
BuildRequires:  allegro5-addon-ttf-devel
# dub uses git client to determine version of dependencies in local cache
BuildRequires:  git
# To avoid "wrong-file-end-of-line-encoding" warning in rpmlint
BuildRequires: dos2unix

Requires:       dejavu-sans-fonts

Recommends:     lix-music = %{version}-%{release}

%description
Lix is a puzzle game inspired by Lemmings. Lix is free and open source.
Assign skills to guide the lix through over 700 single-player puzzles.
Design your own levels with the included editor.
Attack and defend in real-time multiplayer for 2 to 8 players:
Who can save the most lix?

%package music
Summary:        Music for Lix - a single and multiplayer puzzle game inspired by Lemmings
# CC0-1.0 for menulix.ogg and minim-mobius/, CC-BY-4.0 for rubix/
License:        CC0-1.0 AND CC-BY-4.0
BuildArch:      noarch

%description music
Music for Lix - a single and multiplayer puzzle game inspired by Lemmings.


%prep
%setup -q -n LixD-%{version}
# TODO: Ask upstream to switch end of lines and/or normalize with .gitattributes
dos2unix README.md doc/cmdargs.txt doc/history.txt doc/levmaint.txt doc/thanks.txt
tar xJf %{SOURCE1}
unzip %{SOURCE2}

%build
export DFLAGS="%{_d_optflags}"
export DUB_DEPS_LOCAL_PATH=$(pwd)/lix-dub-deps-local-%{version}
# TODO: Run unit-tests?
DUB_HOME="$DUB_DEPS_LOCAL_PATH" dub build --nodeps --cache=local -f -b releaseXDG

%install
install -Dm 0755 bin/%{name} %{buildroot}%{_bindir}/%{name}
install -d %{buildroot}%{_datadir}/%{name}
cp -ar data/ images/ levels/ %{buildroot}%{_datadir}/%{name}
cp -ar music/ %{buildroot}%{_datadir}/%{name}

rm -f %{buildroot}%{_datadir}/lix/data/fonts/djvusans.ttf
ln -s %{_fontbasedir}/dejavu-sans-fonts/DejaVuSans.ttf %{buildroot}%{_datadir}/lix/data/fonts/djvusans.ttf

install -Dm 0644 doc/lix.6 %{buildroot}%{_mandir}/man6/lix.6
install -Dm 0644 data/images/lix_logo.svg %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/com.lixgame.Lix.svg
install -Dm 0644 data/desktop/com.lixgame.Lix.metainfo.xml %{buildroot}%{_datadir}/metainfo/com.lixgame.Lix-metainfo.xml
install -Dm 0644 data/desktop/com.lixgame.Lix.desktop %{buildroot}%{_datadir}/applications/com.lixgame.Lix.desktop

%files
%doc README.md doc/cmdargs.txt doc/history.txt doc/levmaint.txt doc/thanks.txt
%license doc/copying.txt
%{_bindir}/lix
%{_datadir}/lix/data
%{_datadir}/lix/images
%{_datadir}/lix/levels
%{_datadir}/icons/hicolor/scalable/apps/com.lixgame.Lix.svg
%{_datadir}/applications/com.lixgame.Lix.desktop
%{_datadir}/metainfo/com.lixgame.Lix-metainfo.xml
%{_mandir}/man6/lix.6*
# Already installed in other directories, no duplication needed
%exclude %{_datadir}/lix/data/images/lix_logo.svg
%exclude %{_datadir}/lix/data/desktop/com.lixgame.Lix.metainfo.xml
%exclude %{_datadir}/lix/data/desktop/com.lixgame.Lix.desktop

%files music
%{_datadir}/lix/music

%changelog
* Mon Oct 12 2026 Marcin Zajaczkowski <mszpak ATT wp DOTT pl> 0.10.36-2
- remove some linter warnings

* Mon Oct 12 2026 Marcin Zajaczkowski <mszpak ATT wp DOTT pl> 0.10.36-1
- upgrade to 0.10.36

* Sun Oct 11 2026 josef radinger <cheese@nosuchhost.net> - 0.10.35-1
- bump version
- use versioned local-deps (version instead of date)
- add vendor.sh to create local-deps
- small corrections in spec-file (typos)
- remove djvusans.ttf and use Requires on dejavu-sans-fonts

* Thu Aug 27 2026 Marcin Zajaczkowski <mszpak ATT wp DOTT pl> 0.10.26-2
- rebuild for Fedora 44

* Fri Nov 08 2024 Marcin Zajaczkowski <mszpak ATT wp DOTT pl> 0.10.26-1
- upgrade to 0.10.26

* Mon Feb 19 2024 Marcin Zajaczkowski <mszpak ATT wp DOTT pl> 0.10.20-0.2
- exclude some duplicated files in RPM package

* Mon Feb 19 2024 Marcin Zajaczkowski <mszpak ATT wp DOTT pl> 0.10.20-0.1
- upgrade to 0.10.20
- upgrade local (offline) dub dependencies (allegro 4.0.4+5.2.0 → 4.0.6+5.2.0)
- make music subpackage architecture agnostic (noarch)

* Mon Feb 19 2024 Marcin Zajaczkowski <mszpak ATT wp DOTT pl> 0.10.12-0.1
- upgrade to 0.10.12
- use updated lix-music 1.1 package (still using the same URL - see discussion in https://github.com/SimonN/LixD/issues/457)

* Sun Apr 02 2023 Marcin Zajaczkowski <mszpak ATT wp DOTT pl> 0.10.7-0.5
- improve version rule for "Recommends"
- remove superfluous "clean" section (as suggested by linter)

* Sun Apr 02 2023 Marcin Zajaczkowski <mszpak ATT wp DOTT pl> 0.10.7-0.4
- generate debuginfo packages

* Sun Apr 02 2023 Marcin Zajaczkowski <mszpak ATT wp DOTT pl> 0.10.7-0.3
- recommended music subpackage
- remove duplicated svg icon (3,6MB)

* Sun Apr 02 2023 Marcin Zajaczkowski <mszpak ATT wp DOTT pl> 0.10.7-0.2
- local (offline) dub dependencies

* Sat Mar 25 2023 Marcin Zajaczkowski <mszpak ATT wp DOTT pl> 0.10.7-0.1
- initial package (loosely based on the SUSE version)

