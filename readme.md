# py-fonttools-script

This is the repository containing useful scripts when dealing with CJK fonts.

## Tools

### `get_cjk_char_list`

Get CJK Unified Ideographs characters that are in the `cmap` table of an OpenType font. With slight modification it can list all mapped Unicode characters in the font file.

Dependency: `fontTools`

### `convert_ufo`

Converts a TTF/OTF font to UFO format.

Dependency: `defcon`, `ufo-extractor`

### `win_file_lister`

List files under the folder that the program is in.

Dependency: `natsort`

## Precompiled release

Download precompiled Windows release under Releases page, or under `\dist` folder.

## Build

Use `pyinstaller *.spec` to build the programs. Best if UPX is provided.

## License

Released under MIT License.
