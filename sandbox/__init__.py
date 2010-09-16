class SandboxError(Exception):
    pass

class Protection:
    def enable(self, sandbox):
        pass

    def disable(self, sandbox):
        pass

# CPython restricted mode is only available in Python 2.x
from sys import version_info
HAVE_CPYTHON_RESTRICTED = (version_info < (3, 0))

# Use the C module (_sandbox)
try:
    from _sandbox import set_error_class, version as _sandbox_version
except ImportError:
    if not HAVE_CPYTHON_RESTRICTED:
        raise SandboxError("_sandbox is required on Python 3.x")
    USE_CSANDBOX = False
else:
    USE_CSANDBOX = True
    set_error_class(SandboxError)
    del set_error_class
    if _sandbox_version != 1:
        raise SandboxError("Unknown _sandbox version (%s)" % _sandbox_version)

from .config import SandboxConfig
from .sandbox_class import Sandbox

from .builtins import CleanupBuiltins
Sandbox.PROTECTIONS.append(CleanupBuiltins)

from .attributes import HideAttributes
Sandbox.PROTECTIONS.append(HideAttributes)

from .stdio import ProtectStdio
Sandbox.PROTECTIONS.append(ProtectStdio)

if USE_CSANDBOX:
    from .code import DisableCode
    Sandbox.PROTECTIONS.append(DisableCode)

from .timeout import Timeout
