# AGENTS.md

이 저장소에서 작업하는 AI 코딩 에이전트를 위한 안내입니다.

## 프로젝트 개요

Markdown 문서를 읽어 Word(.docx) 문서로 변환하는 파이썬 프로젝트입니다.

- `reader/` — 마크다운 등 문서를 읽고 파싱하는 모듈 (`MarkdownReader`)
- `writer/` — Word 문서를 생성/저장하는 모듈 (`WordWriter`, `python-docx` 기반)
- `main.py` — 진입점

## 개발 환경

- 패키지/의존성 관리는 `uv`를 사용합니다. `pip`을 직접 사용하지 마세요.
- Python 버전은 `.python-version`(3.12)을 따릅니다.
- 의존성 설치: `uv sync`
- 실행: `uv run main.py`

## 코드 작성 규칙

- 새 모듈을 추가할 때는 `reader`, `writer`처럼 역할별 패키지로 분리하세요.
- 타입 힌트를 사용하고, 공개 함수/메서드에는 docstring을 작성하세요 (기존 코드 스타일 참고).
- 커밋 메시지, 주석, docstring은 기존 코드처럼 한국어를 사용해도 됩니다.

## 린트 / 포맷

- 린트: `uv run ruff check .`
- 포맷: `uv run ruff format .`
- 규칙은 `pyproject.toml`의 `[tool.ruff]`를 따르며, `tests/`는 린트 대상에서 제외됩니다.
- 커밋 전 `uv run pre-commit install`로 pre-commit 훅(ruff lint/format 체크)을 활성화할 수 있습니다.

## 테스트

- 테스트 러너: `pytest` (`uv run pytest`)
- 테스트 파일은 `tests/` 디렉터리에 `test_*.py` 형식으로 작성합니다 (`pyproject.toml`의 `[tool.pytest.ini_options]` 참고).
- 코드를 변경한 뒤에는 관련 테스트를 실행해서 통과를 확인하세요. 새 기능/버그 수정에는 테스트를 함께 추가하는 것을 권장합니다.

## PR / 커밋 전 체크리스트

1. `uv run ruff check .`
2. `uv run ruff format --check .`
3. `uv run pytest`

위 명령이 모두 통과해야 합니다.
