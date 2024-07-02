'''
@Author: Amirhossein Hosseinpour <https://amirhp.com>
@Date Created: 2024/07/02 16:35:01
@Last modified by: amirhp-com <its@amirhp.com>
@Last modified time: 2024/07/02 18:02:01
'''

import os
import re
import datetime
import subprocess
import sys

author = "Amirhossein Hosseinpour <its@amirhp.com>"

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Ensure required libraries are installed
try:
    import polib
except ImportError:
    install("polib")
    import polib

def find_main_plugin_file(directory):
    plugin_files = [f for f in os.listdir(directory) if f.endswith('.php')]
    for file in plugin_files:
        with open(os.path.join(directory, file), 'r', encoding='utf-8') as f:
            content = f.read()
            if re.search(r'Plugin Name:', content):
                return os.path.join(directory, file)
    return None

def send_notification(title, message):
    script = f'display notification "{message}" with title "{title}" subtitle "Developed by AmirhpCom" sound name "Frog"'
    subprocess.run(["osascript", "-e", script])

def extract_plugin_data(file_path):
    plugin_data = {}
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        plugin_data['name'] = re.search(r'Plugin Name:\s*(.*)', content).group(1).strip()
        plugin_data['uri'] = re.search(r'Plugin URI:\s*(.*)', content).group(1).strip()
        plugin_data['description'] = re.search(r'Description:\s*(.*)', content).group(1).strip()
        plugin_data['author'] = re.search(r'Author:\s*(.*)', content).group(1).strip()
        plugin_data['author_uri'] = re.search(r'Author URI:\s*(.*)', content).group(1).strip()
        plugin_data['text_domain'] = re.search(r'Text Domain:\s*(.*)', content).group(1).strip()
    return plugin_data

def create_pot_file(directory, plugin_data):
    pot_file_path = os.path.join(directory, 'languages', f"{plugin_data['text_domain']}.pot")
    os.makedirs(os.path.dirname(pot_file_path), exist_ok=True)

    pot = polib.POFile()
    pot.metadata = {
        'Project-Id-Version': plugin_data['name'],
        'POT-Creation-Date': datetime.datetime.now().strftime('%Y-%m-%d %H:%M%z'),
        'PO-Revision-Date': datetime.datetime.now().strftime('%Y-%m-%d %H:%M%z'),
        'Last-Translator': author,
        'Language-Team': author,
        'MIME-Version': '1.0',
        'Content-Type': 'text/plain; charset=UTF-8',
        'Content-Transfer-Encoding': '8bit',
        'Plural-Forms': 'nplurals=INTEGER; plural=EXPRESSION;',
        'X-Generator': 'Poedit 3.4.2',
        'X-Poedit-Basepath': '..',
        'X-Poedit-Flags-xgettext': '--add-comments=translators:',
        'X-Poedit-WPHeader': os.path.basename(file_path),
        'X-Poedit-SourceCharset': 'UTF-8',
        'X-Poedit-KeywordsList': '__;_e;_n:1,2;_x:1,2c;_ex:1,2c;_nx:4c,1,2;esc_attr__;esc_attr_e;esc_attr_x:1,2c;esc_html__;esc_html_e;esc_html_x:1,2c;_n_noop:1,2;_nx_noop:3c,1,2;__ngettext_noop:1,2',
        'X-Poedit-SearchPath-0': '.',
        'X-Poedit-SearchPathExcluded-0': '*.js'
    }

    pot.append(polib.POEntry(
        comment="Plugin Name of the plugin/theme",
        msgid=plugin_data['name'],
        msgstr=plugin_data['name']
    ))
    pot.append(polib.POEntry(
        comment="Description of the plugin/theme",
        msgid=plugin_data['description'],
        msgstr=plugin_data['description']
    ))
    pot.append(polib.POEntry(
        comment="Plugin URI of the plugin/theme",
        msgid=plugin_data['uri'],
        msgstr=plugin_data['uri']
    ))
    pot.append(polib.POEntry(
        comment="Author of the plugin/theme",
        msgid=plugin_data['author'],
        msgstr=plugin_data['author']
    ))
    pot.append(polib.POEntry(
        comment="Author URI of the plugin/theme",
        msgid=plugin_data['author_uri'],
        msgstr=plugin_data['author_uri']
    ))
    pot.save(pot_file_path)
    print(f"Generated POT file: {pot_file_path}")

def create_fa_IR_translation(directory, plugin_data):
    pot_file_path = os.path.join(directory, 'languages', f"{plugin_data['text_domain']}.pot")
    fa_IR_dir = os.path.join(directory, 'languages')
    os.makedirs(fa_IR_dir, exist_ok=True)
    fa_IR_po_file_path = os.path.join(fa_IR_dir, f"{plugin_data['text_domain']}-fa_IR.po")

    pot = polib.pofile(pot_file_path)
    po = polib.POFile()

    po.metadata = pot.metadata
    po.metadata['Language'] = 'fa_IR'
    po.metadata['X-Poedit-Language'] = 'fa_IR'
    po.metadata['X-Poedit-Country'] = 'IR'

    for entry in pot:
        fa_entry = polib.POEntry(
            msgid=entry.msgid,
            msgstr=entry.msgstr
        )
        po.append(fa_entry)

    po.save(fa_IR_po_file_path)
    print(f"Generated fa_IR PO file: {fa_IR_po_file_path}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        directory = sys.argv[1]
        file_path = find_main_plugin_file(directory)
        if file_path:
            plugin_data = extract_plugin_data(file_path)
            create_pot_file(directory, plugin_data)
            create_fa_IR_translation(directory, plugin_data)
            send_notification("Translation Extraction", "POT file has been successfully created.")
        else:
            send_notification("Translation Extraction", "Main plugin file not found.")
            print("Main plugin file not found.")
    else:
        send_notification("Translation Extraction", "Please provide the directory path.")
        print("Please provide the directory path.")

