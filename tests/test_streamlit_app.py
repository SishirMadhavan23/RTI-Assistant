import ast
from pathlib import Path

APP_PATH = Path("app.py")


def _app_source() -> str:
    return APP_PATH.read_text(encoding="utf-8")


def _app_tree() -> ast.Module:
    return ast.parse(_app_source())


def test_streamlit_app_file_exists():
    assert APP_PATH.is_file()


def test_app_configures_streamlit_page():
    source = _app_source()

    assert "st.set_page_config" in source
    assert 'page_title="RTI Assistant AI"' in source
    assert 'layout="wide"' in source


def test_app_defines_cached_resource_loaders():
    source = _app_source()
    tree = _app_tree()
    function_names = {node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)}

    assert {"load_db", "load_model"}.issubset(function_names)
    assert source.count("@st.cache_resource") >= 2


def test_app_has_core_user_flows():
    source = _app_source()

    expected_ui = [
        "Ask your RTI Question",
        "Suggested Questions",
        "RTI Draft Generator",
        "Generate Draft",
        "Download Draft",
        "Sources Used",
    ]

    for label in expected_ui:
        assert label in source


def test_app_keeps_session_history():
    source = _app_source()

    assert '"history" not in st.session_state' in source
    assert "st.session_state.history.append" in source
