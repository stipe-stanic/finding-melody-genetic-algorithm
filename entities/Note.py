from typing import Optional

class Note:
    def __init__(self, note: str, octave: int, accidental: Optional[str] = None, duration: float = 0.5):
        self.note = note
        self.octave = octave
        self.accidental = accidental
        self.duration = duration

    def __str__(self) -> str:
        return f"{self.note}{self.accidental}{self.octave}-{self.duration}"

    def __repr__(self) -> str:
        return f"Note: {self.note}{self.octave}{self.accidental}-{self.duration}"

    def __hash__(self) -> int:
        return hash((self.note, self.octave, self.accidental, self.duration))

    def __eq__(self, other) -> bool:
        if not isinstance(other, Note):
            return False
        return self.note == other.note and self.octave == other.octave \
                    and self.accidental == other.accidental and self.duration == other.duration
