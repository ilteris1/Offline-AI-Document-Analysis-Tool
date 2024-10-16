from PyInstaller.utils.hooks import copy_metadata, collect_data_files
import spacy.cli

# Specify additional data files to include with the package
datas = collect_data_files('en_core_web_lg')

# Ensure that the en_core_web_lg model is downloaded during packaging
spacy.cli.download('en_core_web_lg')