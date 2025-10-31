"""
ConvoSync - AI Conversation Data Processing Toolkit
对话数据处理工具集

A professional toolkit for cleaning, transforming, and managing AI conversation data.
用于清理、转换和管理 AI 对话数据的专业工具集。
"""

__title__ = "ConvoSync"
__description__ = "AI Conversation Data Processing Toolkit"
__version__ = "1.0.0"
__author__ = "Cagedbird"
__license__ = "MIT"

from .cleaners import JSONCleaner
from .converters import MarkdownConverter

__all__ = ["JSONCleaner", "MarkdownConverter"]
