import collections
import dataclasses
import enum
import itertools
import math
import pathlib

@enum.unique
class Pulse(enum.IntEnum):
    Low = 0
    High = 1

@dataclasses.dataclass(slots=True)
class BaseModule:
    name: str
    targets: tuple = dataclasses.field(default_factory=tuple)

    def iter_pulses(self, pulse: Pulse):
        yield from ((self.name, pulse, target) for target in self.targets)

    def send(self, source, pulse: Pulse):
        ...

    def store_sources(self, sources):
        ...

@dataclasses.dataclass(slots=True)
class FlipFlopModule(BaseModule):
    state: bool = False

    def send(self, _: BaseModule, pulse: Pulse):
        if pulse == pulse.High:
            return

        self.state = not self.state
        yield from self.iter_pulses(Pulse(self.state))

@dataclasses.dataclass(slots=True)
class ConjunctionModule(BaseModule):
    _sources: dict[str, Pulse] = dataclasses.field(default_factory=dict)

    def send(self, source: str, pulse: Pulse):
        self._sources[source] = pulse

        out_pulse = Pulse(not all(self._sources.values()))
        yield from self.iter_pulses(out_pulse)

@dataclasses.dataclass(slots=True)
class Computer:
    puzzle_file: pathlib.Path
    modules: dict[str, BaseModule] = dataclasses.field(
        default_factory=dict, init=False
    )
    _initial_targets: tuple[BaseModule, ...] = dataclasses.field(
        default_factory=tuple, init=False
    )

    def push_button(self) -> tuple[tuple[str, Pulse, str], ...]:
        pulses = [("button", Pulse.Low, "broadcaster")]
        queue = collections.deque(
            ("broadcaster", Pulse.Low, target)
            for target in self._initial_targets
        )

        while queue:
            sent = queue.popleft()
            pulses.append(sent)

            source, pulse, target = sent
            if target not in self.modules:
                continue
            queue += [*self.modules[target].send(source, pulse)]

        return tuple(pulses)

    def __post_init__(self):
        inp = puzzle_file.read_text().strip()
        modules = tuple(map(parse_line, inp.splitlines()))
        conj_modules = {
            source: []
            for module_type, source, _ in modules
            if module_type is ConjunctionModule
        }

        for module_type, source, targets in modules:
            for target in targets:
                if target in conj_modules:
                    conj_modules[target].append(source)

            if module_type is None:
                self._initial_targets = targets
                continue
            self.modules[source] = module_type(name=source, targets=targets)

        for conj_module, sources in conj_modules.items():
            self.modules[conj_module] = (
                dataclasses.replace(
                    self.modules[conj_module], 
                    _sources={source: Pulse.Low for source in sources}
                )
            )

def parse_line(line: str) -> tuple[BaseModule | None, str, tuple[str, ...]]:
    raw_source, _, *targets = line.replace(",", "").split()
    targets = tuple(targets)
    if raw_source == "broadcaster":
        return None, raw_source, targets

    source = raw_source[1:]
    module_type = {"%": FlipFlopModule, "&": ConjunctionModule}[raw_source[0]]
    return module_type, source, targets

def p1(puzzle_file):
    computer = Computer(puzzle_file)

    return math.prod(
        collections.Counter(
            pulse
            for _ in range(1000)
            for _, pulse, _ in computer.push_button()
        ).values()
    )

def p2(puzzle_file):
    computer = Computer(puzzle_file)

    rx_sources = {
        source 
        for source, module in computer.modules.items()
        if "rx" in module.targets
    }

    rx_penultimate_sources = {
        source 
        for source, module in computer.modules.items()
        if rx_sources & set(module.targets)
    }

    todo = {source: None for source in rx_penultimate_sources}
    for i in itertools.count(1):
        for source, pulse, _ in computer.push_button():
            if (source in todo) and pulse == Pulse.High:
                todo[source] = i

        if all(todo.values()):
            break

    return math.lcm(*todo.values())

puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
#puzzle_file = puzzle_file.with_stem("test_puzzle")

print(p1(puzzle_file))
print(p2(puzzle_file))
