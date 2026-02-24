import os
import re
import shutil
from pathlib import Path
import html2text

def html_to_md(html_path, md_path, base_dir, images_dir):
    with open(html_path, 'r', encoding='utf-8', errors='ignore') as f:
        html_content = f.read()

    images_dir.mkdir(parents=True, exist_ok=True)

    chm_name = Path(html_path).parent.relative_to(base_dir).parts[0]

    img_pattern = re.compile(r'<img[^>]+src=["\']([^"\']+)["\']', re.IGNORECASE)
    for match in img_pattern.finditer(html_content):
        img_src = match.group(1)
        if img_src.startswith(('http://', 'https://')):
            continue
        
        img_path = Path(html_path).parent / img_src
        if not img_path.exists():
            img_path = Path(img_src)
        
        if img_path.exists():
            img_name = img_path.name
            dest_img = images_dir / chm_name / img_name
            dest_img.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(img_path, dest_img)
            
            md_dir = md_path.parent
            rel_to_md = os.path.relpath(dest_img, md_dir)
            html_content = html_content.replace(img_src, rel_to_md.replace('\\', '/'))

    chm_link_pattern = re.compile(r'href=["\'](chm://|ms-its:[^"\']+)["\']', re.IGNORECASE)
    for match in chm_link_pattern.finditer(html_content):
        full_link = match.group(1)
        
        if full_link.startswith('ms-its:'):
            msits_match = re.match(r'ms-its:([^:]+\.chm)::(/.*)', full_link, re.IGNORECASE)
            if msits_match:
                chm_link = msits_match.group(2)
            else:
                continue
        else:
            chm_link = full_link[6:]
        
        if '#' in chm_link:
            anchor_part = '#' + chm_link.split('#')[1]
        else:
            anchor_part = ''
        
        chm_link = chm_link.split('#')[0]
        chm_link = chm_link.replace('\\', '/')
        
        if '.htm' in chm_link.lower():
            md_file = re.sub(r'\.html?$', '.md', chm_link, flags=re.IGNORECASE)
            new_link = f'[{md_file}]({md_file}{anchor_part})'
        else:
            new_link = f'[{chm_link}]({chm_link}{anchor_part})'
        
        html_content = html_content.replace(match.group(0), new_link)

    a_pattern = re.compile(r'<a[^>]+href=["\']([^"\']+)["\']', re.IGNORECASE)
    for match in a_pattern.finditer(html_content):
        href = match.group(1)
        if href.startswith(('http://', 'https://', 'mailto:', 'javascript:', 'chm://', 'ms-its:')):
            continue
        
        href = href.replace('\\', '/')
        
        anchor = ''
        if '#' in href:
            href, anchor = href.split('#', 1)
            anchor = '#' + anchor
        
        link_path = Path(html_path).parent / href
        if link_path.exists() and link_path.suffix.lower() in ['.htm', '.html']:
            rel_path = link_path.relative_to(Path(html_path).parent)
            md_file = str(rel_path.with_suffix('.md')) + anchor
            html_content = html_content.replace(match.group(1), md_file)

    id_pattern = re.compile(r'\sid=["\']([^"\']+)["\']')
    name_pattern = re.compile(r'\sname=["\']([^"\']+)["\']')
    
    for tag in re.finditer(r'<[^>]+>', html_content):
        tag_str = tag.group(0)
        id_match = id_pattern.search(tag_str)
        anchor_id = None
        if id_match:
            anchor_id = id_match.group(1)
        else:
            name_match = name_pattern.search(tag_str)
            if name_match:
                anchor_id = name_match.group(1)
        
        if anchor_id and '</a>' not in tag_str:
            html_content = html_content.replace(tag_str, f'{tag_str}<a id="{anchor_id}"></a>', 1)

    h = html2text.HTML2Text()
    h.ignore_links = False
    h.ignore_images = False
    h.ignore_emphasis = False
    h.body_width = 0
    
    md_content = h.handle(html_content)
    
    md_path.parent.mkdir(parents=True, exist_ok=True)
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(md_content)

def convert_folder(base_folder):
    base_path = Path(base_folder)
    html_dir = base_path / 'html'
    md_dir = base_path / 'md'
    images_dir = md_dir / 'images'
    
    if not html_dir.exists():
        print(f"html dir not found: {html_dir}")
        return
    
    for chm_folder in html_dir.iterdir():
        if not chm_folder.is_dir():
            continue
        
        print(f"Processing: {chm_folder.name}")
        
        for html_file in chm_folder.rglob('*.html'):
            rel_path = html_file.relative_to(html_dir)
            md_file = md_dir / rel_path.with_suffix('.md')
            
            html_to_md(html_file, md_file, html_dir, images_dir)
            print(f"  Converted: {rel_path}")
        
        for html_file in chm_folder.rglob('*.htm'):
            if html_file.suffix == '.html':
                continue
            rel_path = html_file.relative_to(html_dir)
            md_file = md_dir / rel_path.with_suffix('.md')
            
            html_to_md(html_file, md_file, html_dir, images_dir)
            print(f"  Converted: {rel_path}")
