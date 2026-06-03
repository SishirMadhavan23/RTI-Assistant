from pathlib import Path

ASSET_PATH = Path("assets/style.css")
DATA_PATH = Path("data")
VECTORSTORE_PATH = Path("vectorstore")


def test_required_project_directories_exist():
    for path in [Path("assets"), DATA_PATH, VECTORSTORE_PATH]:
        assert path.is_dir()


def test_stylesheet_exists_and_contains_main_classes():
    css = ASSET_PATH.read_text(encoding="utf-8")

    expected_selectors = [
        ".stApp",
        ".main-title",
        ".subtitle",
        ".chat-user",
        ".chat-ai",
        ".stButton button",
    ]

    for selector in expected_selectors:
        assert selector in css


def test_data_folder_contains_rti_pdf_sources():
    pdf_names = {path.name for path in DATA_PATH.glob("*.pdf")}

    assert "RTI-Act_English.pdf" in pdf_names
    assert "RTIRules_2012_English_0.pdf" in pdf_names
    assert "FAQ_RTI_2012 (1).pdf" in pdf_names


def test_vectorstore_contains_faiss_index_files():
    assert (VECTORSTORE_PATH / "index.faiss").is_file()
    assert (VECTORSTORE_PATH / "index.pkl").is_file()
