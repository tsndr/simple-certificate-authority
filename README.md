# Simple Certificate Authority

This is just a simplified CLI for OpenSSL to make it easier to issue self signed certificates.

`ca help`
```
USAGE
  ca help
  ca <COMMAND> help
  ca <COMMAND> <SUBCOMMAND> help

COMMANDS
  init            Generate root key and root certificate
  key             Manage private keys
  request         Manage certificate requests
  certificate     Manage certificates
```

`ca certificate help`
```
USAGE
  ca certificate help
  ca certificate <COMMAND> help

COMMANDS
  list            List all certificates
  get             Get certificate content
  create          Create a new certificate
  delete          Delete existing certificate
```
