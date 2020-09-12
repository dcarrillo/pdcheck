# Pager Duty check

A POC for a multi os (QT5) system tray app for checking pager duty incident status. Currently
when an incident is triggered or marked as acknowledge an icon is shown accordingly at your system
tray, when clicking, a menu with links to the Pager Duty incident page is shown.

## Configuration

### Auth

An API Token from your Pager Duty settings is needed.

### Configuration file

Create a file named `pdcheck.yml` at the same level of `pdcheck.py`, example:

```yaml
---

interval: 30         # Interval between checks, 30 seconds by default
pd_api_key: xxxxxx   # Pager Duty API key
pd_teams:            # Array of team identifiers to filtering by. Empty by default.
  - XXXXXX
pd_users:            # Array of user identifiers to filtering by. Empty by default.
  - XXXXXXX
```

The system environment variable `PD_API_KEY` can be used innstead of setting `pd_api_key`.
