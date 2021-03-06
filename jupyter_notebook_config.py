# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

from jupyter_core.paths import jupyter_data_dir
import subprocess
import os
import errno
import stat

c = get_config()
c.NotebookApp.ip = '*'
c.NotebookApp.port = 8888
c.NotebookApp.open_browser = False
c.NotebookApp.default_url='/lab'

c.InteractiveShellApp.extensions = [
    'jupyternotify'
]

c.GitHubConfig.access_token = 'b58a6210c6f9ac02bf5391915ec84c47a60cd8bc'

# Generate a self-signed certificate
if 'GEN_CERT' in os.environ:
    dir_name = jupyter_data_dir()
    pem_file = os.path.join(dir_name, 'notebook.pem')
    try:
        os.makedirs(dir_name)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(dir_name):
            pass
        else:
            raise
    # Generate a certificate if one doesn't exist on disk
    subprocess.check_call(['openssl', 'req', '-new',
                           '-newkey', 'rsa:2048',
                           '-days', '365',
                           '-nodes', '-x509',
                           '-subj', '/C=XX/ST=XX/L=XX/O=generated/CN=generated',
                           '-keyout', pem_file,
                           '-out', pem_file])
    # Restrict access to the file
    os.chmod(pem_file, stat.S_IRUSR | stat.S_IWUSR)
    c.NotebookApp.certfile = pem_file

# 預測在在notebook中顯示matplot圖片
c.IPKernelApp.matplotlib = 'inline'
c.InlineBackend.figure_formats = {'svg', 'png', 'retina'}

c.JupyterLabIFrame.iframes = ['https://mlc.app', 'https://406.csie.nuu.edu.tw', 'https://iothome.csie.nuu.edu.tw']
c.JupyterLabIFrame.welcome = 'https://ai.csie.nuu.edu.tw/hub/home'
