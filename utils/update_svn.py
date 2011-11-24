from bhp_netbook.classes import Svn
from models import Netbook


"""
from bhp_netbook.classes import Svn
svn = Svn()
svn.update_svn()
"""

def update_svn(**kwargs):
    svn = Svn()
    svn.update_svn()

if __name__ == "__main__":
    update_svn()
