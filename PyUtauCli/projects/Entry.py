from PyUtauCli.common import convert_notenum

from .EntryBase import (
    BoolEntry,
    EntryBase,
    FloatEntry,
    IntEntry,
    ListEntry,
    StringEntry,
)


class NumberEntry(StringEntry):
    pass


class LengthEntry(IntEntry):
    _value = 480


class LyricEntry(StringEntry):
    pass


class NoteNumEntry(IntEntry):
    _value = 60

    def set_from_str(self, value: str):
        self.value = convert_notenum.toInt(value)
        self._set_update()
        self._hasValue = True

    def get_tone_name(self) -> str:
        return convert_notenum.toStr(self.value)


class TempoEntry(FloatEntry):
    _value = 120
    point = 2

    @property
    def hasValue(self) -> bool:
        return self._hasValue

    @hasValue.setter
    def hasValue(self, value: bool):
        self._hasValue = value


class PreEntry(FloatEntry):
    @property
    def hasValue(self) -> bool:
        return self._hasValue

    @hasValue.setter
    def hasValue(self, value: bool):
        self._hasValue = value


class AtPreEntry(FloatEntry):
    pass


class OveEntry(FloatEntry):
    @property
    def hasValue(self) -> bool:
        return self._hasValue

    @hasValue.setter
    def hasValue(self, value: bool):
        self._hasValue = value


class AtOveEntry(FloatEntry):
    pass


class StpEntry(FloatEntry):
    pass


class AtStpEntry(FloatEntry):
    pass


class AtFileNameEntry(StringEntry):
    pass


class AtAliasEntry(StringEntry):
    pass


class VelocityEntry(IntEntry):
    _value = 100

    @property
    def rate(self) -> float:
        return 2 ** ((100 - self._value) / 100)


class IntensityEntry(IntEntry):
    _value = 100


class ModulationEntry(IntEntry):
    _value = 100


class PitchesEntry(ListEntry):
    def _check_value(self, value) -> int:
        return int(value)


class PBStartEntry(FloatEntry):
    pass


class PBSEntry(EntryBase):
    _time: float = 0
    _height: float = 0
    _value: str

    @property
    def time(self) -> float:
        return self._time

    @property
    def height(self) -> float:
        return self._height

    @property
    def value(self) -> str:
        return self._value

    @time.setter
    def time(self, value: float):
        self._time = float(value)
        self._value = f'{self._time:.3f};{self._height:.3f}'
        self._set_update()
        self._hasValue = True

    @height.setter
    def height(self, value: float):
        self._height = float(value)
        self._value = f'{self._time:.3f};{self._height:.3f}'
        self._set_update()
        self._hasValue = True

    @value.setter
    def value(self, value: str):
        value = value.replace(',', ';')
        if ';' in value:
            values: list = value.split(';')
            self._time = float(values[0])
            self._height = float(values[1])
            self._value = value
            self._set_update()
            self._hasValue = True
        else:
            self._time = float(value)
            self._height = 0
            self._value = value
            self._set_update()
            self._hasValue = True

    def init(self, value: str):
        value = value.replace(',', ';')
        if ';' in value:
            values: list = value.split(';')
            self._time = float(values[0])
            self._height = float(values[1])
            self._value = value
            self._hasValue = True
        else:
            self._time = float(value)
            self._height = 0
            self._value = value
            self._hasValue = True

    def __str__(self) -> str:
        if self._height == 0:
            return f'{self._time:.3f}'
        return self._value


class PBYEntry(ListEntry):
    def _check_value(self, value):
        if value == ' ':
            value = 0
        if value == '':
            value = 0
        return float(value)


class PBWEntry(ListEntry):
    def _check_value(self, value):
        if value == ' ':
            value = 0
        if value == '':
            value = 0
        return float(value)


class PBMEntry(ListEntry):
    def _check_value(self, value):
        if value in ['', 's', 'r', 'j']:
            return str(value)
        msg = f"{value} is not '',s,r,j"
        raise ValueError(msg)


