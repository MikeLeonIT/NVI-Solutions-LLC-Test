import os
import shutil

import fitz


def convert_pdf(filename):
    doc = fitz.open(filename)
    result = []

    path_name = "tmp"
    if not os.path.exists(path_name):
        os.makedirs(path_name)
    else:
        for filename in os.listdir(path_name):
            file_path = os.path.join(path_name, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))

    for i, page in enumerate(doc):
        pix = page.get_pixmap()
        name = f"tmp/page_{i+1}.png"
        pix.save(name)
        result.append(name)

    return result
