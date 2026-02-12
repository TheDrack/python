# Browser Extension Manager

## Overview

The Browser Extension Manager is a component of the Jarvis automation platform that manages browser extensions for complex Playwright-based automations. It provides a clean interface for installing, enabling, disabling, and managing browser extensions that can be loaded into Chromium browsers for enhanced automation capabilities.

## Features

- **Extension Installation**: Install browser extensions from source directories
- **Dynamic Enable/Disable**: Toggle extensions on and off without reinstalling
- **Persistent Storage**: Extensions are stored and tracked across sessions
- **Chromium Integration**: Seamless integration with Playwright's Chromium browser
- **Metadata Tracking**: Store and retrieve metadata about each extension

## Architecture

### Components

1. **BrowserExtension**: A data model representing a single browser extension
2. **BrowserExtensionManager**: The main service class that manages extensions

### Storage

Extensions are stored in:
- Default location: `~/.jarvis/browser_extensions/`
- Manifest file: `~/.jarvis/browser_extensions/manifest.json`

Each extension has:
- A unique `extension_id`
- A human-readable `name`
- A `path` to the extension directory
- An `enabled` status flag
- Optional `metadata` dictionary

## Usage

### Basic Example

```python
from app.application.services.browser_extension_manager import BrowserExtensionManager
from pathlib import Path

# Initialize the manager
manager = BrowserExtensionManager()

# Install an extension
source_path = Path("/path/to/my-extension")
manager.install_extension(
    extension_id="my-automation-ext",
    name="My Automation Extension",
    source_path=source_path,
    metadata={"version": "1.0", "author": "Developer"}
)

# List all extensions
extensions = manager.list_extensions()
for ext in extensions:
    print(f"{ext.name}: {ext.enabled}")

# Disable an extension
manager.disable_extension("my-automation-ext")

# Get Chromium launch arguments
chromium_args = manager.get_extension_args_for_chromium()
```

### Integration with Browser Manager

The Browser Extension Manager is automatically integrated with the `PersistentBrowserManager`:

```python
from app.application.services.browser_manager import PersistentBrowserManager

# Browser manager automatically loads extensions
browser_manager = PersistentBrowserManager()

# Extensions are loaded when starting the browser
cdp_url = browser_manager.start_browser()

# Access the extension manager
ext_manager = browser_manager.extension_manager
ext_count = ext_manager.get_extension_count()
print(f"Loaded {ext_count['enabled']} extensions")
```

### Extension Directory Structure

Each extension should follow the Chrome Extension manifest format:

```
my-extension/
├── manifest.json          # Extension manifest
├── content.js            # Content scripts
├── background.js         # Background scripts
├── popup.html           # Extension popup (optional)
└── icons/               # Extension icons (optional)
    ├── icon16.png
    ├── icon48.png
    └── icon128.png
```

## API Reference

### BrowserExtensionManager

#### Methods

##### `__init__(extensions_dir: Optional[Path] = None)`
Initialize the extension manager.

**Parameters:**
- `extensions_dir`: Custom directory for storing extensions (default: `~/.jarvis/browser_extensions`)

##### `install_extension(extension_id: str, name: str, source_path: Path, metadata: Optional[Dict] = None) -> bool`
Install a browser extension.

**Parameters:**
- `extension_id`: Unique identifier for the extension
- `name`: Human-readable name
- `source_path`: Path to the extension source directory
- `metadata`: Optional metadata dictionary

**Returns:** `True` if successful, `False` otherwise

##### `uninstall_extension(extension_id: str) -> bool`
Uninstall a browser extension.

**Parameters:**
- `extension_id`: Extension identifier

**Returns:** `True` if successful, `False` otherwise

##### `enable_extension(extension_id: str) -> bool`
Enable a browser extension.

**Parameters:**
- `extension_id`: Extension identifier

**Returns:** `True` if successful, `False` otherwise

##### `disable_extension(extension_id: str) -> bool`
Disable a browser extension.

**Parameters:**
- `extension_id`: Extension identifier

**Returns:** `True` if successful, `False` otherwise

