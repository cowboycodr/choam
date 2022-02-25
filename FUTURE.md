# Choam's future

## Proposals

### Choam script downloading
With the addition of renaming Choam's `run` command to `script` I am also considering implementing the ability to download choam scripts through the internet from a choam hosted domain such as `https://choam.org/api/scripts`

Downloading example:

`$ choam script cowboycodr/fmt --download`

Which would then add it to the `Choam.toml` and allow you to use it in development.