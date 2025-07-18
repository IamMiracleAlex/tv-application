import os

from .base import *

if os.environ.get("ENVIRONMENT") == "prod":
    from .prod import *

elif os.environ.get("ENVIRONMENT") == "local":
    from .local import *

else:
    raise NotImplementedError("Make sure there is an ENVIRONMENT variable")
