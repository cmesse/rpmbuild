Name:           test-lua
Version:        1.0
Release:        1%{?dist}
Summary:        Test Lua Script in RPM
License:        GPL
URL:            http://example.com

%global lua_test_value %{lua: return "Hello from Lua"}

%description
A test package to check Lua scripting in RPM spec files.

%prep
echo "Lua test value: %{lua_test_value}"

%build
# Nothing to build

%install
# Nothing to install

%files
# No files

%changelog
* Wed Dec 20 2023 Your Name <you@example.com> - 1.0-1
- Initial package
