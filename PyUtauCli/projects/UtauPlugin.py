import os
import os.path

from .Ust import Ust


class UtauPlugin(Ust):
    """
    | UTAUのプラグイン用一時ファイルを扱います。
    | ほぼ、Ustと共通の仕様ですが、主に書き出しに関する仕様が異なります。
    """

    def save(self, filepath: str = '', encoding: str = 'cp932'):
        """
        | self.filepathもしくはfilepathにファイルを保存します。
        | windows版UTAUとの互換性を優先してcp932を優先します。

        Parameters
        ----------
        filepath: str, default ""
        encoding: str, default "cp932"
        """
        if filepath != '':
            self.filepath = filepath
        if os.path.split(self.filepath)[0] != '':
            os.makedirs(os.path.split(self.filepath)[0], exist_ok=True)
        self.logger.info(f'saving utau plugin temp to:{self.filepath}')
        with open(self.filepath, 'w', encoding=encoding) as fw:
            for note in self.notes:
                fw.write(f'[{str(note.num)}]\n')
                if note.num.value == '#DELETE':
                    continue
                if note.length.hasValue and note.length.isUpdate:
                    fw.write(f'Length={str(note.length)}\n')
                if note.lyric.hasValue and note.lyric.isUpdate:
                    fw.write(f'Lyric={str(note.lyric)}\n')
                if note.notenum.hasValue and note.notenum.isUpdate:
                    fw.write(f'NoteNum={str(note.notenum.value)}\n')
                if note.tempo.hasValue and note.tempo.isUpdate:
                    fw.write(f'Tempo={str(note.tempo)}\n')
                if note.pre.hasValue and note.pre.isUpdate:
                    fw.write(f'PreUtterance={str(note.pre)}\n')
                if note.ove.hasValue and note.ove.isUpdate:
                    fw.write(f'VoiceOverlap={str(note.ove)}\n')
                if note.stp.hasValue and note.stp.isUpdate:
                    fw.write(f'StartPoint={str(note.stp)}\n')
                if note.velocity.hasValue and note.velocity.isUpdate:
                    fw.write(f'Velocity={str(note.velocity)}\n')
                if note.intensity.hasValue and note.intensity.isUpdate:
                    fw.write(f'Intensity={str(note.intensity)}\n')
                if note.modulation.hasValue and note.modulation.isUpdate:
                    fw.write(f'Modulation={str(note.modulation)}\n')
                if note.pitches.hasValue and note.pitches.isUpdate:
                    fw.write(f'Pitches={str(note.pitches)}\n')
                if note.pbStart.hasValue and note.pbStart.isUpdate:
                    fw.write(f'PBStart={str(note.pbStart)}\n')
                if note.pbs.hasValue and note.pbs.isUpdate:
                    fw.write(f'PBS={str(note.pbs)}\n')
                if note.pby.hasValue and note.pby.isUpdate:
                    fw.write(f'PBY={str(note.pby)}\n')
                if note.pbm.hasValue and note.pbm.isUpdate:
                    fw.write(f'PBM={str(note.pbm)}\n')
                if note.pbw.hasValue and note.pbw.isUpdate:
                    fw.write(f'PBW={str(note.pbw)}\n')
                if note.flags.hasValue and note.flags.isUpdate:
                    fw.write(f'Flags={str(note.flags)}\n')
                if note.vibrato.hasValue and note.vibrato.isUpdate:
                    fw.write(f'VBR={str(note.vibrato)}\n')
                if note.envelope.hasValue and note.envelope.isUpdate:
                    fw.write(f'Envelope={str(note.envelope)}\n')
                if note.label.hasValue and note.label.isUpdate:
                    fw.write(f'Label={str(note.label)}\n')
                if note.direct.hasValue and note.direct.isUpdate:
                    fw.write(f'$direct={str(note.direct)}\n')
                if note.region.hasValue and note.region.isUpdate:
                    fw.write(f'$region={str(note.region)}\n')
                if note.region_end.hasValue and note.region_end.isUpdate:
                    fw.write(f'$region_end={str(note.region_end)}\n')
        self.logger.info(f'saving utau plugin temp to:{self.filepath} complete')
