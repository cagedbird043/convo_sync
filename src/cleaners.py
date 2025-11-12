"""
JSON Cleaning Module - 数据清理模块

专门用于清理 Google AI Studio 导出的对话 JSON，
移除思考过程和代码块以节省 tokens，同时保留模型配置和文件引用。
"""

import json
import re


class JSONCleaner:
    """Clean and optimize Google AI Studio exported JSON conversations.

    This class provides intelligent cleaning of conversation data exported from
    Google AI Studio, reducing token usage while preserving essential content.

    The cleaner performs the following operations:
        - Preserves model configuration (runSettings, systemInstruction)
        - Removes AI thinking process chunks (optional, default: True)
        - Removes code blocks using heuristic detection (optional, default: True)
        - Maintains file references (driveDocument) for uploaded files
        - Provides statistics on cleaned data

    Attributes:
        input_file (str): Path to the input JSON file.
        output_file (str): Path to the output cleaned JSON file.
        remove_thinking (bool): Whether to remove thinking process chunks.
        remove_code_blocks (bool): Whether to remove detected code blocks.
        data (dict): The loaded and processed JSON data.

    Example:
        >>> cleaner = JSONCleaner("conversation.json", remove_thinking=True)
        >>> cleaner.clean()
        >>> stats = cleaner.get_stats()
        >>> print(f"Cleaned {stats['total']} chunks")

    Note:
        The cleaned JSON maintains compatibility with Google AI Studio and can
        be re-imported after processing.
    """

    def __init__(
        self,
        input_file: str,
        output_file: str | None = None,
        remove_thinking: bool = True,
        remove_code_blocks: bool = True,
    ) -> None:
        """Initialize the JSON cleaner with configuration.

        Args:
            input_file: Path to the input JSON file from Google AI Studio.
            output_file: Path for the cleaned JSON output. If None, automatically
                generates filename by appending '.cleaned' before extension.
            remove_thinking: If True, removes chunks marked as thinking process
                (isThought: true) and parts with thought: true flag. Default is True.
            remove_code_blocks: If True, applies heuristic algorithm to detect and
                remove code blocks while preserving descriptive text. Default is True.

        Raises:
            FileNotFoundError: If input_file does not exist.
            json.JSONDecodeError: If input_file is not valid JSON.
        """
        self.input_file = input_file
        self.output_file = output_file or input_file.replace(".json", ".cleaned.json")
        self.remove_thinking = remove_thinking
        self.remove_code_blocks = remove_code_blocks

    def clean(self) -> dict:
        """Execute the cleaning process and save results.

        This method orchestrates the entire cleaning workflow:
            1. Loads the input JSON file
            2. Processes and filters conversation data
            3. Removes thinking process chunks (if enabled)
            4. Removes code blocks using heuristic detection (if enabled)
            5. Preserves model configuration and file references
            6. Saves the cleaned data to output file

        Returns:
            dict: The cleaned conversation data dictionary with the same structure
                as Google AI Studio format, ready for re-import.

        Raises:
            FileNotFoundError: If the input file does not exist.
            json.JSONDecodeError: If the input file contains invalid JSON.
            IOError: If unable to write to the output file.

        Example:
            >>> cleaner = JSONCleaner("input.json", remove_thinking=True)
            >>> result = cleaner.clean()
            >>> print(f"Cleaned file saved with {len(result['chunkedPrompt']['chunks'])} chunks")
        """
        data = self._load_json_file()
        cleaned_data = self._process_google_ai_studio_format(data)
        self._save_json_file(cleaned_data)
        return cleaned_data

    def _load_json_file(self) -> dict:
        """Load and parse JSON file."""
        try:
            with open(self.input_file, encoding="utf-8") as f:
                data: dict = json.load(f)
                return data
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalisd JSON file: {e}") from e
        except FileNotFoundError as e:
            raise FileNotFoundError(f"Input file not found: {self.input_file}") from e

    def _save_json_file(self, data):
        """Save cleaned data to JSON file."""
        with open(self.output_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def _process_google_ai_studio_format(self, data: dict) -> dict:
        """Process Google AI Studio exported JSON format.

        Structure:
        {
          "runSettings": { ... },
          "systemInstruction": { ... },
          "chunkedPrompt": {
            "chunks": [ ... ]
          }
        }
        """
        cleaned_data: dict = {}

        # 1. 保留 runSettings
        if "runSettings" in data:
            cleaned_data["runSettings"] = data["runSettings"]

        # 2. 保留 systemInstruction
        if "systemInstruction" in data:
            cleaned_data["systemInstruction"] = data["systemInstruction"]

        # 3. 处理 chunkedPrompt
        if "chunkedPrompt" in data:
            chunked_prompt = data["chunkedPrompt"]
            chunks = chunked_prompt.get("chunks", [])
            cleaned_chunks = self._process_chunks(chunks)
            cleaned_data["chunkedPrompt"] = {"chunks": cleaned_chunks}

        return cleaned_data

    def _process_chunks(self, chunks):
        """Process and clean chunks array."""
        cleaned_chunks = []

        for chunk in chunks:
            # 保留文件引用（driveDocument）
            if "driveDocument" in chunk:
                cleaned_chunks.append(chunk)
                continue

            # 跳过思考过程
            if self.remove_thinking and chunk.get("isThought"):
                continue

            # 处理普通消息
            cleaned_chunk = self._process_single_chunk(chunk)
            if cleaned_chunk:
                cleaned_chunks.append(cleaned_chunk)

        return cleaned_chunks

    def _process_single_chunk(self, chunk):
        """Process a single chunk."""
        cleaned_chunk = {}

        # 复制基本字段
        for key in ["role", "tokenCount"]:
            if key in chunk:
                cleaned_chunk[key] = chunk[key]

        # 处理文本内容
        if "text" in chunk:
            text = chunk["text"]
            if self.remove_code_blocks:
                text = self._remove_code_blocks(text)
            cleaned_chunk["text"] = text

        # 处理 parts 数组
        elif "parts" in chunk:
            cleaned_parts = self._process_parts(chunk["parts"])
            if cleaned_parts:
                cleaned_chunk["parts"] = cleaned_parts

        # 如果没有任何内容，返回 None
        if "text" not in cleaned_chunk and "parts" not in cleaned_chunk:
            return None

        return cleaned_chunk

    def _process_parts(self, parts):
        """Process parts array, filtering out thinking parts."""
        cleaned_parts = []

        for part in parts:
            # 跳过思考片段
            if self.remove_thinking and part.get("thought"):
                continue

            # 处理普通文本片段
            if "text" in part:
                text = part["text"]
                if self.remove_code_blocks:
                    text = self._remove_code_blocks(text)
                cleaned_parts.append({"text": text})

        return cleaned_parts

    def _remove_code_blocks(self, text):
        """Remove code blocks from text while preserving structure.

        智能检测：只移除包含代码的块，保留纯文本/总结。

        识别代码块的模式：
        - 三个或更多反引号开始
        - 可选的语言标识符
        - 代码内容
        - 相同数量的反引号结束
        """
        # 改进的正则：不强制要求换行符，支持更多格式
        pattern = r"(`{3,})([a-zA-Z]*)\s*(.*?)\s*\1"

        def replace_code_block(match):
            """根据内容决定是否移除代码块"""
            language = match.group(2)  # 语言标识符
            content = match.group(3)  # 块内容

            # 如果明确指定了编程语言，直接移除
            if language and language.lower() in {
                "python",
                "javascript",
                "typescript",
                "java",
                "cpp",
                "c",
                "rust",
                "go",
                "ruby",
                "php",
                "shell",
                "bash",
                "sql",
                "html",
                "css",
                "json",
                "yaml",
                "xml",
                "markdown",
                "code",
            }:
                return ""

            # 智能检测内容是否为代码
            if self._is_code_content(content):
                return ""

            # 保留纯文本/总结（去掉围栏，保留内容）
            return content.strip()

        return re.sub(pattern, replace_code_block, text, flags=re.DOTALL)

    def _is_code_content(self, content):
        """检测内容是否为代码.

        通过代码特征判断：
        - 包含编程关键字
        - 包含特殊符号（{}, [], (), ;, =>, etc.）
        - 行以缩进开始
        - 包含函数调用模式
        """
        min_content_length = 10
        if not content or len(content.strip()) < min_content_length:
            return False

        content_lower = content.lower()

        # 代码关键字（常见编程语言）
        code_keywords = {
            "def ",
            "class ",
            "import ",
            "from ",
            "return ",
            "function ",
            "const ",
            "let ",
            "var ",
            "if ",
            "else ",
            "for ",
            "while ",
            "async ",
            "await ",
            "try ",
            "catch ",
            "throw ",
            "new ",
            "this.",
            "self.",
            "public ",
            "private ",
            "protected ",
            "static ",
            "void ",
            "int ",
            "string ",
            "bool ",
        }

        # 检查是否包含代码关键字
        if any(keyword in content_lower for keyword in code_keywords):
            return True

        # 检查是否包含大量代码特征符号
        code_symbols = ["{", "}", "()", "[]", "=>", "->", "==", "!=", "<=", ">="]
        symbol_count = sum(content.count(symbol) for symbol in code_symbols)
        lines = content.split("\n")

        # 如果符号密度高（平均每行超过2个符号），可能是代码
        symbol_per_line_threshold = 2
        if len(lines) > 0 and symbol_count / len(lines) > symbol_per_line_threshold:
            return True

        # 检查缩进模式（代码通常有规律的缩进）
        min_lines_for_indent_check = 3
        indent_ratio_threshold = 0.5
        indented_lines = sum(1 for line in lines if line.startswith(("    ", "\t")))
        if len(lines) > min_lines_for_indent_check and indented_lines / len(lines) > indent_ratio_threshold:
            return True

        # 检查是否包含函数调用模式 function_name(...)
        # 但排除常见的中文括号用法
        return bool(re.search(r"\w+\([^)]*\)", content) and not re.search(r"[\u4e00-\u9fa5]+\([^)]*\)", content))

    def get_stats(self) -> dict[str, int | bool]:
        """Calculate statistics from the cleaned conversation data.

        Analyzes the output file to provide insights about the cleaned data,
        including message counts, file references, and applied cleaning options.

        Returns:
            dict: A dictionary containing the following statistics:
                - total (int): Total number of conversation chunks
                - users (int): Number of user messages
                - models (int): Number of model (assistant) messages
                - files (int): Number of file references (driveDocument)
                - thinking_removed (bool): Whether thinking process was removed
                - code_blocks_removed (bool): Whether code blocks were removed

        Raises:
            FileNotFoundError: If the output file hasn't been created yet.
            json.JSONDecodeError: If the output file contains invalid JSON.

        Example:
            >>> cleaner = JSONCleaner("input.json")
            >>> cleaner.clean()
            >>> stats = cleaner.get_stats()
            >>> print(f"Total: {stats['total']}, Users: {stats['users']}")
            Total: 150, Users: 76

        Note:
            This method reads from the output file, so clean() must be called first.
        """
        with open(self.output_file, encoding="utf-8") as f:
            data = json.load(f)

        chunks = data.get("chunkedPrompt", {}).get("chunks", [])
        user_count = sum(1 for c in chunks if c.get("role") == "user")
        model_count = sum(1 for c in chunks if c.get("role") == "model")
        file_count = sum(1 for c in chunks if "driveDocument" in c)

        return {
            "total": len(chunks),
            "users": user_count,
            "models": model_count,
            "files": file_count,
            "thinking_removed": self.remove_thinking,
            "code_blocks_removed": self.remove_code_blocks,
        }
