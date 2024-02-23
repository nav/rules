with (import <nixpkgs> {});
let
    basePackages = [
        pkgs.uv
        pkgs.python39
    ];
    extensionPath = ./local.nix;
    inputs = basePackages
             ++ lib.optional (builtins.pathExists extensionPath) (import extensionPath {}).inputs;

    baseHooks = ''
        export PIP_PREFIX="$(pwd)/.venv"
        export PYTHONPATH="$PYTHONPATH:$PIP_PREFIX/${pkgs.python39.sitePackages}"
        export PATH="$PIP_PREFIX/bin:$PATH"
        export PIP_NO_CACHE_DIR=true
        unset SOURCE_DATE_EPOCH
    '';

    shellHooks = baseHooks
                 + lib.optionalString (builtins.pathExists extensionPath) (import extensionPath {}).hooks;
in mkShell {
    buildInputs = inputs;
    shellHooks = shellHooks;
}
