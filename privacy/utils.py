"""
Utilidades para privacy.
"""
import re


def markdown_to_html(text):
    """
    Convierte Markdown básico a HTML.
    Soporta: headers, bold, italic, listas, párrafos, links.
    """
    if not text:
        return ""
    
    lines = text.split('\n')
    result = []
    in_ul = False
    in_ol = False
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Headers (# ## ### etc)
        if re.match(r'^#{1,6}\s+', line):
            # Cerrar listas si estaban abiertas
            if in_ul:
                result.append('</ul>')
                in_ul = False
            if in_ol:
                result.append('</ol>')
                in_ol = False
            
            level = len(re.match(r'^(#{1,6})', line).group(1))
            content = re.sub(r'^#{1,6}\s+', '', line)
            result.append(f'<h{level}>{content}</h{level}>')
        
        # Listas no ordenadas (- item)
        elif re.match(r'^-\s+', line):
            if not in_ul:
                if in_ol:
                    result.append('</ol>')
                    in_ol = False
                result.append('<ul>')
                in_ul = True
            item = re.sub(r'^-\s+', '', line)
            result.append(f'<li>{item}</li>')
        
        # Listas ordenadas (1. item)
        elif re.match(r'^\d+\.\s+', line):
            if not in_ol:
                if in_ul:
                    result.append('</ul>')
                    in_ul = False
                result.append('<ol>')
                in_ol = True
            item = re.sub(r'^\d+\.\s+', '', line)
            result.append(f'<li>{item}</li>')
        
        # Línea vacía
        elif not line.strip():
            if in_ul:
                result.append('</ul>')
                in_ul = False
            if in_ol:
                result.append('</ol>')
                in_ol = False
            result.append('')
        
        # Línea normal (párrafo)
        else:
            if in_ul:
                result.append('</ul>')
                in_ul = False
            if in_ol:
                result.append('</ol>')
                in_ol = False
            result.append(f'<p>{line}</p>')
        
        i += 1
    
    # Cerrar listas si quedaron abiertas
    if in_ul:
        result.append('</ul>')
    if in_ol:
        result.append('</ol>')
    
    html = '\n'.join(result)
    
    # Bold (**text** o __text__)
    html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
    html = re.sub(r'__(.+?)__', r'<strong>\1</strong>', html)
    
    # Italic (*text* o _text_) - cuidado con no confundir con bold
    html = re.sub(r'(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)', r'<em>\1</em>', html)
    html = re.sub(r'(?<!_)_(?!_)(.+?)(?<!_)_(?!_)', r'<em>\1</em>', html)
    
    # Links [text](url)
    html = re.sub(r'\[([^\]]+)\]\(([^\)]+)\)', r'<a href="\2">\1</a>', html)
    
    return html
