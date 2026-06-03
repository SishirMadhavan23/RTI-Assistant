from pathlib import Path
import re


def test_required_top_level_files_exist():
    required_files = [
        "README.md",
        "requirements.txt",
        "requirements-dev.txt",
        "LICENSE",
        "Makefile",
        "pytest.ini",
        ".coveragerc",
        ".flake8",
        ".pre-commit-config.yaml",
        ".gitleaks.toml",
        ".env.example",
        "Dockerfile",
    ]

    for file_name in required_files:
        assert Path(file_name).is_file()


def test_requirements_include_runtime_and_test_dependencies():
    requirements = Path("requirements.txt").read_text(encoding="utf-8").splitlines()
    dev_requirements = Path("requirements-dev.txt").read_text(encoding="utf-8").splitlines()

    expected_packages = [
        "streamlit",
        "langchain",
        "langchain-community",
        "langchain-huggingface",
        "faiss-cpu",
        "transformers",
        "pytest",
        "pytest-cov",
        "coverage",
        "pip-audit",
        "pre-commit",
        "black",
        "mypy",
        "bandit",
        "vulture",
        "pylint",
        "flake8",
        "pyupgrade",
        "ruff",
    ]

    for package in expected_packages:
        assert package in requirements

    assert "-r requirements.txt" in dev_requirements
    assert "semgrep" in dev_requirements


def test_pytest_coverage_configuration_is_present():
    pytest_config = Path("pyproject.toml").read_text(encoding="utf-8")
    pytest_ini_config = Path("pytest.ini").read_text(encoding="utf-8")
    fail_under_match = re.search(r"--cov-fail-under=(\d+)", pytest_config)

    assert "[tool.pytest.ini_options]" in pytest_config
    assert 'testpaths = ["tests"]' in pytest_config
    assert "--cov=." in pytest_config
    assert "--cov-report=term-missing" in pytest_config
    assert "--cov-report=xml" in pytest_config
    assert "--cov-report=html" in pytest_config
    assert "--cov=." in pytest_ini_config
    assert "--cov-report=term-missing" in pytest_ini_config
    assert "--cov-report=xml" in pytest_ini_config
    assert "--cov-report=html" in pytest_ini_config
    assert "--cov-fail-under=51" in pytest_ini_config
    assert fail_under_match is not None
    assert int(fail_under_match.group(1)) > 50


def test_coverage_reporting_configuration_is_present():
    coverage_config = Path(".coveragerc").read_text(encoding="utf-8")
    pyproject_config = Path("pyproject.toml").read_text(encoding="utf-8")

    assert "[report]" in coverage_config
    assert "show_missing = True" in coverage_config
    assert "fail_under = 51" in coverage_config
    assert "[xml]" in coverage_config
    assert "output = coverage.xml" in coverage_config
    assert "[html]" in coverage_config
    assert "directory = htmlcov" in coverage_config

    assert "[tool.coverage.report]" in pyproject_config
    assert "fail_under = 51" in pyproject_config
    assert "[tool.coverage.xml]" in pyproject_config
    assert "[tool.coverage.html]" in pyproject_config

    makefile = Path("Makefile").read_text(encoding="utf-8")
    assert "coverage-report:" in makefile
    assert "--cov-report=term-missing" in makefile
    assert "--cov-report=xml" in makefile
    assert "--cov-report=html" in makefile


def test_dependency_audit_configuration_is_present():
    makefile = Path("Makefile").read_text(encoding="utf-8")
    readme = Path("README.md").read_text(encoding="utf-8")
    security = Path("SECURITY.md").read_text(encoding="utf-8")
    pre_commit_config = Path(".pre-commit-config.yaml").read_text(encoding="utf-8")

    assert "audit:" in makefile
    assert "dependency-audit:" in makefile
    assert "pip-audit -r requirements.txt" in makefile
    assert "pip-audit -r requirements.txt" in readme
    assert "pip-audit -r requirements.txt" in security
    assert "id: pip-audit" in pre_commit_config
    assert "requirements.txt" in pre_commit_config
    assert "Dependency audit" in readme


def test_pre_commit_hooks_cover_lint_format_types_security_and_quality():
    pre_commit_config = Path(".pre-commit-config.yaml").read_text(encoding="utf-8")

    expected_hooks = [
        "id: ruff",
        "id: ruff-format",
        "id: black",
        "id: mypy",
        "id: bandit",
        "id: pip-audit",
        "id: pyupgrade",
        "id: flake8",
        "id: pylint",
        "id: vulture",
        "id: semgrep",
        "id: gitleaks",
        "id: trailing-whitespace",
        "id: end-of-file-fixer",
        "id: check-yaml",
        "id: check-toml",
        "id: check-added-large-files",
    ]

    for hook in expected_hooks:
        assert hook in pre_commit_config

    assert "--config=.gitleaks.toml" in pre_commit_config


def test_tooling_configuration_is_declared_in_pyproject():
    pyproject_config = Path("pyproject.toml").read_text(encoding="utf-8")

    expected_sections = [
        "[tool.ruff]",
        "[tool.black]",
        "[tool.mypy]",
        "[tool.bandit]",
        "[tool.pylint.main]",
        "[tool.vulture]",
        "[tool.flake8]",
        "[tool.pytest.ini_options]",
        "[tool.coverage.report]",
        "[tool.coverage.xml]",
        "[tool.coverage.html]",
    ]

    for section in expected_sections:
        assert section in pyproject_config
