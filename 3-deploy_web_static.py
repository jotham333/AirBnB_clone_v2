from datetime import datetime
from fabric.api import env, put, run, local
import os

env.hosts = ['34.224.3.182', '54.237.225.149']

def do_pack():
    """
    Creates a .tgz archive from the contents of the web_static folder
    """
    try:
        now = datetime.now()
        archive_name = f"web_static_{now.strftime('%Y%m%d%H%M%S')}.tgz"
        local("mkdir -p versions")
        local(f"tar -cvzf versions/{archive_name} web_static")
        return f"versions/{archive_name}"
    except Exception:
        return None

def do_deploy(archive_path):
    """
    Distributes an archive to the web servers
    """
    if not os.path.exists(archive_path):
        return False

    try:
        archive_filename = os.path.basename(archive_path)
        archive_name = os.path.splitext(archive_filename)[0]
        releases_path = "/data/web_static/releases/"
        tmp_path = "/tmp/"

        put(archive_path, tmp_path)
        run(f"mkdir -p {releases_path}{archive_name}")
        run(f"tar -xzf {tmp_path}{archive_filename} -C {releases_path}{archive_name}")
        run(f"rm {tmp_path}{archive_filename}")
        run(f"mv {releases_path}{archive_name}/web_static/* {releases_path}{archive_name}/")
        run(f"rm -rf {releases_path}{archive_name}/web_static")
        run("rm -rf /data/web_static/current")
        run(f"ln -s {releases_path}{archive_name}/ /data/web_static/current")

        return True
    except Exception:
        return False

def deploy():
    """
    Creates and distributes an archive to the web servers
    """
    archive_path = do_pack()
    if not archive_path:
        return False
    return do_deploy(archive_path)
    # Return False if no archive has been created
    if not archive_path:
        return False

    # Call the do_deploy(archive_path) function using the new path of the new archive
    return do_deploy(archive_path)
