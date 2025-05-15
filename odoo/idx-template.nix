# Originally part of the project idx under the Apache 2.0 license
# Modified by Marco Román on 05-15-2025

{ pkgs, version ? "17", ... }: {
  packages = [
    pkgs.git
  ];

  bootstrap = let
    packagesV15 = [
      pkgs.gcc
      pkgs.python39
      pkgs.python39Packages.pip
      pkgs.python39Packages.setuptools
      pkgs.python39Packages.virtualenv
      pkgs.openldap
      pkgs.openldap.dev
      pkgs.cyrus_sasl.dev
      pkgs.libpqxx
      pkgs.libxml2.dev
      pkgs.libxslt.dev
    ];
    packagesV16 = [
      pkgs.gcc
      pkgs.python311
      pkgs.python311Packages.pip
      pkgs.python311Packages.setuptools
      pkgs.python311Packages.virtualenv
      pkgs.openldap
      pkgs.openldap.dev
      pkgs.cyrus_sasl.dev
      pkgs.libpqxx
    ];
    packagesV17 = packagesV16;

    odooPackages = builtins.getAttr ("packagesV" + version) {
      inherit packagesV15 packagesV16 packagesV17;
    };
  in
    ''
      mkdir "$out"
      cd "$out"

      mkdir -p .idx/.data/
      mkdir -p .vscode/

      cat > .idx/dev.nix <<EOF
{ pkgs, ... }: {
  channel = "stable-24.05";
  packages = [
    ${builtins.concatStringsSep "\n    " (map (p: "pkgs.${p.name or "unknown"}") odooPackages)}
  ];
  services.postgres.enable = true;

  idx = {
    extensions = [
      "ms-python.python"
    ];
    previews = {
      enable = true;
      previews = {
        web = {
          command = ["sh" "httpserver.sh" "\$PORT"];
          manager = "web";
        };
      };
    };
    workspace = {
      onCreate = {
        odoo-install = ''
          set -e
          echo "✅ Creando entorno virtual..."
          python -m venv .venv
          source .venv/bin/activate
          pip install --upgrade pip
          pip install -r .idx/.data/odoo/requirements.txt

          BIN_PATH="$(pwd)/.idx/.data/odoo/odoo-bin"
          if [ -f "$BIN_PATH" ]; then
            ln -s "$BIN_PATH" .venv/bin/odoo-bin
          fi

          odoo-bin --save --stop-after-init
          mv ../.odoorc odoo.conf

          sed -i \
            -e "/^addons_path =/ s|$|,$(pwd)/custom_addons|" \
            -e "s|.local/share/Odoo|.idx/.data/odoo-data|g" \
            odoo.conf
        '';
        default.openFiles = [ "README.md" ];
      };
    };
  };
}
EOF

      cp -f ${./httpserver.sh} "httpserver.sh"
      cp -f ${./README.md} "README.md"
      cp -f ${./settings.json} ".vscode/settings.json"
      printf "/.idx/odoo\n/.idx/odoo-data" > ".gitignore"

      git clone https://github.com/odoo/odoo.git --single-branch --branch ${version}.0 --depth 1 .idx/.data/odoo

      mkdir custom_addons/

      cd ..
      chmod -R +w "$out"
    '';
}
