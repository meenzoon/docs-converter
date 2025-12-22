"""
Markdown reader module for reading and parsing markdown files.
"""

from pathlib import Path
from typing import Optional, Dict, List, Any
import re


class MarkdownReader:
    """
    A class for reading and parsing markdown files.
    
    This class provides methods to read markdown files from disk,
    parse their content, and extract structured information.
    """
    
    def __init__(self, file_path: Optional[str] = None):
        """
        Initialize the MarkdownReader.
        
        Args:
            file_path: Optional path to a markdown file to read immediately.
        """
        self.file_path: Optional[Path] = None
        self.content: Optional[str] = None
        self.parsed_content: Optional[Dict[str, Any]] = None
        
        if file_path:
            self.read(file_path)
    
    def read(self, file_path: str) -> str:
        """
        Read a markdown file from disk.
        
        Args:
            file_path: Path to the markdown file.
            
        Returns:
            The content of the file as a string.
            
        Raises:
            FileNotFoundError: If the file doesn't exist.
            IOError: If there's an error reading the file.
        """
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        if not path.is_file():
            raise ValueError(f"Path is not a file: {file_path}")
        
        self.file_path = path
        self.content = path.read_text(encoding='utf-8')
        self.parsed_content = None  # Reset parsed content when reading new file
        
        return self.content
    
    def read_string(self, content: str) -> str:
        """
        Read markdown content from a string.
        
        Args:
            content: Markdown content as a string.
            
        Returns:
            The content string.
        """
        self.content = content
        self.file_path = None
        self.parsed_content = None
        
        return self.content
    
    def get_content(self) -> Optional[str]:
        """
        Get the raw markdown content.
        
        Returns:
            The raw markdown content, or None if no content has been loaded.
        """
        return self.content
    
    def parse(self) -> Dict[str, Any]:
        """
        Parse the markdown content into structured data.
        
        Returns:
            A dictionary containing:
            - 'title': The first H1 heading, if any
            - 'headings': List of all headings with their levels
            - 'paragraphs': List of paragraphs
            - 'code_blocks': List of code blocks
            - 'links': List of links found in the document
            - 'images': List of images found in the document
            - 'raw': The raw markdown content
        """
        if not self.content:
            raise ValueError("No content to parse. Call read() or read_string() first.")
        
        if self.parsed_content:
            return self.parsed_content
        
        parsed = {
            'title': self._extract_title(),
            'headings': self._extract_headings(),
            'paragraphs': self._extract_paragraphs(),
            'code_blocks': self._extract_code_blocks(),
            'links': self._extract_links(),
            'images': self._extract_images(),
            'raw': self.content
        }
        
        self.parsed_content = parsed
        return parsed
    
    def _extract_title(self) -> Optional[str]:
        """Extract the first H1 heading as the title."""
        if not self.content:
            return None
        
        lines = self.content.split('\n')
        for line in lines:
            # Check for # Title format
            match = re.match(r'^#\s+(.+)$', line.strip())
            if match:
                return match.group(1).strip()
        
        return None
    
    def _extract_headings(self) -> List[Dict[str, Any]]:
        """Extract all headings from the markdown."""
        if not self.content:
            return []
        
        headings = []
        lines = self.content.split('\n')
        
        for i, line in enumerate(lines):
            # Check for # Heading format
            match = re.match(r'^(#{1,6})\s+(.+)$', line.strip())
            if match:
                level = len(match.group(1))
                text = match.group(2).strip()
                headings.append({
                    'level': level,
                    'text': text,
                    'line_number': i + 1
                })
        
        return headings
    
    def _extract_paragraphs(self) -> List[str]:
        """Extract paragraphs from the markdown."""
        if not self.content:
            return []
        
        # Split by double newlines (paragraph breaks)
        paragraphs = []
        current_paragraph = []
        
        lines = self.content.split('\n')
        for line in lines:
            stripped = line.strip()
            
            # Skip empty lines, headings, code blocks, lists
            if not stripped:
                if current_paragraph:
                    paragraphs.append(' '.join(current_paragraph))
                    current_paragraph = []
                continue
            
            if stripped.startswith('#'):
                continue
            
            if stripped.startswith('```'):
                continue
            
            if re.match(r'^[-*+]\s+', stripped):
                continue
            
            if re.match(r'^\d+\.\s+', stripped):
                continue
            
            current_paragraph.append(stripped)
        
        if current_paragraph:
            paragraphs.append(' '.join(current_paragraph))
        
        return [p for p in paragraphs if p]
    
    def _extract_code_blocks(self) -> List[Dict[str, Any]]:
        """Extract code blocks from the markdown."""
        if not self.content:
            return []
        
        code_blocks = []
        pattern = r'```(\w+)?\n(.*?)```'
        
        matches = re.finditer(pattern, self.content, re.DOTALL)
        for match in matches:
            language = match.group(1) if match.group(1) else None
            code = match.group(2).strip()
            code_blocks.append({
                'language': language,
                'code': code
            })
        
        return code_blocks
    
    def _extract_links(self) -> List[Dict[str, Any]]:
        """Extract links from the markdown."""
        if not self.content:
            return []
        
        links = []
        
        # Inline links: [text](url)
        pattern = r'\[([^\]]+)\]\(([^\)]+)\)'
        matches = re.finditer(pattern, self.content)
        for match in matches:
            links.append({
                'text': match.group(1),
                'url': match.group(2)
            })
        
        # Reference links: [text][ref] (we'll extract the reference definitions separately)
        ref_pattern = r'^\[([^\]]+)\]:\s+(.+)$'
        lines = self.content.split('\n')
        for line in lines:
            ref_match = re.match(ref_pattern, line.strip())
            if ref_match:
                links.append({
                    'text': ref_match.group(1),
                    'url': ref_match.group(2).strip()
                })
        
        return links
    
    def _extract_images(self) -> List[Dict[str, Any]]:
        """Extract images from the markdown."""
        if not self.content:
            return []
        
        images = []
        pattern = r'!\[([^\]]*)\]\(([^\)]+)\)'
        
        matches = re.finditer(pattern, self.content)
        for match in matches:
            images.append({
                'alt_text': match.group(1),
                'url': match.group(2)
            })
        
        return images
    
    def get_headings_by_level(self, level: int) -> List[str]:
        """
        Get all headings of a specific level.
        
        Args:
            level: The heading level (1-6).
            
        Returns:
            List of heading texts at the specified level.
        """
        parsed = self.parse()
        return [h['text'] for h in parsed['headings'] if h['level'] == level]
    
    def get_sections(self) -> List[Dict[str, Any]]:
        """
        Get the document organized by sections (based on headings).
        
        Returns:
            List of sections, each containing heading and content.
        """
        if not self.content:
            return []
        
        sections = []
        lines = self.content.split('\n')
        current_section = None
        current_content = []
        
        for line in lines:
            # Check if line is a heading
            match = re.match(r'^(#{1,6})\s+(.+)$', line.strip())
            if match:
                # Save previous section if exists
                if current_section:
                    current_section['content'] = '\n'.join(current_content).strip()
                    sections.append(current_section)
                
                # Start new section
                level = len(match.group(1))
                text = match.group(2).strip()
                current_section = {
                    'level': level,
                    'heading': text,
                    'content': ''
                }
                current_content = []
            else:
                if current_section:
                    current_content.append(line)
        
        # Add last section
        if current_section:
            current_section['content'] = '\n'.join(current_content).strip()
            sections.append(current_section)
        
        return sections

