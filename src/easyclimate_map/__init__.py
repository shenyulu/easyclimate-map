from .version import __version__, show_versions

from .map.map_zh_CN import *
from .map.map_tibetan_plateau import *
from .core.tool import *

from rich import print

print(
    "[bold yellow]<easyclimate-map notice>[/bold yellow]: "
    "Maps are provided [bold]as-is[/bold]. "
    "Users assume all risk. "
    "No liability. "
    "No political or territorial claims."
)
