from django import template
import os

register = template.Library()

@register.filter
def file_icon(file_url):
    # Get the file extension (lowercase for consistency)
    extension = os.path.splitext(file_url)[1].lower()
    
    # Map extensions to Bootstrap Icons classes
    icon_map = {
        '.pdf': 'bi-file-earmark-pdf',
        '.doc': 'bi-file-earmark-word',
        '.docx': 'bi-file-earmark-word',
        '.txt': 'bi-file-earmark-text',
        '.jpg': 'bi-file-earmark-image',
        '.jpeg': 'bi-file-earmark-image',
        '.png': 'bi-file-earmark-image',
        '.xls': 'bi-file-earmark-excel',
        '.xlsx': 'bi-file-earmark-excel',
        '.ppt': 'bi-file-earmark-slides',
        '.pptx': 'bi-file-earmark-slides',
        '.zip': 'bi-file-earmark-zip',
        # Fallback for unknown types
        '': 'bi-file-earmark',
    }
    
    # Return the icon class (default to generic file icon if extension not found)
    return icon_map.get(extension, 'bi-file-earmark')