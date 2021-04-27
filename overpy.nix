{ lib, buildPythonPackage, fetchPypi, pytest, pytest-runner }:

buildPythonPackage rec {
  pname = "overpy";
  version = "0.6";

  nativeBuildInputs = [ pytest pytest-runner ];

  src = fetchPypi {
    inherit pname version;
    sha256 = "sha256:14117s63m6l22s9j4fc6ai2ky9qd2mpxz15d9pg8lgas8hn4dykm";
  };
}
