from typer.testing import CliRunner

from mtg_token_generator.cli import app


def test_cli_help_exposes_icon_flags():
    result = CliRunner().invoke(app, ["--help"])

    assert result.exit_code == 0
    assert "--generate-icons" in result.output
    assert "--no-generate" in result.output
    assert "--regen-icons" in result.output
    assert "--icon-provider" in result.output
    assert "--generate-previe" in result.output
    assert "--no-generate-pre" in result.output
