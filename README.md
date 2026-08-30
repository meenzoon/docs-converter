# docs-converter

Markdown 문서를 읽어 Word(.docx) 문서로 변환하는 파이썬 프로젝트입니다.

## 주요 구성

- `reader/markdown_reader.py` — `MarkdownReader`: 마크다운 파일/문자열을 읽고 제목, 헤딩, 문단, 코드 블록, 링크, 이미지, 섹션 단위로 파싱합니다.
- `writer/docx.py` — `WordWriter`: `python-docx` 기반으로 Word 문서를 생성하거나 기존 문서를 열어 제목/문단을 추가하고 저장합니다.
- `main.py` — 진입점 스크립트.

## 요구 사항

- Python >= 3.12
- [uv](https://docs.astral.sh/uv/) (의존성 관리 및 실행)

## 설치

```bash
uv sync
```

## 실행

```bash
uv run main.py
```

## 개발

### 테스트

```bash
uv run pytest
```

### 린트 / 포맷

```bash
uv run ruff check .
uv run ruff format .
```

### pre-commit

커밋 전 자동으로 ruff lint/format 검사를 실행합니다.

```bash
uv run pre-commit install
```

## 라이선스

[LICENSE](./LICENSE) 파일을 참고하세요.
