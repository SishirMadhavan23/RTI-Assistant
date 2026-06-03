import ast
from pathlib import Path

INGEST_PATH = Path("ingest.py")


def _ingest_source() -> str:
    return INGEST_PATH.read_text(encoding="utf-8")


def test_ingest_script_exists():
    assert INGEST_PATH.is_file()


def test_ingest_pipeline_uses_expected_langchain_components():
    source = _ingest_source()

    expected_components = [
        "PyPDFLoader",
        "RecursiveCharacterTextSplitter",
        "FAISS",
        "HuggingFaceEmbeddings",
    ]

    for component in expected_components:
        assert component in source


def test_ingest_only_loads_pdf_files_from_data_folder():
    source = _ingest_source()

    assert 'os.listdir("data")' in source
    assert '.endswith(".pdf")' in source


def test_ingest_creates_reasonable_document_chunks():
    source = _ingest_source()

    assert "chunk_size=500" in source
    assert "chunk_overlap=50" in source


def test_ingest_saves_vectorstore_locally():
    tree = ast.parse(_ingest_source())
    calls = [node for node in ast.walk(tree) if isinstance(node, ast.Call)]

    assert any(
        isinstance(call.func, ast.Attribute)
        and call.func.attr == "save_local"
        and call.args
        and isinstance(call.args[0], ast.Constant)
        and call.args[0].value == "vectorstore"
        for call in calls
    )
