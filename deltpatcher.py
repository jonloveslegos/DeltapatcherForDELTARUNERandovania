from pathlib import Path

def GetDeltaPath() -> Path:
    return Path(__file__).parent

def patchfile(input_file: Optional[Path], output_file: Path, patch_data: dict):
        """
        Invokes the necessary tools to patch the game.
        :param input_file: Vanilla copy of the game. Required if uses_input_file_directly or has_internal_copy is False.
        :param output_file: Where a modified copy of the game is placed.
        :param patch_data: Data created by create_patch_data.
        :param internal_copies_path: Path to where all internal copies are stored.
        :param progress_update: Pushes updates as slow operations are done.
        :return: None
        """
        
        import subprocess
        new_config = copy.copy(patch_data)
        my_seed = new_config.pop("description")
        Path(output_file.joinpath("Deltarune Randomizer " + my_seed)).mkdir(exist_ok=True)
        tomakepath = Path(output_file.joinpath("Deltarune Randomizer " + my_seed))
        copyDir(input_file,tomakepath)
        subprocess.run([str(deltpatcher.GetDeltaPath().joinpath("xdelta.exe")), '-f', '-d','-s',str(input_file.joinpath("data.win")), str(deltpatcher.GetDeltaPath().joinpath("PATCH THIS.xdelta")),str(tomakepath.joinpath("data.win"))],check=True)
        Path(tomakepath).joinpath("Deltarune Randomizer Seed.txt").unlink(missing_ok=True)
        has_spoiler = new_config.pop("has_spoiler")
        patch_as_str = json.dumps(new_config, indent=4, separators=(',', ': '))
        if has_spoiler:
            Path(tomakepath).joinpath("Deltarune Randomizer "+my_seed+"-patcher.json").write_text(patch_as_str)
        with Path(tomakepath).joinpath("Deltarune Randomizer Seed.txt").open("w") as f:
            for item in patch_data["pickups"]:
                f.write(str(item["pickup_index"]))
                f.write('\n')
                f.write(str(item["item_index"]))
                f.write('\n')
                f.write(str(item["progressive"]))
                f.write('\n')
            for item in patch_data["starting_items"]:
                f.write(str(item["item_index"]))
                f.write('\n')