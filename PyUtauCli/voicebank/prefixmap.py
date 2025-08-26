import os.path

from ..common import convert_notenum


class MapRecord:
    """PrefixMapの各行のデータを扱います。

    Attributes
    ----------
    key: str

        | 音名。C4,D#3,Ab5など
        | この値は、loadしたprefix.mapをsaveするときに活用します。
        | 参照には活用しません。

    prefix: str
    suffix: str
    """

    key: str
    prefix: str
    suffix: str

    def __init__(self, record: str):
        """
        Parameters
        ----------
        record: str
            key,prefix,suffixの順でタブで区切った文字列

        Raises
        ------
        ValueError
            レコードのフォーマットに則らない文字列が渡されたとき
        """
        try:
            self.key, self.prefix, self.suffix = record.split("\t")
        except Exception as e:
            raise ValueError(
                f"can't set prefix map value.{record} is bad format."
            ) from e


class PrefixMap:
    """prefix.mapのデータを扱います。"""

    _key: list = list(range(24, 108))
    _values: dict = {}

    def __init__(self, dirpath: str = ""):
        """
        Parameters
        ----------
        dirpath: str, default ""
            音源のルートディレクトリのパス。引数が与えられている場合self.load(dirpath)を実行する。

        Raises
        ------
        FileNotFoundError
            load実行時prefix.mapが見つからなかった場合
        UnicodeDecodeError
            load実行時ファイルがcp932でもutf-8でもなかった場合
        """
        for i in self._key:
            self._values[i] = MapRecord(convert_notenum.toStr(i) + "\t\t")
        if dirpath != "":
            self.load(dirpath)

    def __getitem__(self, key) -> MapRecord:
        if key in self._values:
            return self._values[key]
        return self._values[convert_notenum.toInt(key)]

    def load(self, dirpath: str, filename: str = "prefix.map"):
        """
        *dirpath\\\\prefix.map* を読み込んでself._valueを更新する。

        Parameters
        ----------
        dirpath: str
            音源のルートディレクトリのパス

        filename: str, default "prefix.map"
            ファイル名。UTAU本体の仕様では指定不要ですが、複数のprefix.mapを読み込む仕様を想定

        Raises
        ------
        FileNotFoundError
            prefix.mapが見つからなかった場合
        UnicodeDecodeError
            ファイルがcp932でもutf-8でもなかった場合
        """
        filepath: str = os.path.join(dirpath, filename)
        lines: list
        if not os.path.isfile(filepath):
            raise FileNotFoundError(f"{filepath} is not found.")

        try:
            with open(filepath, encoding="cp932") as fr:
                lines = fr.read().replace("\r", "").split("\n")
        except Exception:
            try:
                with open(filepath, encoding="utf-8") as fr:
                    lines = fr.read().replace("\r", "").split("\n")
            except UnicodeDecodeError as e:
                e.reason = "can't read prefix.map. because required character encoding is utf-8 or cp932"
                raise e

        for line in lines:
            if line == "":
                continue
            if "\t" not in line:
                continue
            self._values[convert_notenum.toInt(line.split("\t")[0])] = MapRecord(line)

    def save(self, dirpath: str, filename: str = "prefix.map", encoding: str = "cp932"):
        """
        *dirpath\\\\prefix.map* を *encoding* で保存する。

        Parameters
        ----------
        dirpath: str
            音源のルートディレクトリのパス

        filename: str, default "prefix.map"
            ファイル名。UTAU本体の仕様では指定不要ですが、複数のprefix.mapを読み込む仕様を想定

        encoding: str, default "cp932"

            | 保存する際の文字コード
            | UTAU本体のGUIを考えるとcp932が無難

        Raises
        ------
        OSError
            character.txtに書き込み権限がないとき
        UnicodeDecodeError
            パラメータをcp932に変換できなかったとき
        """
        filepath: str = os.path.join(dirpath, filename)
        with open(filepath, "w", encoding=encoding) as fw:
            for i in range(len(self._values)):
                fw.write(
                    self._values[107 - i].key
                    + "\t"
                    + self._values[107 - i].prefix
                    + "\t"
                    + self._values[107 - i].suffix
                    + "\r\n"
                )
