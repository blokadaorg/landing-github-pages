# Blokada Landing GitHub Pages - Scripts Documentation

## Overview

This repository contains scripts for managing blocklists and mirrors for the Blokada project. The scripts handle whitelist generation, blocklist processing, and mirror synchronization.

## Scripts Workflow

### Whitelist Management

1. **Manual Whitelist Entry**
   - Add domains to `scripts/whitelist-manual` (one domain per line)
   - **Domain Types**:
     - `domain.com` - Exact match only (allows API subdomains to be blocked separately)
     - `*.domain.com` - Wildcard match (protects all subdomains)
   - Examples:
     - `example.com` - Only protects example.com, allows `track.example.com` to be blocked
     - `*.example.org` - Protects all example.org subdomains

2. **Whitelist Generation & Testing**
   - Run `make test` to verify whitelist filtering logic
   - Master whitelist is automatically generated during sync process
   - Master whitelist combines:
     - Manual whitelist (`scripts/whitelist-manual`)
     - External whitelist sources (`scripts/whitelist-sets`)
   - Output: `scripts/whitelist` (master whitelist file)

3. **Mirror Synchronization**
   - Run `make sync` to update all mirrors (includes test verification + whitelist generation)
   - This runs tests first, generates updated whitelist, then calls `./sync-mirrors.sh`
   - The sync script processes:
     - `./ddg.py` - DuckDuckGo tracker radar (with whitelist filtering)
     - `./exodus.py` - Exodus Privacy trackers (with whitelist filtering)
     - `./mirror.py` - External blocklists (with whitelist filtering)

## Key Scripts

### `gen-whitelist.py`
- **Purpose**: Generates master whitelist from manual entries and external sources
- **Input**: 
  - `whitelist-manual` - manually added domains
  - `whitelist-sets` - URLs to external whitelist sources
- **Output**: `whitelist` - combined whitelist file
- **Usage**: `./gen-whitelist.py [-o <output-file>]`

### `ddg.py`
- **Purpose**: Processes DuckDuckGo Tracker Radar data
- **Filtering**: Uses `scripts/whitelist` to filter out whitelisted domains
- **Output**: `../blocklists/ddgtrackerradar/standard/hosts.txt`
- **Features**: 
  - Filters by category (skips CDN, Online Payment, Non-Tracking)
  - Filters by subdomain patterns
  - Respects resource count thresholds

### `exodus.py`
- **Purpose**: Processes Exodus Privacy tracker database
- **Filtering**: Uses `scripts/whitelist` to filter out whitelisted domains
- **Output**: `../blocklists/exodusprivacy/standard/hosts.txt`
- **Features**: 
  - Filters out common subdomains (www, api, cdn)
  - Respects master whitelist

### `mirror.py`
- **Purpose**: Downloads and mirrors external blocklists
- **Filtering**: Uses `WhitelistFilter` class with `scripts/whitelist`
- **Output**: `../mirror/v5/` directory structure
- **Features**:
  - Downloads from multiple external sources (1hosts, StevenBlack, etc.)
  - Normalizes entries first (`hostname_normalizer.py`): strips leading dots, converts IDNs to punycode, drops entries that still aren't hostnames
  - Applies sophisticated whitelist filtering to all downloaded content
  - Supports custom merging and wildcard prefixing
  - Handles various formats:
    - Standard host files: `0.0.0.0 domain.com`, `127.0.0.1 domain.com`
    - Plain domains: `domain.com`
    - uBlock Origin format: `||domain.com^`, `||domain.com^$options`

### `whitelist_filter.py`
- **Purpose**: Reusable whitelist filtering module
- **Features**:
  - Exact domain matching (default behavior)
  - Wildcard support (`*.domain.com` for subdomain protection)
  - uBlock Origin format parsing
  - Comprehensive test suite (9 tests)
- **Usage**: `python whitelist_filter.py` to run tests

### `sync-mirrors.sh`
- **Purpose**: Master script to update all mirrors and blocklists
- **Process**:
  1. Updates tracker-radar repository
  2. Runs `ddg.py` (DuckDuckGo processing)
  3. Runs `exodus.py` (Exodus Privacy processing)
  4. Runs `mirror.py` (external blocklist mirroring)
  5. Commits changes to git

### `Makefile`
- **Purpose**: Provides safe build targets with dependency management
- **Targets**:
  - `make test` - Runs whitelist filtering and hostname normalizer tests
  - `make gen-whitelist` - Generates master whitelist from manual entries
  - `make sync` - Runs tests, generates whitelist, then syncs mirrors (only if tests pass)

## File Structure

```
scripts/
├── whitelist-manual          # Manually curated whitelist entries
├── whitelist-sets           # URLs to external whitelist sources
├── whitelist               # Generated master whitelist (output)
├── whitelist-subdomains    # Subdomain patterns for filtering
├── gen-whitelist.py        # Whitelist generator
├── ddg.py                 # DuckDuckGo tracker processor
├── exodus.py              # Exodus Privacy processor
├── mirror.py              # External blocklist mirror
├── hostname_normalizer.py # Leading-dot / IDN entry normalization
└── sync-mirrors.sh        # Master sync script
```

## Troubleshooting

### Issue: Whitelisted domains still appear in mirrors
**Solution**: Follow the complete workflow:
1. Add domain to `scripts/whitelist-manual` (use `*.domain.com` for subdomains)
2. Run `make test` to verify filtering logic
3. Run `make sync` to regenerate all mirrors with improved filtering

### Issue: Tests fail before sync
**Cause**: Whitelist filtering logic has issues
**Solution**: 
- Check test output for specific failures
- Run `python whitelist_filter.py` for detailed test results
- Fix whitelist logic before running sync

### Issue: Scripts fail to load whitelist
**Cause**: Missing `scripts/whitelist` file
**Solution**: Run `./gen-whitelist.py` first to generate the master whitelist

### Issue: Want to block tracking subdomains but not main domain
**Solution**: Use exact matching in whitelist
- ✅ Add `example.com` to whitelist (allows `track.example.com` to be blocked)  
- ❌ Don't use `*.example.com` (would protect all subdomains)

## Recent Changes

- **2025-09-12**: Complete whitelist filtering overhaul
  - Added `WhitelistFilter` class with comprehensive test suite
  - Implemented exact domain matching vs wildcard support
  - Added uBlock Origin format support (`||domain.com^`)
  - Updated workflow to use `make sync` with automated test verification and whitelist generation
  - Enhanced Makefile with proper dependency management

## Commands Reference

```bash
# Test whitelist filtering logic (recommended before changes)
make test

# Generate master whitelist (if needed manually)
make gen-whitelist

# Sync all mirrors safely (tests + whitelist generation + sync)
make sync

# Manual operations (not recommended - bypasses safety checks)
./gen-whitelist.py           # Generate whitelist manually
./sync-mirrors.sh            # Sync without tests

# Individual script runs (for debugging)
./ddg.py
./exodus.py  
./mirror.py

# Test individual components
python whitelist_filter.py  # Run whitelist filter tests
```