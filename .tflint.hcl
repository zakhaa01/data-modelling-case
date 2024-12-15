config {
  format = "compact"
  plugin_dir = "~/.tflint.d/plugins"
  module = false
  force = false
  disabled_by_default = false
}

plugin "terraform" {
    // Plugin common attributes
    enabled = true
    preset = "recommended"
}

plugin "aws" {
    enabled = true
    version = "0.28.0"
    source  = "github.com/terraform-linters/tflint-ruleset-aws"
}

rule "aws_secretsmanager_secret_version_invalid_secret_string" {
  enabled = false
}
