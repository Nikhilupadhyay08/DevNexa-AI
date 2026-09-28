from app.agents.tool_selector import select_tool
from app.agents.tools import (
    find_references_tool,
    read_file_tool,
    search_code_tool,
)
from app.services.github import get_source_files
from app.services.llm import LLMService, OllamaProvider


llm_service = LLMService(
    provider=OllamaProvider()
)


class DevNexaAgent:
    async def run(
        self,
        question: str,
    ) -> str:
        if not question.strip():
            raise ValueError(
                "Question cannot be empty"
            )

        selected_tool = select_tool(question)

        print(
            f"\n[DevNexa Agent] Selected tool: "
            f"{selected_tool}"
        )

        if selected_tool == "search_code":
            return await self._run_search_code(
                question
            )

        if selected_tool == "read_file":
            return await self._run_read_file(
                question
            )

        if selected_tool == "find_references":
            return await self._run_find_references(
                question
            )

        return "Unable to determine the appropriate tool."

    async def _run_search_code(
        self,
        question: str,
    ) -> str:
        search_results = search_code_tool(
            query=question,
            limit=5,
        )

        if not search_results:
            return "No relevant code was found."

        context_parts = []

        for index, result in enumerate(
            search_results,
            start=1,
        ):
            context_parts.append(
                f"""--- Search Result {index} ---
File: {result["path"]}
Chunk: {result["chunk_index"]}
Similarity: {result["score"]:.4f}

{result["content"]}
"""
            )

        context = "\n".join(context_parts)

        prompt = f"""
You are DevNexa AI, an AI software engineering agent.

Answer the user's question using the retrieved repository code.

Rules:
- Use the repository code as your primary source.
- Do not invent files, functions, or implementation details.
- Mention relevant file paths when useful.
- If the context is insufficient, clearly say so.

Retrieved Repository Code:
{context}

User Question:
{question}

Answer:
"""

        return llm_service.generate(prompt)

    async def _run_read_file(
        self,
        question: str,
    ) -> str:
        requested_filename = self._extract_filename(
            question
        )

        if not requested_filename:
            return (
                "Please specify the repository file "
                "you want to inspect."
            )

        source_files = await get_source_files(
            owner="Nikhilupadhyay08",
            repository="DevNexa-AI",
            branch="main",
        )

        matching_files = [
            file
            for file in source_files
            if file["path"].split("/")[-1].lower()
            == requested_filename.lower()
        ]

        if not matching_files:
            return (
                f"Could not find a file named "
                f"{requested_filename}."
            )

        if len(matching_files) > 1:
            paths = "\n".join(
                file["path"]
                for file in matching_files
            )

            return (
                f"Multiple files named "
                f"{requested_filename} were found:\n"
                f"{paths}"
            )

        file_path = matching_files[0]["path"]

        print(
            f"\n[DevNexa Agent] Selected file path: "
            f"{file_path}"
        )

        content = await read_file_tool(
            owner="Nikhilupadhyay08",
            repository="DevNexa-AI",
            path=file_path,
            branch="main",
        )

        if self._is_complete_file_request(question):
            return (
                f"Complete file: {file_path}\n\n"
                f"```text\n"
                f"{content}\n"
                f"```"
            )

        answer_prompt = f"""
You are DevNexa AI, an AI software engineering agent.

The user wants to understand a repository file.

Use only the actual file content provided below.

Rules:
- Do not invent implementation details.
- Do not modify or rewrite the code.
- Mention the exact file path.
- Explain the important functions clearly.
- Base your explanation only on the provided file.

File:
{file_path}

Actual File Content:
{content}

User Question:
{question}

Answer:
"""

        return llm_service.generate(
            answer_prompt
        )

    async def _run_find_references(
        self,
        question: str,
    ) -> str:
        symbol = self._extract_symbol(
            question
        )

        if not symbol:
            return (
                "Please specify the function, class, "
                "variable, or symbol you want to find "
                "references for."
            )

        references = find_references_tool(
            symbol=symbol,
            limit=20,
        )

        if not references:
            return (
                f"No references to "
                f"`{symbol}` were found."
            )

        reference_parts = []

        for index, reference in enumerate(
            references,
            start=1,
        ):
            reference_parts.append(
                f"""--- Reference {index} ---
File: {reference["path"]}
Chunk: {reference["chunk_index"]}
Similarity: {reference["score"]:.4f}

{reference["content"]}
"""
            )

        context = "\n".join(
            reference_parts
        )

        prompt = f"""
You are DevNexa AI, an AI software engineering agent.

The user wants to find references to a repository symbol.

Use only the retrieved repository code below.

Rules:
- Do not invent references.
- Clearly identify the files where the symbol appears.
- Explain whether the symbol appears to be defined,
  imported, called, or otherwise used when the
  retrieved code makes that clear.
- Mention exact file paths.
- If the retrieved context is insufficient to determine
  the exact usage, say so.

Symbol:
{symbol}

Retrieved References:
{context}

User Question:
{question}

Answer:
"""

        return llm_service.generate(
            prompt
        )

    @staticmethod
    def _extract_filename(
        question: str,
    ) -> str | None:
        words = (
            question
            .replace('"', " ")
            .replace("'", " ")
            .split()
        )

        supported_extensions = (
            ".py",
            ".js",
            ".jsx",
            ".ts",
            ".tsx",
            ".json",
            ".css",
            ".scss",
            ".html",
            ".md",
            ".yaml",
            ".yml",
            ".toml",
            ".txt",
        )

        for word in words:
            cleaned_word = word.strip(
                ".,!?():;[]{}"
            )

            if cleaned_word.lower().endswith(
                supported_extensions
            ):
                return cleaned_word

        return None

    @staticmethod
    def _extract_symbol(
        question: str,
    ) -> str | None:
        words = (
            question
            .replace("`", " ")
            .replace('"', " ")
            .replace("'", " ")
            .replace("(", " ")
            .replace(")", " ")
            .split()
        )

        reference_keywords = {
            "where",
            "is",
            "are",
            "used",
            "use",
            "references",
            "reference",
            "called",
            "call",
            "imported",
            "import",
            "find",
            "to",
            "the",
            "for",
            "this",
            "function",
            "class",
            "variable",
            "symbol",
        }

        candidates = []

        for word in words:
            cleaned_word = word.strip(
                ".,!?():;[]{}"
            )

            if not cleaned_word:
                continue

            if cleaned_word.lower() in reference_keywords:
                continue

            candidates.append(
                cleaned_word
            )

        if not candidates:
            return None

        return candidates[-1]

    @staticmethod
    def _is_complete_file_request(
        question: str,
    ) -> bool:
        question_lower = question.lower()

        complete_keywords = (
            "complete",
            "entire",
            "full",
            "whole",
        )

        file_keywords = (
            "file",
            "code",
            "contents",
            "content",
        )

        has_complete_keyword = any(
            keyword in question_lower
            for keyword in complete_keywords
        )

        has_file_keyword = any(
            keyword in question_lower
            for keyword in file_keywords
        )

        return (
            has_complete_keyword
            and has_file_keyword
        )