##### `get_extension(extension_id: str) -> Optional[BrowserExtension]`
Get an extension by ID.

**Parameters:**
- `extension_id`: Extension identifier

**Returns:** `BrowserExtension` object if found, `None` otherwise

##### `list_extensions(enabled_only: bool = False) -> List[BrowserExtension]`
List all extensions.

**Parameters:**
- `enabled_only`: If `True`, only return enabled extensions

**Returns:** List of `BrowserExtension` objects

##### `get_enabled_extension_paths() -> List[str]`
Get paths to all enabled extensions.

**Returns:** List of extension paths as strings

##### `get_extension_args_for_chromium() -> List[str]`
Get Chromium launch arguments for loading enabled extensions.

**Returns:** List of command-line arguments

##### `get_extension_count() -> Dict[str, int]`
Get counts of extensions by status.

**Returns:** Dictionary with `total`, `enabled`, and `disabled` counts

## Use Cases

### 1. Ad Blocker for Web Scraping

Install an ad blocker extension to improve web scraping performance:

```python
manager = BrowserExtensionManager()
manager.install_extension(
    "ublock-origin",
    "uBlock Origin",
    Path("/path/to/ublock-extension"),
    metadata={"purpose": "Ad blocking for cleaner scraping"}
)
```

### 2. Custom Automation Scripts

Load custom content scripts for specific automation tasks:

```python
# Create a custom extension for automation
custom_ext_dir = Path("/tmp/custom-automation")
custom_ext_dir.mkdir(exist_ok=True)

# Create manifest
manifest = {
    "name": "Jarvis Automation Helper",
    "version": "1.0",
    "manifest_version": 3,
    "content_scripts": [{
        "matches": ["<all_urls>"],
        "js": ["helper.js"]
    }]
}

(custom_ext_dir / "manifest.json").write_text(json.dumps(manifest))
(custom_ext_dir / "helper.js").write_text("""
    // Custom automation helper
    console.log('Jarvis automation helper loaded');
    window.jarvisHelpers = {
        extractData: function() { /* ... */ }
    };
""")

# Install the extension
manager.install_extension(
    "jarvis-helper",
    "Jarvis Automation Helper",
    custom_ext_dir
)
```

### 3. Development Tools

Load development tools for debugging automations:

```python
# Install Chrome DevTools extension
manager.install_extension(
    "devtools-helper",
    "DevTools Helper",
    Path("/path/to/devtools-ext"),
    metadata={"category": "development"}
)

# Enable only during development
if settings.DEBUG:
    manager.enable_extension("devtools-helper")
else:
    manager.disable_extension("devtools-helper")
```

## Best Practices

1. **Use Descriptive IDs**: Use kebab-case identifiers that describe the extension's purpose
2. **Track Versions**: Include version information in metadata for easier management
3. **Enable Selectively**: Only enable extensions that are needed for the current automation
4. **Clean Up**: Regularly uninstall unused extensions to keep the system clean
5. **Test Compatibility**: Test extensions in isolation before using in production automations

## Troubleshooting

### Extension Not Loading

If an extension doesn't load:

1. Check the manifest.json format
2. Verify the extension path exists
3. Check browser console for extension errors
4. Ensure the extension is enabled: `manager.get_extension("ext-id").enabled`

### Permission Issues

If you encounter permission errors:

1. Check directory permissions for `~/.jarvis/browser_extensions/`
2. Ensure the source extension directory is readable
3. Run with appropriate user permissions

### Chromium Compatibility

Not all Chrome extensions work with Playwright's Chromium:

1. Use Manifest V3 extensions when possible
2. Avoid extensions that require Chrome Web Store APIs
3. Test extensions thoroughly in Playwright context

## Related Components

- **PersistentBrowserManager**: Manages browser instances and loads extensions
- **TaskRunner**: Executes automation scripts that may use browser extensions
- **ExtensionManager**: Manages Python package extensions (different from browser extensions)

## Future Enhancements

- Extension marketplace integration
- Automatic extension updates
- Extension dependency management
- Performance profiling per extension
- Extension sandboxing and security scanning
