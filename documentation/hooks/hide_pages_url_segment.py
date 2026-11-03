# Change the URL segment for pages in MkDocs to hide the "/pages" prefix, so
# that pages inside the "pages" directory are served directly at the root URL.
import os
from mkdocs.plugins import event_priority


@event_priority(-100)
def on_files(files, config):
    for file in files:
        if file.src_uri.startswith("pages/"):
            # Remove "pages/" prefix from the URL
            file.dest_uri = file.dest_uri.removeprefix("pages/")
            file.url = file.url.removeprefix("pages/")
            file.abs_dest_path = os.path.join(config.site_dir, file.dest_uri)
    return files