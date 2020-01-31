import typing as t
from dataclasses import dataclass, field


@dataclass
class XMLTag:
    tag: str
    children: t.List['XMLTag'] = field(default_factory=list)
    attrs: t.List[t.Tuple[str, str]] = field(default_factory=list)
    value: t.Optional[str] = None