class EnvelopeEntry(EntryBase):
    _value: str
    _p: list
    _v: list
    separater: str = ','

    @property
    def value(self) -> str:
        if len(self._p) == 3:
            return '{:.2f},{:.2f},{:.2f},{},{},{},{}'.format(  # noqa: UP032
                self._p[0],
                self._p[1],
                self._p[2],
                self._v[0],
                self._v[1],
                self._v[2],
                self._v[3],
            )
        if len(self._p) == 4:
            return '{:.2f},{:.2f},{:.2f},{},{},{},{},%,{:.2f}'.format(  # noqa: UP032
                self._p[0],
                self._p[1],
                self._p[2],
                self._v[0],
                self._v[1],
                self._v[2],
                self._v[3],
                self._p[3],
            )
        if len(self._p) == 5:
            return '{:.2f},{:.2f},{:.2f},{},{},{},{},%,{:.2f},{:.2f},{}'.format(  # noqa: UP032
                self._p[0],
                self._p[1],
                self._p[2],
                self._v[0],
                self._v[1],
                self._v[2],
                self._v[3],
                self._p[3],
                self._p[4],
                self._v[4],
            )

        return self._value

    @property
    def p(self) -> list:
        return self._p[:]

    @property
    def v(self) -> list:
        return self._v[:]

    @value.setter
    def value(self, value: str):
        self._set_value(value)
        self._set_update()
        self._hasValue = True

    def _set_value(self, value):
        tmp: list = value.split(self.separater)
        self._p = []
        self._v = []
        try:
            for i in range(len(tmp)):
                if i in [0, 1, 2, 8, 9]:
                    self._p.append(float(tmp[i]))
                elif i in [3, 4, 5, 6, 10]:
                    self._v.append(int(tmp[i]))
        except Exception as e:
            raise ValueError(f'{value} is not envelope pattern') from e
        self._value = value

    def init(self, value: list):
        self._set_value(value)
        self._hasValue = True

    def __str__(self) -> str:
        return self.value

    def set_p(self, pos: int, value: float):
        self._p[pos] = float(value)
        self._set_update()

    def set_v(self, pos: int, value: int):
        self._v[pos] = int(value)
        self._set_update()


class VibratoEntry(EntryBase):
    _length: float
    _cycle: float
    _depth: float
    _fadeInTime: float
    _fadeOutTime: float
    _phase: float
    _height: float
    _amp: float
    _value: str
    separater: str = ','

    @property
    def length(self) -> float:
        return self._length

    @property
    def cycle(self) -> float:
        return self._cycle

    @property
    def depth(self) -> float:
        return self._depth

    @property
    def fadeInTime(self) -> float:
        return self._fadeInTime

    @property
    def fadeOutTime(self) -> float:
        return self._fadeOutTime

    @property
    def phase(self) -> float:
        return self._phase

    @property
    def height(self) -> float:
        return self._height

    @property
    def amp(self) -> float:
        return self._amp

    @property
    def value(self) -> str:
        return '{:.2f},{:.2f},{:.2f},{:.2f},{:.2f},{:.2f},{:.2f},{:.2f}'.format(  # noqa: UP032
            self._length,
            self._cycle,
            self._depth,
            self._fadeInTime,
            self._fadeOutTime,
            self._phase,
            self._height,
            self._amp,
        )

    @length.setter
    def length(self, value: float):
        self._length = float(value)
        self._set_update()

    @cycle.setter
    def cycle(self, value: float):
        self._cycle = float(value)
        self._set_update()

    @depth.setter
    def depth(self, value: float):
        self._depth = float(value)
        self._set_update()

    @fadeInTime.setter
    def fadeInTime(self, value: float):
        self._fadeInTime = float(value)
        self._set_update()

    @fadeOutTime.setter
    def fadeOutTime(self, value: float):
        self._fadeOutTime = float(value)
        self._set_update()

    @phase.setter
    def phase(self, value: float):
        self._phase = float(value)
        self._set_update()

    @height.setter
    def height(self, value: float):
        self._height = float(value)
        self._set_update()

    @amp.setter
    def amp(self, value: float):
        self._amp = float(value)
        self._set_update()

    @value.setter
    def value(self, value: str):
        values: list = value.split(self.separater)
        self.length = values[0]
        self.cycle = values[1]
        self.depth = values[2]
        self.fadeInTime = values[3]
        self.fadeOutTime = values[4]
        self.phase = values[5]
        self.height = values[6]
        self.amp = values[7]
        self._hasValue = True

    def init(self, value: str):
        self.value = value
        self._isUpdate = False

    def __str__(self) -> str:
        return self.value


class LabelEntry(StringEntry):
    pass


class DirectEntry(BoolEntry):
    pass


class RegionEntry(StringEntry):
    pass


class RegionEndEntry(StringEntry):
    pass


class FlagsEntry(StringEntry):
    @property
    def hasValue(self) -> bool:
        return self._hasValue

    @hasValue.setter
    def hasValue(self, value: bool):
        self._hasValue = value
