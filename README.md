# TTMS Hugo Base Template

This is the base Hugo template used by the TTMS Client Provisioning Service (CPS) to create new client sites.

## Template Variables

The following placeholders will be automatically replaced when creating a new client site:

- `{{CLIENT_NAME}}` - The client's subdomain name (e.g., `sipontheave`)
- `{{SITE_TITLE}}` - The site title (e.g., "Sip on the Ave")
- `{{ANALYTICS_ID}}` - Matomo analytics site ID
- `{{WHATSAPP}}` - WhatsApp contact number
- `{{PHONE}}` - Phone contact number
- `{{EMAIL}}` - Email contact address

## Structure

```
├── archetypes/         # Content templates
├── content/            # Markdown content files
├── data/               # Data files (locations.yaml)
├── layouts/            # Hugo layouts
├── static/             # Static assets
│   ├── branding/       # Logos, favicons, images
│   ├── css/            # Custom CSS
│   ├── js/             # Custom JavaScript
│   └── main/           # Main images
├── themes/             # Hugo theme (git submodule)
├── scripts/            # Helper scripts
├── hugo.toml           # Hugo configuration (with placeholders)
├── netlify.toml        # Netlify deployment config
└── build.sh            # Build script

## Theme

The theme `_menus_ttms` is added as a git submodule from:
https://github.com/anomrac21/ttms-app-cluster (subdirectory: `_menus_ttms`)

## Usage by CPS

1. CPS clones this repository as a template
2. Replaces all `{{VARIABLE}}` placeholders with actual values
3. Updates `data/locations.yaml` with location information
4. Adds custom branding images
5. Creates a new GitHub repository
6. Deploys to Netlify

## Local Development

```bash
# Install Hugo
# Clone this repo
git clone https://github.com/anomrac21/ttms-hugo-base.git
cd ttms-hugo-base

# Initialize theme submodule
git submodule update --init --recursive

# Run Hugo dev server
hugo server -D
```

## Building

```bash
# Build for production
hugo --minify

# Or use the build script
./build.sh
```

## License

Proprietary - TTMS (Trinidad & Tobago Menu Service)

